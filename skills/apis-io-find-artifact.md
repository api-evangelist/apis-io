---
name: find-artifact
description: Search the apis.io catalog for any artifact type beyond OpenAPI — Arazzo workflows, Spectral rules, pricing plans, FinOps, rate limits, GraphQL, Postman collections, JSON Schemas, examples, and more. Use when the user wants governance, commercial, or workflow artifacts rather than an API contract.
license: CC-BY-NC-SA-4.0
---

# find-artifact

The catalog profiles far more than OpenAPI. This is the door to every other artifact type.

## When to use this skill

Use for "who publishes Spectral rules", "find Arazzo workflows for payments", "which APIs
document their rate limits", "show me pricing plans I can parse", "find JSON Schemas for
invoices". For the API contract itself use `fetch-api-spec`.

## One endpoint shape, many types

Base `https://apis.io/api/v1`. Each artifact type is its own collection endpoint sharing the
standard envelope — `{ "meta": {...}, "data": [...] }` — and the same filters:
`q`, `tags`, `providers`, `limit`, `page`.

| Endpoint | What it holds | Tier |
|---|---|---|
| `/openapis` | OpenAPI contracts | free |
| `/asyncapis` | AsyncAPI event contracts | free |
| `/graphql` | GraphQL schemas | free |
| `/postman` | Postman collections | free |
| `/collections` | API collections | free |
| `/arazzo` | Arazzo workflow definitions | free |
| `/rules` | Spectral governance rulesets | free |
| `/plans` | Machine-readable pricing plans | free |
| `/finops` | FinOps / cost artifacts | free |
| `/rate-limits` | Documented rate limits | free |
| `/json-schemas` | JSON Schema definitions | free |
| `/json-structures` | JSON Structure definitions | free |
| `/json-ld` | JSON-LD vocabularies | free |
| `/examples` | Request/response examples | free |
| `/apis-json` | APIs.json self-descriptions | free |
| `/channels` | Event channels | free |
| `/mcp` | MCP servers — see `discover-mcp-servers` | free |
| `/skills` | Agent Skills — see `discover-agent-skills` | free |
| `/scopes` | OAuth scopes | **Pro** |
| `/security` | Security artifacts | **Pro** |

Read `meta.total` for scale rather than hardcoding counts — every one of these moves with
each catalog build.

## Recipe

```bash
# How much of this artifact type exists at all?
curl -s "https://apis.io/api/v1/arazzo?limit=1" | jq '.meta.total'

# Scoped to a capability
curl -s "https://apis.io/api/v1/rules?q=governance&limit=10" \
  | jq '[.data[] | {provider_slug, name, url}]'

# Everything one provider publishes of a type
curl -s "https://apis.io/api/v1/plans?providers=twilio" \
  | jq '{n: .meta.total, plans: [.data[] | {name, url}]}'

# Fetch the artifact body itself — the URLs are public raw files
curl -s "https://apis.io/api/v1/rules?q=openapi&limit=1" \
  | jq -r '.data[0].url' | xargs -r curl -s | head -40
```

### `include=content`

Some endpoints accept `?include=content` to inline the artifact body. It works for
machine-readable artifacts (OpenAPI, AsyncAPI, rules). When the artifact is an HTML page the
API declines and tells you why:

```json
{ "content_skipped": "not_machine_readable",
  "content_hint": "HTML/doc page — fetch the url directly, or pass artifact_types to force inlining." }
```

Check for `content_skipped` before reading `content`, and fall back to fetching `url`.

## Finding out what a provider has before you go looking

One call lists every type a provider publishes — cheaper than probing endpoint by endpoint:

```bash
curl -s "https://apis.io/api/v1/providers/twilio/artifacts" | jq '.artifact_types'
# ["APIsJSON","AgentSkill","AgenticAccess","Arazzo","AsyncAPI","Authentication","CLI",
#  "ChangeLog","Documentation","FinOps","GraphQL","LLMsTxt","MCP","OpenAPI","Plans", ...]
```

`by_type_counts` in the same response tells you how many of each.

MCP equivalents (`https://apis.io/mcp`): `find_arazzo`, `find_rules`, `find_plans`,
`find_finops`, `find_rate_limits`, `find_graphql`, `find_postman`, `find_collections`,
`find_examples`, `find_json_schemas`, `find_json_structures`, `find_json_ld`,
`find_channels`, `find_apis_json`, `find_scopes`, `find_security`, `get_provider_artifacts`.

## Output format

Group by provider, and for each artifact give the name, the fetchable `url`, and one line on
what it's for. When the user asked a "who does this well" question, sort by provider band
using `/resolve?identifier=<slug>` — it returns `band` free.

## Errors

`/scopes` and `/security` return HTTP 402 with `error`, `detail`, `tier`, `plans`. Surface
the upgrade link; don't retry, and don't substitute a guess for the gated data.

## Related skills

- `discover-apis-io` — conventions.
- `fetch-api-spec` — the API contract specifically.
- `discover-mcp-servers` · `discover-agent-skills` — the two agent-facing types.
- `verify-provenance` — whether an artifact is first-party or derived.
