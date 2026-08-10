# discover-mcp-servers

**Description:** Find providers in the apis.io catalog that publish a public MCP server, so you can plug real tools into an agent.

## When to use this skill

Use when the user wants agent-ready tools: "which of these vendors has an MCP server", "find MCP servers for payments", "what can I plug into my agent". MCP servers are the fastest path from catalog to working agent tools.

## The v1 API

Base URL: `https://apis.io/api/v1`. All **free**. MCP is a first-class artifact type in the catalog.

| Step | Call | Why |
|---|---|---|
| 1. Browse MCP | `GET /mcp?q=<capability>` | All catalogued MCP servers (rich records), filterable by text/tags/providers. |
| 2. Per provider | `GET /providers/{slug}/artifacts` | Confirm a specific provider publishes an `MCP` artifact. |
| 3. Inline | `GET /mcp?providers={slug}&include=content` | Fetch the MCP server card / manifest body. |

MCP equivalents: `find_artifacts` with `type: "mcp"`, `get_provider_artifacts`.

## Recipe

```bash
# 1. MCP servers for a capability
curl -s "https://apis.io/api/v1/mcp?q=payments&limit=10" | jq '.data[] | {provider_slug,name,url}'

# 2. Does this provider ship one?
curl -s "https://apis.io/api/v1/providers/stripe/artifacts" | jq '.artifact_types | index("MCP") != null'

# 3. Pull the server card
curl -s "https://apis.io/api/v1/mcp?providers=stripe&include=content" | jq '.data[0].content'
```

## Output format (recommended)

For each MCP server found:
- Provider + server name
- Its endpoint / install URL
- What tools it exposes (from the manifest, if inlined)
- A one-line note on wiring it into the agent (endpoint, transport)

If a provider has no MCP server, say so and fall back to `integrate-provider` (raw REST).

## Related skills

- `find-api` — find the provider first, then check for an MCP server here.
- `assemble-api-stack` — assemble multiple MCP servers/skills into a full agent toolset.
