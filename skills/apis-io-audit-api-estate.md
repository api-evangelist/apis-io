# audit-api-estate

**Description:** Inventory, score, and gap a set of providers — what they publish, how they rate, and what they're missing.

> **Pro tier.** Comparison, gap, and rating endpoints require an apis.io Pro API key. See https://apis.io/developer/plans/.

## When to use this skill

Use to assess a portfolio: "audit the APIs we depend on", "how healthy is our vendor set", "where are the gaps across these providers". This produces an estate report — coverage, scores, and the highest-value gaps to close.

## The v1 API

Base URL: `https://apis.io/api/v1`. Send `x-api-key: <key>`.

| Step | Call | Why |
|---|---|---|
| 1. Compare | `GET /compare?providers=a,b,c` | Composite/band + artifact-coverage matrix across the set. |
| 2. Gaps | `GET /gaps?providers=a,b,c` | Per-provider high-value gaps (MCP, Arazzo, Rules, Skills…) + stack-level gaps. |
| 3. Scores | `GET /ratings` / `GET /providers/{slug}/rating` | Anchor each provider's quality. |
| 4. Vertical | `GET /gaps/industry/{slug}` | What the whole industry commonly lacks (context for your gaps). |

MCP equivalents: `compare_providers`, `gap_analysis`, `find_ratings`, `get_provider_rating`, `industry_gap_analysis`. Or run the `audit_api_estate` prompt.

## Recipe

```bash
# 1. Coverage + score matrix
curl -s -H "x-api-key: $APISIO_KEY" \
  "https://apis.io/api/v1/compare?providers=twilio,sendgrid,stripe" | jq '{best_overall,artifact_matrix}'

# 2. Gaps across the estate
curl -s -H "x-api-key: $APISIO_KEY" \
  "https://apis.io/api/v1/gaps?providers=twilio,sendgrid,stripe" | jq '.stack.valuable_missing'
```

## Output format (recommended)

An estate report:
1. A coverage + score table (provider × artifact type, with band).
2. The top 3 gaps to close across the estate, most valuable first.
3. Strongest and weakest provider, with why — and any single-vendor risk.

## Related skills

- `shortlist-vendors` — when a gap means finding a replacement.
- `track-api-changes` — monitor the estate over time after the audit.
