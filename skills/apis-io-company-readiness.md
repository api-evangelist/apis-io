---
name: company-readiness
description: Read the demand side of the API market — what technologies a company is investing in, where it is thin, and which catalog providers are already in its stack. Use for account research, sales targeting, or to find where demand outruns supply.
license: CC-BY-NC-SA-4.0
---

# company-readiness

Most of apis.io describes **supply** — what providers publish. The insights surface
describes **demand** — what companies are actually hiring and building for, extracted from
job posts and company publications.

## When to use this skill

Use for "what is JP Morgan investing in", "who should we sell our API to", "where is demand
outrunning coverage", "what does this account already use". For the supply-side view of the
same market use `explore-cohort`.

## Find the company — free

```bash
curl -s "https://apis.io/api/v1/insights/companies?limit=5" \
  | jq '{n: .meta.total, sample: [.data[] | {slug, name, industry}]}'
```

Slugs are hyphenated: `jp-morgan-chase`, `goldman-sachs`. Filter with `q`.

## The profile — free preview

```
GET https://apis.io/api/v1/insights/company/{slug}
```

```json
{ "slug": "jp-morgan-chase", "name": "JP Morgan Chase",
  "industry": "Financial Technology", "sub_sector": "Payment Processing",
  "source": "jobs+blogs", "confidence": "high",
  "readiness_total": 1545,
  "top_dimensions": [ { "key": "data", "score": 176 },
                      { "key": "roiBusinessMetrics", "score": 97 },
                      { "key": "cloud", "score": 93 } ],
  "sample_gap": { "dimension": "domainSpecialization", "score": 1 },
  "quarters": [ "q2-2026", "q1-2026" ],
  "upgrade": "Preview is deliberately thin. Pro unlocks the full 40-dimension profile..." }
```

Read `source` and `confidence` before quoting any of it. `jobs+blogs` with `high` confidence
is a real signal; a thin source with low confidence is not something to build a pitch on.

`readiness_total` is a **volume** measure — the aggregate signal across dimensions. A big
company generates more signal than a small one, so compare dimensions *within* a company, or
compare companies of similar size. It is not a quality score and is not the Kin Score.

## The dimension space — free

```bash
curl -s "https://apis.io/api/v1/insights/dimensions" \
  | jq '[.data[] | {dimension, total_signal}]'
```

42 dimensions in the current quarter, each with total market signal — this is the map of
where the whole market is investing. Pair it with a company's `top_dimensions` to see where
that company is ahead of or behind its market.

## Adoption and industries — free

```bash
# What products companies actually run, with a Thoughtworks-style radar ring
curl -s "https://apis.io/api/v1/insights/adoption?limit=10" \
  | jq '[.data[] | {name, companyCount, radarRing}]'
# {"name":"Microsoft Office","companyCount":731,"radarRing":"Optimizing"}

# Demand by vertical
curl -s "https://apis.io/api/v1/insights/industries" | jq '[.data[] | {name, company_count}]'
```

## Pro depth

| Call | Adds |
|---|---|
| `GET /insights/company/{slug}/gaps` | The dimensions where the company is weakest — the openings. |
| `GET /insights/company/{slug}/match` | Catalog providers whose product is already in its stack. |

Both 402 without a Pro key. `/match` is the supply↔demand join — the answer to "who is
already inside this account".

MCP equivalents (`https://apis.io/mcp`): `find_company_insights`, `get_company_insight`,
`insights_dimensions`, `insights_adoption`, `entity_demand`, `company_gaps` (Pro),
`match_providers` (Pro). Or run the `company_readiness` / `demand_vs_supply` prompts.

## Demand vs supply

The most useful thing here is the join against the supply side:

```bash
# 1. Where is the market investing?
curl -s "https://apis.io/api/v1/insights/dimensions" | jq -r '.data[:10][] | "\(.dimension)\t\(.total_signal)"'

# 2. How well is that covered by the catalog?
curl -s "https://apis.io/api/v1/cohorts?kind=industry&limit=100" | jq -r '.data[] | "\(.slug)\t\(.provider_count)"'
```

High demand signal against thin provider coverage is a gap worth naming — for a product
decision, a story, or a market entry.

## Honesty rules

This data is **inferred from public signal**, not declared by the companies. Say so.

- Quote `source`, `confidence`, and the `quarters` covered whenever you cite a number.
- `readiness_total` compares dimensions within a company, not companies against each other
  unless they're comparable in size.
- Never present demand signal as a stated intent, a budget, or a commitment.
- The preview is deliberately thin. If the answer needs the full 40-dimension profile, say
  the preview can't support it rather than extrapolating from three dimensions.

## Output format

1. **The company** — industry, sub-sector, source, confidence.
2. **Where it's investing** — top dimensions with scores, read against the market's
   `insights/dimensions`.
3. **Where it's thin** — the `sample_gap`, or the full gaps list if you have Pro.
4. **Already inside** — providers in its stack, if you have `/match`.
5. **The opening** — one line on where a provider could sell in or partner, grounded in a
   named dimension.

## Related skills

- `explore-cohort` — the supply side of the same market.
- `score-my-api` — how a provider selling into these accounts rates.
- `resolve-provider` — insights slugs are company slugs, not provider slugs; resolve
  separately when crossing between the two.
