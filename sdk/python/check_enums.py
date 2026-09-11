#!/usr/bin/env python3
"""Check that the vocabularies our published OpenAPIs declare match the ones the scorer emits.

roadmap#311. `contract_diff.py` compares top-level PROPERTY NAMES against live responses, which is
how it found the `/search` shape defect — and it is blind to enum VALUES, which is how it missed a
worse one: every published `Band` enum omitted `emerging`, so a validating client would reject a
correct response for **6,576 providers**.

A name-level diff cannot catch that. This does, and it reads the rubric rather than a copy of it,
so the check cannot go stale the way the enums did.

    python3 check_enums.py          # report
    python3 check_enums.py --strict # non-zero if any published enum disagrees

Read-only. Touches no network and no catalog.
"""

from __future__ import annotations

import argparse
import glob
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SPECS = os.path.normpath(os.path.join(HERE, "..", "..", "openapi", "_original"))
RUBRIC = os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "..", "api-search", "signals", "_data", "scoring.yml"))

# Which rubric list each published vocabulary must agree with. Keyed by a value that only that
# vocabulary contains, so a schema is matched by what it SAYS rather than by what it is named —
# the band enum is called `Band` in eight specs and `band` inside a property in a ninth.
VOCABULARIES = [
    ("composite band", "exemplar", lambda r: [b["id"] for b in r.get("bands") or []], True),
    ("agent-readiness band", "agent-native",
     lambda r: [b["id"] for b in (r.get("agent_readiness") or {}).get("bands") or []], True),
    # FACETS ARE ADVISORY, NOT AUTHORITATIVE, and the difference is the point.
    #
    # The rubric has nine facet KEYS. `/rating/facets` serves eight NAMES, and they are not a
    # subset: it emits each renamed facet under BOTH its key and a snake_cased label, measured on
    # three providers —
    #
    #     access_clarity 76.3 == commercial_clarity 76.3      (label "Access Clarity")
    #     contract_governance 33.3 == governance 33.3         (label "Contract Governance")
    #
    # — while `regulatory` rides in its own top-level block and `open_source` / `upsert` are
    # conditional and absent entirely. So neither vocabulary is a superset of the other, and
    # "make the enum match the rubric" would document a response the API does not send.
    #
    # Reported rather than enforced until that is settled: the aliasing is either deliberate
    # backward compatibility for a rename or an accident, and a consumer summing the object
    # double-counts two of them either way.
    ("facet name", "contract_quality", lambda r: list((r.get("facets") or {}).keys()), False),
]


def walk(node, path=""):
    """Every `enum` in the document, with the path that reaches it."""
    if isinstance(node, dict):
        if isinstance(node.get("enum"), list):
            yield path, node["enum"]
        for k, v in node.items():
            yield from walk(v, f"{path}/{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, f"{path}/{i}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    rubric = yaml.safe_load(open(RUBRIC, encoding="utf-8"))
    expected = {}
    for label, marker, get, enforced in VOCABULARIES:
        vals = [v for v in (get(rubric) or []) if v]
        if vals:
            expected[marker] = (label, vals, enforced)

    print(f"rubric {rubric.get('schema_version')} — vocabularies to check:")
    for marker, (label, vals, enforced) in expected.items():
        print(f"  {label:<22} {'enforced' if enforced else 'advisory'}  {vals}")
    print()

    problems, checked = [], 0
    for f in sorted(glob.glob(os.path.join(SPECS, "*"))):
        try:
            doc = yaml.safe_load(open(f, encoding="utf-8"))
        except Exception:                                              # noqa: BLE001
            continue
        if not isinstance(doc, dict):
            continue
        for path, enum in walk(doc):
            for marker, (label, vals, enforced) in expected.items():
                if marker not in enum:
                    continue
                checked += 1
                missing = [v for v in vals if v not in enum]
                extra = [v for v in enum if v not in vals]
                if missing or extra:
                    problems.append((os.path.basename(f), path, label, missing, extra, enforced))

    print(f"  published enums checked   {checked}")
    print(f"  DISAGREE with the rubric  {len(problems)}\n")
    for fname, path, label, missing, extra, enforced in problems:
        print(f"  {fname}")
        print(f"    {path}  [{label}{'' if enforced else ' — ADVISORY'}]")
        if missing:
            # The dangerous direction, but only where the rubric IS the served vocabulary. For an
            # advisory row the rubric and the endpoint disagree, so "a client would reject this"
            # would be claiming more than is known.
            why = ("<- a client validating this REJECTS a real response" if enforced
                   else "<- in the rubric; the endpoint may not serve them (see the note in this file)")
            print(f"      MISSING  {missing}   {why}")
        if extra:
            print(f"      EXTRA    {extra}   <- documented but never served")
    if not problems:
        print("  every published vocabulary matches the rubric")
    hard = [p for p in problems if p[5]]
    if problems and not hard:
        print("\n  (all advisory — nothing a client would reject)")
    return 1 if (a.strict and hard) else 0


if __name__ == "__main__":
    sys.exit(main())
