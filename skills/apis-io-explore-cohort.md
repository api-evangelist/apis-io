---
name: explore-cohort
description: Explore any slice of the API market as a scored cohort — an industry, topic area, region, or tag — with its members, their Kin Scores and agent readiness. Use to size a market, find the leaders in a category, or research a sector.
license: CC-BY-NC-SA-4.0
---

# explore-cohort

A cohort is any slice of the catalog treated as a scored group: an industry, an API
Evangelist topic area, a region, or a tag. This is how you research a market rather than a
single vendor.

## When to use this skill

Use for "who leads the fintech API market", "how mature is healthcare", "size the observability
space", "what's the state of APIs in Germany", or as the research spine behind a report.

## The cohort space — free

```bash
curl -s "https://apis.io/api/v1/cohorts?limit=5" | jq '{n: .meta.total, sample: [.data[] | {kind, slug, name, member_count: .provider_count}]}'
```

Four kinds, filterable with `kind=`:

| Kind | Roughly | What it is |
|---|---|---|
| `tag` | ~13,700 | Topic tags — the long tail. |
| `area` | ~77 | API Evangelist practice areas. |
| `industry` | ~72 | Business verticals. |
| `region` | ~17 | Geographies. |

Read `meta.total` for live counts.

```bash
curl -s "https://apis.io/api/v1/cohorts?kind=industry&limit=100" \
  | jq -r '.data[] | "\(.slug)\t\(.provider_count)"'
```

## One cohort, in full — free

```
GET https://apis.io/api/v1/cohorts/{kind}/{slug}
```

```bash
curl -s "https://apis.io/api/v1/cohorts/industry/artificial-intelligence" \
  | jq '{name, description, tier, sufficient, member_count,
         top: [.members[:10][] | {slug, name, kin_score, band, agent_readiness}]}'
```

Every member arrives scored:

```json
{ "slug": "convertkit", "name": "Kit", "kin_score": 85.4,
  "band": "exemplar", "agent_readiness": 58.8 }
```

This is the **cheapest scored data in the catalog** — a full member roster with Kin Scores
and agent readiness, free, in one call. Large cohorts return thousands of members, so page
or slice client-side rather than printing the array.

### Three fields to read before you analyze

- **`tier`** — `data` or `report`. A `report`-tier cohort has no rolled-up `band` or
  `composite` of its own (both `null`); score it yourself from `members[].kin_score`.
- **`sufficient`** — whether the cohort has enough members to say anything. If `false`, say
  so instead of reporting a number.
- **`member_count` vs `declared_member_count`** — a gap means members were declared but not
  resolved into the catalog.

### `parts` — the Pro sub-resources

The response carries a `parts` object pointing at four gated sub-resources:

```json
{ "stats": "/v1/cohorts/{kind}/{slug}/stats",
  "rankings": "/v1/cohorts/{kind}/{slug}/rankings",
  "scores": "/v1/cohorts/{kind}/{slug}/scores",
  "capabilities": "/v1/cohorts/{kind}/{slug}/capabilities" }
```

All return **402** without a Pro key, as does `/cohorts/compare`. The free member roster
already lets you compute a median, a leaderboard, and a band distribution yourself.

## Recipe — score a market from free data

```bash
COHORT=industry/artificial-intelligence

curl -s "https://apis.io/api/v1/cohorts/$COHORT" | python3 -c "
import json,sys,statistics as st
d=json.load(sys.stdin)
m=[x for x in d['members'] if x.get('kin_score') is not None]
print(f\"{d['name']}: {d['member_count']} members, {len(m)} scored\")
print('median kin_score:', round(st.median([x['kin_score'] for x in m]), 1))
ar=[x['agent_readiness'] for x in m if x.get('agent_readiness') is not None]
print('median agent_readiness:', round(st.median(ar), 1) if ar else 'n/a')
from collections import Counter
print('bands:', dict(Counter(x['band'] for x in m).most_common()))
print('top 5:', [(x['name'], x['kin_score']) for x in sorted(m, key=lambda y: -y['kin_score'])[:5]])"
```

MCP equivalents (`https://apis.io/mcp`): `find_cohorts`, `get_cohort`, `cohort_stats`,
`cohort_rankings`, `cohort_scores`, `cohort_capabilities`, `compare_cohorts` (the last five
Pro). Related free surfaces: `find_industries`, `find_areas`, `find_regions`, `find_tags`,
and the `get_*_leaders` endpoints.

## Output format

1. **The cohort** — name, what it covers, member count, and whether `sufficient` is true.
2. **Distribution** — median Kin Score and the band spread. A market where 80% sits in
   `thin` is a different story from one with a long exemplar tail.
3. **Leaders** — the top members with scores.
4. **Agent readiness** — the median, and how it diverges from the quality median. The gap
   between the two is usually the most interesting sentence in the analysis.
5. **Caveats** — `tier: report` means no rolled-up composite; say you computed it yourself.

## Errors

`/cohorts` and `/cohorts/{kind}/{slug}` are free. The `parts` sub-resources and
`/cohorts/compare` return 402 with `error`, `detail`, `tier`, `plans`. Compute what you can
from the free roster, label it as your own computation, and surface the upgrade link for the
rest.

Note: `/cohorts` is not in the published OpenAPI contract. Verify shapes against a live
response rather than the spec.

## Related skills

- `benchmark-against-peers` — one provider inside a cohort.
- `company-readiness` — the demand side of the same market.
- `search-apis` — find the tag or industry slug first.
