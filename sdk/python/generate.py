#!/usr/bin/env python3
"""Generate apisio/operations.py from the OpenAPI documents apis.io PUBLISHES.

The source is `all/apis-io/openapi/_original/` — the as-published archive, not the refined
mirror. Those are different document sets (roadmap#291), and a client generated from our own
derivative would describe an API nobody can call.

Why generated rather than hand-written: 110 operations across 19 documents. Hand-written
bindings drift from the contract silently and the drift is invisible until a consumer hits it.
Generated ones cannot — `make generate` re-runs this, and a diff is the review.

    python3 generate.py            # write apisio/operations.py
    python3 generate.py --check    # non-zero if the committed file is stale
"""

from __future__ import annotations

import argparse
import glob
import keyword
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SPECS = os.path.normpath(os.path.join(HERE, "..", "..", "openapi", "_original"))
OUT = os.path.join(HERE, "apisio", "operations.py")
# ONE generator, THREE targets. The spec-reading is the hard part and it is solved once here; a
# second parser per language is how three clients drift from each other and from the contract.
SDK_ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT_JS = os.path.join(SDK_ROOT, "javascript", "src", "operations.js")
OUT_GO = os.path.join(SDK_ROOT, "go", "apisio", "operations.go")

# Operations the client deliberately does not bind.
#
# `/search/apis` lives in a legacy document describing a surface the v1 API re-expresses as
# `/search`; binding both would publish two names for one thing and invite the wrong one.
SKIP_FILES = {"apis-io-search-openapi.yaml"}

HEADER = '''"""apis.io operation bindings — GENERATED, DO NOT EDIT.

Regenerate with `python3 generate.py` from the OpenAPI documents in
`all/apis-io/openapi/_original/` — the documents apis.io publishes, not the refined mirror.

{count} operations across {docs} documents, generated {stamp}.

Every method is a thin call through `Client.request`. Collection endpoints return a `Page`
(a list, with `.meta`/`.total`/`.pages`); everything else returns the parsed body.
"""

from __future__ import annotations

from typing import Any

__all__ = ["Operations"]


class Operations:
    """Mixin carrying one method per published operation. `Client` inherits it."""
'''

METHOD = '''
    def {name}(self{sig}) -> Any:
        """{doc}

        ``{verb} {path}``
        """
        return self.{call}
'''


def snake(s: str) -> str:
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", s.replace("-", "_")).lower()
    s = re.sub(r"__+", "_", s).strip("_")
    return s + "_" if keyword.iskeyword(s) else s


def py_param(name: str) -> str:
    p = snake(name)
    return p + "_" if keyword.iskeyword(p) else p


def _deref(doc, node):
    """One level of local $ref. Path and query parameters in these documents are hoisted into
    #/components/parameters/ and referenced, which is the standard way to declare a parameter
    shared across operations — and invisible to a reader that does not resolve it."""
    if not (isinstance(node, dict) and isinstance(node.get("$ref"), str)):
        return node
    m = re.match(r"^#/(.+)$", node["$ref"])
    if not m:
        return node
    cur = doc
    for seg in m.group(1).split("/"):
        seg = seg.replace("~1", "/").replace("~0", "~")
        if not isinstance(cur, dict) or seg not in cur:
            return node
        cur = cur[seg]
    return cur if isinstance(cur, dict) else node


def load_ops():
    docs, ops, seen = 0, [], {}
    for f in sorted(glob.glob(os.path.join(SPECS, "*"))):
        if os.path.basename(f) in SKIP_FILES:
            continue
        try:
            d = yaml.safe_load(open(f, encoding="utf-8"))
        except Exception:                                              # noqa: BLE001
            continue
        if not isinstance(d, dict) or not isinstance(d.get("paths"), dict):
            continue
        docs += 1
        for path, item in d["paths"].items():
            if not isinstance(item, dict):
                continue
            shared = item.get("parameters") or []
            for verb, op in item.items():
                if verb not in ("get", "post", "put", "patch", "delete") or not isinstance(op, dict):
                    continue
                oid = op.get("operationId")
                if not oid:
                    continue
                name = snake(oid)
                if name in seen:
                    # Two documents claiming one operationId is a contract defect, not something
                    # to paper over by silently picking one.
                    raise SystemExit(
                        f"duplicate operationId {oid!r}: {seen[name]} and {os.path.basename(f)}")
                seen[name] = os.path.basename(f)
                params = [_deref(d, x) for x in (list(shared) + list(op.get("parameters") or []))]
                ops.append({
                    "name": name, "verb": verb.upper(), "path": path,
                    "summary": (op.get("summary") or op.get("description") or oid).strip(),
                    # From the PATH TEMPLATE, not the declarations. A path parameter is whatever
                    # the template names, by definition — and the declarations cannot be trusted
                    # to say so: every one in this API is a $ref to #/components/parameters/Slug,
                    # which a reader that does not resolve refs sees as a dict with no `in` and
                    # no `name`. That is the same hoisted-parameter defect score.rb's
                    # operation_params exists to work around (Adyen's Idempotency-Key), and the
                    # first cut of this generator walked straight into it: 108 methods, not one
                    # of them taking a slug.
                    "path_params": re.findall(r"\{([^}]+)\}", path),
                    "query_params": [p["name"] for p in params
                                     if isinstance(p, dict) and p.get("in") == "query"
                                     and p.get("name")],
                    "body": bool(op.get("requestBody")),
                    "collection": _is_collection(d, op),
                })
    return docs, sorted(ops, key=lambda o: o["name"])


def _is_collection(doc, op) -> bool:
    """Does the 200 answer with the {meta, data} envelope?

    Read from the schema rather than guessed from the path — `/providers/{slug}` and
    `/providers` differ in shape, and a name-based rule gets the sub-resources wrong.

    RESOLVES $ref, and must: every list response here is `{"$ref":
    "#/components/schemas/ProviderList"}`, so the first cut saw no `properties`, decided nothing
    was a collection, and `list_providers()` returned a raw dict that callers could not iterate.
    Third time this API's hoisting caught this generator out — parameters, then path params, now
    response schemas. In these documents, assume a $ref until proven otherwise.
    """
    try:
        content = ((op.get("responses") or {}).get("200") or {}).get("content") or {}
        for media in content.values():
            schema = _deref(doc, (media or {}).get("schema") or {})
            props = (schema or {}).get("properties") or {}
            if "data" in props and "meta" in props:
                return True
            # one more hop: allOf composition over a shared envelope
            for sub in (schema or {}).get("allOf") or []:
                sp = (_deref(doc, sub) or {}).get("properties") or {}
                if "data" in sp or "meta" in sp:
                    return True
    except Exception:                                                  # noqa: BLE001
        pass
    return False


def render(docs: int, ops: list) -> str:
    import datetime
    out = [HEADER.format(count=len(ops), docs=docs,
                         stamp=datetime.date.today().isoformat())]
    for o in ops:
        path_args = [py_param(p) for p in o["path_params"]]
        sig = "".join(f", {a}: str" for a in path_args)
        if o["body"]:
            sig += ", body: Any = None"
        sig += ", **params: Any"

        # f-string path, with the python names substituted back into the template.
        tpl = o["path"]
        for orig, arg in zip(o["path_params"], path_args):
            tpl = tpl.replace("{" + orig + "}", "{" + arg + "}")
        literal = f'f"{tpl}"' if path_args else f'"{tpl}"'

        if o["verb"] == "GET":
            call = f"page({literal}, **params)" if o["collection"] else f"get({literal}, **params)"
        elif o["verb"] == "DELETE":
            call = f"delete({literal}, **params)"
        else:
            call = (f'request("{o["verb"]}", {literal}, params=params, json=body)'
                    if o["body"] else f'request("{o["verb"]}", {literal}, params=params)')

        doc = o["summary"].replace("\\", "\\\\").replace('"""', "'''")
        doc = " ".join(doc.split())
        if len(doc) > 150:
            doc = doc[:147].rstrip() + "..."
        if o["query_params"]:
            doc += "\n\n        Query parameters: " + ", ".join(sorted(o["query_params"])[:14])
        out.append(METHOD.format(name=o["name"], sig=sig, doc=doc,
                                 verb=o["verb"], path=o["path"], call=call))
    return "".join(out)



JS_HEADER = """/* apis.io operation bindings — GENERATED, DO NOT EDIT.
 *
 * Regenerate with `python3 ../python/generate.py` from the OpenAPI documents in
 * all/apis-io/openapi/_original/ — the documents apis.io publishes, not the refined mirror.
 *
 * {count} operations across {docs} documents, generated {stamp}.
 */

import {{ Transport }} from './client.js';

export class Client extends Transport {{
"""

JS_METHOD = """
  /** {doc}
   *  `{verb} {path}` */
  {name}({sig}) {{
    return this.{call};
  }}
"""

GO_HEADER = """// apis.io operation bindings — GENERATED, DO NOT EDIT.
//
// Regenerate with `python3 ../../python/generate.py` from the OpenAPI documents in
// all/apis-io/openapi/_original/ — the documents apis.io publishes, not the refined mirror.
//
// {count} operations across {docs} documents, generated {stamp}.

package apisio

import "context"
"""

GO_METHOD = """
// {gname} — {doc}
//
// {verb} {path}
func (c *Client) {gname}(ctx context.Context{sig}) ({ret}, error) {{
	return c.{call}
}}
"""


def camel(name):
    parts = name.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


def pascal(name):
    return "".join(p.title() for p in name.split("_"))


def render_js(docs, ops):
    import datetime
    out = [JS_HEADER.format(count=len(ops), docs=docs, stamp=datetime.date.today().isoformat())]
    for o in ops:
        args = [py_param(p) for p in o["path_params"]]
        sig = ", ".join(args + (["body = null"] if o["body"] else []) + ["params = {}"])
        tpl = o["path"]
        for orig, a in zip(o["path_params"], args):
            tpl = tpl.replace("{" + orig + "}", "${" + a + "}")
        lit = f"`{tpl}`"
        if o["verb"] == "GET":
            call = f"page({lit}, params)" if o["collection"] else f"get({lit}, params)"
        elif o["verb"] == "DELETE":
            call = f"delete({lit}, params)"
        else:
            call = (f"request('{o['verb']}', {lit}, {{ params, json: body }})" if o["body"]
                    else f"request('{o['verb']}', {lit}, {{ params }})")
        doc = " ".join(o["summary"].split()).replace("*/", "* /")[:140]
        out.append(JS_METHOD.format(name=camel(o["name"]), sig=sig, doc=doc,
                                    verb=o["verb"], path=o["path"], call=call))
    out.append("}\n")
    return "".join(out)


def render_go(docs, ops):
    import datetime
    out = [GO_HEADER.format(count=len(ops), docs=docs, stamp=datetime.date.today().isoformat())]
    for o in ops:
        args = [py_param(p) for p in o["path_params"]]
        sig = "".join(f", {a} string" for a in args)
        if o["body"]:
            sig += ", body any"
        sig += ", params map[string]any"
        tpl = o["path"]
        fmtargs = []
        for orig, a in zip(o["path_params"], args):
            tpl = tpl.replace("{" + orig + "}", "%s")
            fmtargs.append(a)
        lit = (f'fmt.Sprintf("{tpl}", {", ".join(fmtargs)})' if fmtargs else f'"{tpl}"')
        if o["verb"] == "GET" and o["collection"]:
            call, ret = f"GetPage(ctx, {lit}, params)", "*Page"
        elif o["verb"] == "GET":
            call, ret = f"Get(ctx, {lit}, params)", "any"
        else:
            body = "body" if o["body"] else "nil"
            call, ret = f'Request(ctx, "{o["verb"]}", {lit}, params, {body})', "any"
        doc = " ".join(o["summary"].split())[:120]
        out.append(GO_METHOD.format(gname=pascal(o["name"]), sig=sig, doc=doc,
                                    verb=o["verb"], path=o["path"], call=call, ret=ret))
    body = "".join(out)
    if "fmt.Sprintf" in body:
        body = body.replace('import "context"', 'import (\n\t"context"\n\t"fmt"\n)')
    return body


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero if operations.py is stale")
    a = ap.parse_args()

    if not os.path.isdir(SPECS):
        print(f"published specs not found: {SPECS}", file=sys.stderr)
        return 2
    docs, ops = load_ops()
    new = render(docs, ops)
    targets = [(OUT, new), (OUT_JS, render_js(docs, ops)), (OUT_GO, render_go(docs, ops))]

    strip = lambda s: re.sub(r"generated \d{4}-\d\d-\d\d", "generated", s)             # noqa: E731
    if a.check:
        stale = []
        for path, text in targets:
            cur = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
            if strip(cur) != strip(text):
                stale.append(os.path.relpath(path, SDK_ROOT))
        if stale:
            print(f"STALE: {', '.join(stale)} — {len(ops)} operations in {docs} published documents")
            return 1
        print(f"all 3 clients current — {len(ops)} operations, {docs} documents")
        return 0

    for path, text in targets:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"  wrote {os.path.relpath(path, SDK_ROOT)}")
    print(f"{len(ops)} operations from {docs} published documents, 3 clients")
    return 0


if __name__ == "__main__":
    sys.exit(main())
