"""`apisio` — a command-line client for the apis.io catalog.

    apisio search payments
    apisio provider stripe
    apisio rating stripe
    apisio fix stripe                 # the ranked, costed punch list for a listing you own
    apisio gates stripe               # what stands between this listing and the next band
    apisio call list_tags --limit 5   # any of the 108 published operations

The command set leads with the provider-improvement flow — rating, fix, gates, simulate, claim,
submit — because that is the sequence a provider actually walks, and it is the one that is
tedious over raw HTTP: seven authenticated calls whose output feeds the next.

Key from `APIS_IO_API_KEY`, or `--api-key`. Most of the catalog is free and needs neither.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from . import Client, __version__
from .client import ApisIoError, PaymentRequired, Unauthenticated


def _out(obj, as_json: bool) -> None:
    if as_json:
        json.dump(obj, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
        return
    _render(obj)


def _render(obj, indent: int = 0) -> None:
    pad = "  " * indent
    if isinstance(obj, list):
        if not obj:
            print(f"{pad}(none)")
            return
        for row in obj:
            if isinstance(row, dict):
                name = row.get("name") or row.get("label") or row.get("title") or ""
                slug = row.get("slug") or row.get("id") or row.get("aid") or ""
                extra = [f"{k}={row[k]}" for k in ("band", "composite", "score", "points",
                                                   "type", "status", "tier")
                         if row.get(k) is not None]
                head = f"{pad}{slug:<34}" if slug else pad
                print(f"{head}{name}" + (f"   {' '.join(extra)}" if extra else ""))
            else:
                print(f"{pad}{row}")
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "meta":
                continue
            if isinstance(v, (dict, list)) and v:
                print(f"{pad}{k}:")
                _render(v, indent + 1)
            elif not isinstance(v, (dict, list)):
                print(f"{pad}{k}: {v}")
        return
    print(f"{pad}{obj}")


def _client(a) -> Client:
    return Client(api_key=a.api_key or os.environ.get("APIS_IO_API_KEY"),
                  base_url=a.base_url)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="apisio", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--api-key", help="defaults to $APIS_IO_API_KEY")
    p.add_argument("--base-url", default="https://apis.io/api/v1")
    p.add_argument("--json", action="store_true", help="raw JSON instead of a summary")
    p.add_argument("--version", action="version", version=f"apisio {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    def cmd(name, help_, *args):
        s = sub.add_parser(name, help=help_)
        for a_, kw in args:
            s.add_argument(a_, **kw)
        return s

    SLUG = ("slug", {"help": "provider slug, e.g. stripe"})
    LIMIT = ("--limit", {"type": int, "default": 20})

    cmd("search", "Search the whole catalog", ("q", {"help": "query"}), LIMIT)
    cmd("providers", "List and filter providers",
        ("--q", {}), ("--tag", {}), ("--industry", {}), ("--min-score", {"type": float}), LIMIT)
    cmd("provider", "One provider's record", SLUG)
    cmd("artifacts", "What a provider publishes", SLUG)

    # --- the provider-improvement flow, in the order a provider walks it ---
    cmd("rating", "This listing's Kin Score", SLUG)
    cmd("fix", "The ranked, costed punch list", SLUG)
    cmd("gates", "What stands between this listing and the next band", SLUG)
    cmd("simulate", "Project a score if given fixes landed", SLUG,
        ("--fix", {"action": "append", "default": [], "metavar": "CHECK_ID",
                   "help": "repeatable"}))
    cmd("claim", "Claim this listing", SLUG)
    cmd("submit", "Submit an artifact for this listing", SLUG,
        ("--type", {"required": True, "help": "e.g. OpenAPI, MCPServer"}),
        ("--url", {"required": True}))
    cmd("correct", "Report a correction on this listing", SLUG,
        ("--message", {"required": True}))

    c = cmd("call", "Call any published operation by name")
    c.add_argument("operation", help="e.g. list_tags, get_cohort")
    c.add_argument("args", nargs="*", help="positional path args, then key=value query params")

    sub.add_parser("operations", help="List every operation the client binds")

    a = p.parse_args(argv)
    api = _client(a)

    try:
        if a.cmd == "operations":
            names = sorted(n for n in dir(Client)
                           if not n.startswith("_") and callable(getattr(Client, n))
                           and n not in ("request", "get", "post", "delete", "page", "paginate"))
            for n in names:
                doc = (getattr(Client, n).__doc__ or "").strip().splitlines()[0]
                print(f"  {n:<34} {doc}")
            print(f"\n  {len(names)} operations")
            return 0

        if a.cmd == "search":
            # /search is SECTIONED, not a {meta,data} collection: one {total, top} block per
            # kind (apis, providers, tags, capabilities). Flattening it to a list would throw
            # away the one thing that makes the endpoint useful — which kind matched.
            res = api.search(q=a.q, limit=a.limit)
            if a.json:
                _out(res, True)
            else:
                for kind in ("providers", "apis", "tags", "capabilities"):
                    block = (res or {}).get(kind)
                    if not isinstance(block, dict):
                        continue
                    top = block.get("top") or []
                    print(f"{kind.upper()}  ({block.get('total', 0)} total)")
                    _render(top[:a.limit], 1)
                    print()
                note = (res or {}).get("note")
                if note:
                    print(f"note: {note}")
        elif a.cmd == "providers":
            _out(list(api.list_providers(q=a.q, tags=a.tag, industry=a.industry,
                                         min_score=a.min_score, limit=a.limit)), a.json)
        elif a.cmd == "provider":
            _out(api.get_provider(a.slug), a.json)
        elif a.cmd == "artifacts":
            _out(api.get_provider_artifacts(a.slug), a.json)
        elif a.cmd == "rating":
            _out(api.get_provider_rating(a.slug), a.json)
        elif a.cmd == "fix":
            _out(api.what_can_i_fix(a.slug), a.json)
        elif a.cmd == "gates":
            _out(api.readiness_gates(a.slug), a.json)
        elif a.cmd == "simulate":
            _out(api.simulate_fixes(a.slug, body={"fixes": a.fix}), a.json)
        elif a.cmd == "claim":
            _out(api.claim_listing(a.slug, body={}), a.json)
        elif a.cmd == "submit":
            _out(api.submit_artifact(a.slug, body={"type": a.type, "url": a.url}), a.json)
        elif a.cmd == "correct":
            _out(api.report_correction(a.slug, body={"message": a.message}), a.json)
        elif a.cmd == "call":
            fn = getattr(api, a.operation, None)
            if not callable(fn):
                print(f"no such operation: {a.operation} — try `apisio operations`",
                      file=sys.stderr)
                return 2
            pos = [x for x in a.args if "=" not in x]
            kw = dict(x.split("=", 1) for x in a.args if "=" in x)
            _out(fn(*pos, **kw), a.json)

    except Unauthenticated as e:
        print(f"401 — {e.body.get('detail')}", file=sys.stderr)
        if e.resource_metadata:
            print(f"     bootstrap from: {e.resource_metadata}", file=sys.stderr)
        return 4
    except PaymentRequired as e:
        print(f"402 — {e.body.get('detail')}", file=sys.stderr)
        if e.plans_url:
            print(f"     plans: {e.plans_url}", file=sys.stderr)
        return 5
    except ApisIoError as e:
        print(f"{e.status} — {e.body.get('detail') or e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
