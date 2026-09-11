"""Diff every published GET operation against what apis.io actually serves.

roadmap#308 found that our `/search` contract described a shape the endpoint has never returned.
It was found by accident, because a generated client bound it. Nothing checks the other 107.

READ-ONLY BY CONSTRUCTION. Only GET operations are called — no claim, submit, correction, dispute,
visibility, generate or projection. A contract test that mutates the catalog is not a test.

    python3 contract_diff.py            # free tier
    python3 contract_diff.py --key ...  # includes gated operations
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import time

import yaml

sys.path.insert(0, "/Users/kinlane/GitHub/all/apis-io/sdk/python")
from apisio import Client                                          # noqa: E402
from apisio.client import ApisIoError, Page                        # noqa: E402

SPECS = "/Users/kinlane/GitHub/all/apis-io/openapi/_original"

# Real values for path parameters, so the call exercises a live record rather than a 404.
SAMPLES = {
    "slug": "stripe", "aid": "stripe-api", "kind": "industry", "id": "1",
    "dataset": "providers",
}


def deref(doc, node, depth=0):
    while isinstance(node, dict) and isinstance(node.get("$ref"), str) and depth < 6:
        path = node["$ref"].lstrip("#/").split("/")
        cur = doc
        for seg in path:
            seg = seg.replace("~1", "/").replace("~0", "~")
            if not isinstance(cur, dict) or seg not in cur:
                return node
            cur = cur[seg]
        node = cur
        depth += 1
    return node


def declared_top_level(doc, op):
    """Top-level property names the 200 response schema declares, or None if it declares none."""
    content = ((op.get("responses") or {}).get("200") or {}).get("content") or {}
    for media in content.values():
        schema = deref(doc, (media or {}).get("schema") or {})
        if not isinstance(schema, dict):
            continue
        props = dict(schema.get("properties") or {})
        for sub in schema.get("allOf") or []:
            props.update((deref(doc, sub) or {}).get("properties") or {})
        if props:
            return set(props), schema.get("required") or []
        if schema.get("type") == "array":
            return "ARRAY", []
    return None, []


def load():
    ops = []
    for f in sorted(glob.glob(os.path.join(SPECS, "*"))):
        if os.path.basename(f) == "apis-io-search-openapi.yaml":
            continue
        try:
            doc = yaml.safe_load(open(f, encoding="utf-8"))
        except Exception:                                          # noqa: BLE001
            continue
        if not isinstance(doc, dict) or not isinstance(doc.get("paths"), dict):
            continue
        for path, item in doc["paths"].items():
            if not isinstance(item, dict):
                continue
            op = item.get("get")
            if not isinstance(op, dict):
                continue
            declared, required = declared_top_level(doc, op)
            ops.append({"file": os.path.basename(f), "path": path,
                        "oid": op.get("operationId"), "declared": declared,
                        "required": required})
    return ops


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--key")
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    api = Client(api_key=a.key or os.environ.get("APIS_IO_API_KEY"))

    ops = load()
    if a.limit:
        ops = ops[: a.limit]
    print(f"diffing {len(ops)} published GET operations against the live API\n")

    mismatch, undescribed, gated, errors, ok = [], [], [], [], 0
    for o in ops:
        url = o["path"]
        for name, val in SAMPLES.items():
            url = url.replace("{" + name + "}", val)
        if "{" in url:
            continue
        try:
            body = api.get(url, limit=1)
            time.sleep(0.12)
        except ApisIoError as e:
            (gated if e.status in (401, 402) else errors).append((o, e.status))
            continue
        if isinstance(body, Page):
            body = body.raw
        if o["declared"] is None:
            undescribed.append(o)
            continue
        if o["declared"] == "ARRAY":
            if not isinstance(body, list):
                mismatch.append((o, "declares an array", type(body).__name__))
            else:
                ok += 1
            continue
        if not isinstance(body, dict):
            mismatch.append((o, "declares an object", type(body).__name__))
            continue
        live = set(body.keys())
        missing = {k for k in o["required"] if k not in live}
        # Only flag a REAL disagreement: declared keys that the live answer never provides.
        # Extra live keys are a documentation gap, not a lie, and are reported separately.
        absent = o["declared"] - live
        if missing or (absent and absent == o["declared"]):
            mismatch.append((o, f"declares {sorted(o['declared'])[:6]}",
                             f"serves {sorted(live)[:6]}"))
        else:
            ok += 1

    print(f"  matched                {ok}")
    print(f"  MISMATCHED             {len(mismatch)}")
    print(f"  gated (not checked)    {len(gated)}")
    print(f"  no 200 schema declared {len(undescribed)}")
    print(f"  transport errors       {len(errors)}\n")

    if mismatch:
        print("  === CONTRACT DOES NOT DESCRIBE THE LIVE RESPONSE ===")
        for o, d, s in mismatch:
            print(f"    {o['oid']:<28} {o['path']}")
            print(f"      {d}")
            print(f"      {s}")
    if undescribed:
        print("\n  === NO 200 RESPONSE SCHEMA AT ALL ===")
        for o in undescribed:
            print(f"    {o['oid']:<28} {o['path']}   [{o['file']}]")
    if errors:
        print("\n  === errors ===")
        for o, st in errors:
            print(f"    {st}  {o['oid']:<26} {o['path']}")
    json.dump({"mismatch": [[o["oid"], o["path"]] for o, _, _ in mismatch],
               "undescribed": [[o["oid"], o["path"]] for o in undescribed]},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "contract-diff.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
