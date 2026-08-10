# find-api

**Description:** Find the right API for a task — search the apis.io catalog, inspect the best candidates, and recommend one with its spec and links.

## When to use this skill

Use when the user says "find an API to do X", "what should I use for Y", or "is there an API for Z". This turns a fuzzy need into a concrete, ranked recommendation grounded in the catalog — not a web guess.

## The v1 API

Base URL: `https://apis.io/api/v1`. All endpoints here are **free**. Responses are JSON with a `data` array and pagination.

| Step | Call | Why |
|---|---|---|
| 1. Search | `GET /search?q=<task>&return=apis` (and `&return=providers`) | Ranked matches, quality-weighted. |
| 2. Inspect | `GET /apis/{aid}` | Full detail for a candidate (aid = `provider:api-slug`). |
| 3. Artifacts | `GET /apis/{aid}/artifacts` | What the API publishes (OpenAPI, auth, pricing, MCP…). |
| 4. More like it | `GET /apis/{aid}/similar` | Alternatives by shared tags. |

MCP equivalents (server `https://apis.io/mcp`): `apis_io_search`, `get_api`, `get_api_artifacts`, `find_similar_apis`. Or start from the `find_api` prompt.

## Recipe

```bash
# 1. Search for candidates
curl -s "https://apis.io/api/v1/search?q=send+sms&return=apis&limit=5" | jq '.data[] | {aid,name,provider_slug}'

# 2. Inspect the top pick
curl -s "https://apis.io/api/v1/apis/twilio:programmable-messaging" | jq '{name,description,properties:[.properties[].type]}'

# 3. See alternatives before committing
curl -s "https://apis.io/api/v1/apis/twilio:programmable-messaging/similar?limit=5" | jq '.data[] | {aid,name}'
```

## Output format (recommended)

Recommend ONE API, then list 2 alternatives:
- API name + provider, one-line what-it-does
- Its apis.io URL and OpenAPI URL (from step 2/3)
- Why it's the pick over the alternatives (coverage, rating, fit)

Be decisive — the point of this skill is a recommendation, not a link dump.

## Related skills

- `search-apis` — lighter keyword search over the catalog linkset.
- `integrate-provider` — once you've picked, onboard the provider end-to-end.
- `fetch-api-spec` — pull the chosen API's OpenAPI for parsing.
