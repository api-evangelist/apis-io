---
name: score-my-api
description: Read a provider's apis.io quality score and the Kin Score rubric, then turn it into a ranked, do-this-next punch list of what to publish to move up a band. Use when someone wants to know how their own API rates and how to improve it.
license: CC-BY-NC-SA-4.0
---

# score-my-api

For the provider side of the catalog: what your API scores, why, and the shortest path to a
better band.

## When to use this skill

Use for "how does our API rate", "why is our score low", "what should we publish next",
"how do we get to exemplar". For comparing against named competitors use
`benchmark-against-peers`; for a whole vendor portfolio use `audit-api-estate`.

## Get the score — free

`GET /providers/{slug}/rating` is Pro. `/resolve` returns the headline number free:

```bash
curl -s "https://apis.io/api/v1/resolve?identifier=yourcompany.com" \
  | jq '{slug, name, band, composite}'
# {"slug":"twilio","name":"Twilio","band":"exemplar","composite":73.8}
```

## Get the rubric — free

```bash
curl -s "https://apis.io/api/v1/ratings/rubric"
```

Free, and it is the whole scoring model. Current schema `0.12.0`, **110 checks**.

**Bands** (`bands` / `band_detail`, with the share of the catalog in each):

| Band | Range | Share |
|---|---|---|
| Exemplar | 66.5+ | ~1.0% |
| Strong | 54.3 – 66.4 | ~3.8% |
| Developing | 39.3 – 54.2 | ~13.3% |
| Thin | 26.2 – 39.2 | ~15.9% |
| Emerging | 11 – 26.1 | — |
| Minimal | 0 – 10.9 | — |

Read the live values rather than this table — the bands are re-cut whenever the rubric adds
a dimension.

**Facet weights** (`facet_weights`, and `facet_detail` for what each measures):

| Facet | Weight |
|---|---|
| `contract_quality` | 0.25 |
| `developer_ergonomics` | 0.20 |
| `commercial_clarity` | 0.20 |
| `regulatory` | 0.15 (conditional — applies by industry) |
| `operational_transparency` | 0.13 |
| `governance` | 0.12 |
| `discoverability` | 0.10 |
| `open_source` | 0.10 |

Agent Readiness is scored **separately** — see `agent-readiness-scan`.

## Build the punch list — free

```bash
SLUG=$(curl -s "https://apis.io/api/v1/resolve?identifier=yourcompany.com" | jq -r .slug)

# 1. Score and band
curl -s "https://apis.io/api/v1/resolve?identifier=$SLUG" | jq '{band, composite}'

# 2. What you publish today
curl -s "https://apis.io/api/v1/providers/$SLUG/artifacts" \
  | jq '{types: .artifact_types, counts: .by_type_counts}'

# 3. What the scorer actually saw — and how much of it it had to infer
curl -s "https://apis.io/api/v1/providers/$SLUG/evidence" | jq '{scored_at, rubric_version, provenance}'

# 4. The rubric to map gaps against
curl -s "https://apis.io/api/v1/ratings/rubric" | jq '{facet_weights, facet_detail, checks_total}'

# 5. What comparable providers publish that you don't
curl -s "https://apis.io/api/v1/providers/$SLUG/similar?limit=5" | jq '[.data[].slug]'
```

Diff step 2 against the artifact types the step-5 providers publish. The types they have and
you don't, weighted by the facet each rolls up to, **is** the punch list.

## How to rank the work

Rank by *weight × effort*, not by weight alone:

1. **`contract_quality` (0.25)** — the heaviest facet. A complete OpenAPI with descriptions,
   examples, and error responses moves more points than anything else.
2. **`commercial_clarity` (0.20)** — machine-readable `Plans`, `Pricing`, `RateLimits`.
   Usually the cheapest real points on the board: the facts already exist on your pricing
   page, they just aren't parseable.
3. **`developer_ergonomics` (0.20)** — SDKs, examples, a working getting-started path.
4. **`discoverability` (0.10)** — an `apis.yml`/APIs.json and clean tagging. Small weight,
   near-zero effort, and it improves how every other artifact is found.
5. **`governance` (0.12)** — Spectral rules, a changelog, a lifecycle policy.
6. **`operational_transparency` (0.13)** — status, uptime, deprecation policy.

Check `provenance` from step 3 first. A facet scored on **derived** evidence means apis.io
inferred it because you didn't publish it — publishing the real artifact converts a derived
signal into a first-party one, which is often the single highest-value move available.

MCP equivalents (`https://apis.io/mcp`): `resolve`, `get_rating_rubric`,
`get_provider_artifacts`, `get_provider_evidence`, `find_similar_providers`,
`get_provider_rating` (Pro). Or run the `improve_my_score` prompt.

## Output format

1. **Where you stand** — band, composite, distance to the next band's floor, and what share
   of the catalog is above you.
2. **What you publish** — artifact types present, flagged first-party vs derived.
3. **The punch list** — ranked, each item naming the facet it lifts, its weight, and the
   concrete artifact to publish.
4. **The next band** — the two or three items that close the specific gap to it.

Be concrete. "Publish a machine-readable pricing plan at /plans.json" beats "improve
commercial clarity."

## Pro detail

`GET /providers/{slug}/rating` gives the scored per-facet breakdown, and
`/providers/{slug}/rating/history` the movement. Both 402 without a Pro key — surface
`detail` and `plans`, keep the free analysis, and never invent per-facet numbers.

## Related skills

- `verify-provenance` — first-party vs derived, in depth.
- `agent-readiness-scan` — the separate agent score.
- `benchmark-against-peers` — Pro, facet-by-facet against named competitors.
- `resolve-provider` — get the slug first.
