---
name: benchmark-against-peers
description: Benchmark one API provider against its closest peers facet by facet — score, artifact coverage, and where it leads or trails. Use for competitive positioning or to justify an API investment. Pro tier, with a free fallback.
license: CC-BY-NC-SA-4.0
---

# benchmark-against-peers

Where a provider stands against the vendors it actually competes with — not against the
whole catalog.

## When to use this skill

Use for "how do we compare to Stripe", "who leads our category", "what do our competitors
publish that we don't", or to build the slide that justifies API investment. For a
capability-first buy decision use `shortlist-vendors`; for your own improvement plan use
`score-my-api`.

## Build the peer set — free

Don't guess competitors. The catalog derives them from tag, industry, and artifact overlap:

```bash
SLUG=$(curl -s "https://apis.io/api/v1/resolve?identifier=sendgrid.com" | jq -r .slug)

curl -s "https://apis.io/api/v1/providers/$SLUG/similar?limit=8" \
  | jq '[.data[] | {slug, name}]'
```

Add any competitor the user names by hand — declared rivals and catalog-derived peers are
rarely the same list, and the difference is itself worth reporting.

## Free benchmark

You can build a real comparison without a key. Do this first.

```bash
PEERS="sendgrid mailgun postmark"

# Band + composite for each — free via resolve
for p in $PEERS; do
  curl -s "https://apis.io/api/v1/resolve?identifier=$p" | jq -c '{slug, band, composite}'
done

# Artifact coverage matrix
for p in $PEERS; do
  curl -s "https://apis.io/api/v1/providers/$p/artifacts" \
    | jq -c '{slug, n: (.artifact_types | length), types: .artifact_types}'
done

# Agent surfaces
for p in $PEERS; do
  printf "%s mcp=" "$p"
  curl -s "https://apis.io/api/v1/mcp?providers=$p" | jq -r '.meta.total'
done

# How much of each record is first-party vs inferred
for p in $PEERS; do
  curl -s "https://apis.io/api/v1/providers/$p/evidence" | jq -c '{slug, provenance}'
done
```

That yields composite, band, artifact coverage, agent surface, and provenance across the
peer set — enough for a defensible benchmark.

## Pro depth

| Call | Adds |
|---|---|
| `GET /compare?providers=a,b,c` | Facet leaders and the artifact matrix, computed. |
| `GET /providers/{slug}/rating` | The per-facet breakdown behind each composite. |
| `GET /gaps?providers=a,b,c` | The high-value gaps per provider and across the set. |
| `GET /ratings/movers` | Who is improving and who is slipping. |

Send `x-api-key: <key>`.

```bash
curl -s -H "x-api-key: $APISIO_KEY" \
  "https://apis.io/api/v1/compare?providers=sendgrid,mailgun,postmark" | jq 'keys'
```

Inspect `keys` before assuming field paths — the gated response shapes are not pinned in the
published OpenAPI.

MCP equivalents (`https://apis.io/mcp`): `find_similar_providers`, `resolve`,
`get_provider_artifacts`, `get_provider_evidence`, `compare_providers` (Pro),
`get_provider_rating` (Pro), `gap_analysis` (Pro). Or run the `benchmark_against_peers` prompt.

## Weight the comparison honestly

- Compare against the **rubric's** facet weights, not your own priorities —
  `GET /ratings/rubric` gives `facet_weights`, free. `contract_quality` at 0.25 moves a
  benchmark far more than `discoverability` at 0.10.
- Check `scored_at` on each `evidence` record. Providers are scored on different dates, and
  a stale record is not a fair loss.
- Separate first-party from derived. "They publish an MCP server" and "apis.io inferred one"
  are different competitive facts.
- Note where the peer set is thin. Two comparable providers is an anecdote, not a benchmark.

## Errors and tiering

Gated calls return HTTP **402**:

```json
{ "error": "upgrade_required", "detail": "...", "tier": "pro",
  "plans": "https://apis.io/developer/plans/" }
```

Surface `detail` and `plans`, fall back to the free benchmark above, and say which parts are
free-tier estimates. Never fabricate a facet breakdown you couldn't fetch.

## Output format

1. **The peer set** — who, and how they were derived.
2. **The table** — provider × (band, composite, artifact count, agent surface).
3. **Leads** — facets where the subject is ahead, with the evidence.
4. **Trails** — facets where it's behind, ranked by rubric weight.
5. **The one move** — the single highest-weight artifact a peer publishes and the subject
   doesn't.

## Related skills

- `score-my-api` — the improvement plan this feeds.
- `shortlist-vendors` — the buy-side version.
- `audit-api-estate` — a whole portfolio instead of one provider.
- `explore-cohort` — the scored market this peer set sits inside.
