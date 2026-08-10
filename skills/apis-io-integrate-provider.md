# integrate-provider

**Description:** Onboard a provider end-to-end — read its onboarding + OpenAPI from the catalog and produce concrete first-integration steps.

## When to use this skill

Use once a provider is chosen and the user wants to actually integrate: "how do I get started with Twilio", "wire up Stripe", "what's the first call". This assembles auth, base URLs, and the first operation into runnable steps.

## The v1 API

Base URL: `https://apis.io/api/v1`. All **free**.

| Step | Call | Why |
|---|---|---|
| 1. Onboarding | `GET /providers/{slug}/onboarding` | Website, signup, docs, authentication, base URLs, first steps. |
| 2. Artifacts | `GET /providers/{slug}/artifacts` | Everything the provider publishes; find its primary API. |
| 3. Spec | `GET /openapis/{aid}?include=content` | The primary OpenAPI, inlined — read the real operations. |

MCP equivalents: `get_provider_onboarding`, `get_provider_artifacts`, `get_openapi`. Or run the `integrate_provider` prompt with a `slug`.

## Recipe

```bash
# 1. Getting-started facts
curl -s "https://apis.io/api/v1/providers/twilio/onboarding" | jq '{signup,authentication,baseURLs,first_steps}'

# 2. Find the primary API to integrate
curl -s "https://apis.io/api/v1/providers/twilio/artifacts" | jq '.artifacts[] | select(.type=="OpenAPI") | .aid' | head -1

# 3. Read its operations
curl -s "https://apis.io/api/v1/openapis/twilio:programmable-messaging?include=content" | jq -r '.content' | head -40
```

## Output format (recommended)

Produce a short integration guide:
1. **Authenticate** — the scheme (API key / OAuth), where to get credentials (signup link).
2. **First call** — a concrete method + path + example from the OpenAPI, with the base URL filled in.
3. **Next** — which SDK, Postman collection, or MCP server to adopt (from the artifacts list).

Cite real operations from the spec — never invent endpoints.

## Related skills

- `find-api` — pick the provider/API first.
- `fetch-api-spec` — deeper spec parsing.
- `discover-mcp-servers` — if the provider ships an MCP server, plug that in instead of raw REST.
