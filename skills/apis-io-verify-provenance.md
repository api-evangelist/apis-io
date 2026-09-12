---
name: verify-provenance
description: Check where an apis.io provider record's evidence came from — which artifacts the provider published first-party versus which apis.io derived — before citing a score or an artifact as fact. Use when accuracy matters, or when a provider disputes their rating.
license: CC-BY-NC-SA-4.0
---

# verify-provenance

A catalog entry can mean two very different things: *the provider published this*, or
*apis.io inferred this*. This skill tells you which, so you never present a derived artifact
as something a vendor ships.

## When to use this skill

Use before citing an apis.io score or artifact as evidence, when a provider disputes their
rating, when a decision rests on "they publish X", and any time you're about to tell someone
a vendor has an MCP server or an agent skill.

## The call

```
GET https://apis.io/api/v1/providers/{slug}/evidence
```

**Free**, no key.

```json
{ "slug": "twilio", "name": "Twilio",
  "scored_at": "2026-08-21",
  "rubric_version": "0.12.0",
  "provenance": {
    "mcp": "first-party",
    "skills": "first-party",
    "agentic_access": "derived",
    "conformance": "derived",
    "contracts": { "total": 115, "derived": 0, "marker_coverage": 0, "callable": 100 } },
  "legend": {
    "first-party": "Published by the provider on their own domain.",
    "verified": "Fetched and confirmed by the scorer.",
    "derived": "Inferred from other artifacts rather than declared by the provider." },
  "rubric": "/v1/ratings/rubric" }
```

## Reading it

| Value | What you may say | What you may not say |
|---|---|---|
| `first-party` | "Twilio publishes an MCP server." | — |
| `verified` | "apis.io fetched and confirmed this." | — |
| `derived` | "apis.io inferred this from their other artifacts." | "They publish this." |

The `contracts` block is the one to read closely:

- **`total`** — contracts profiled for this provider.
- **`derived`** — how many apis.io generated rather than the provider publishing them. A
  high ratio means the OpenAPIs are reconstructions, not the vendor's own files.
- **`callable`** — how many resolve to a live, reachable service. A contract that is present
  but not callable describes something you cannot actually invoke.
- **`marker_coverage`** — how much of the contract carries provenance markers.

`scored_at` and `rubric_version` date the whole record. A score from an older rubric version
is not comparable to a current one — say which version you're quoting.

## Recipe

```bash
SLUG=$(curl -s "https://apis.io/api/v1/resolve?identifier=twilio.com" | jq -r .slug)

curl -s "https://apis.io/api/v1/providers/$SLUG/evidence" \
  | jq '{scored_at, rubric_version,
         first_party: [.provenance | to_entries[] | select(.value=="first-party") | .key],
         derived:     [.provenance | to_entries[] | select(.value=="derived")     | .key],
         contracts: .provenance.contracts}'

# What the rubric version means
curl -s "https://apis.io/api/v1/ratings/rubric" \
  | jq '{schema_version, last_updated, checks_total, bands}'
```

MCP equivalent (`https://apis.io/mcp`): `get_provider_evidence`.

## Using it in a dispute

When a provider says their score is wrong, this endpoint is the honest starting point:

1. Pull the evidence and read `scored_at` — the finding may predate a fix they shipped.
2. Separate `first-party` from `derived`. If a facet scored on derived evidence, that is a
   fair thing for them to contest.
3. Check `contracts.callable` against `contracts.total` — unreachable contracts are often
   the real complaint.
4. Quote `rubric_version` and the matching `/ratings/rubric` so both sides argue the same
   rubric.

Report what the endpoint says. Don't defend or attack the score — hand over the evidence and
the rubric, and let the numbers carry it.

## Output format

- **Scored** — `scored_at` and `rubric_version`.
- **First-party** — what the provider actually publishes.
- **Derived** — what apis.io inferred, flagged plainly.
- **Contracts** — total, derived, callable, as a ratio.
- **Confidence** — one line on how much weight this record can bear.

## Related skills

- `score-my-api` — the score this is the evidence for.
- `agent-readiness-scan` — leans on the same provenance fields.
- `resolve-provider` — get the slug first.
