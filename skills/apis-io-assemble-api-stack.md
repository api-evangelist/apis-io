# assemble-api-stack

**Description:** Design a capability stack from the catalog and export it as an adoptable APIs.json a team can commit.

> **Pro tier.** The design/export endpoints below require an apis.io Pro API key. The free preview returns the top pick per capability only. See https://apis.io/developer/plans/.

## When to use this skill

Use when the user needs more than one API: "design an API stack for a payments team", "what should acme.com's integration stack be", "assemble the tools my agent needs". This decomposes a domain into capabilities and returns a scored provider per capability, exportable.

## The v1 API

Base URL: `https://apis.io/api/v1`. Send your key as `x-api-key: <key>`.

| Step | Call | Tier | Why |
|---|---|---|---|
| 1. Design | `GET /stack?capabilities=payments,email,identity&region=europe` | free preview / pro full | Best provider per capability; pro adds alternatives + per-pick gaps. |
| 2. Export | `GET /stack/export?capabilities=payments,email,identity` | pro | The stack as an adoptable APIs.json + Arazzo hint. |

MCP equivalents: `recommend_stack` (free preview / pro full), `export_stack` (pro). Or run the `design_api_stack` / `build_agent_toolset` prompts.

## Recipe

```bash
# 1. Decompose the domain into capabilities, then design
curl -s -H "x-api-key: $APISIO_KEY" \
  "https://apis.io/api/v1/stack?capabilities=payments,email,identity,observability&region=europe" \
  | jq '.stack[] | {capability,top:.top.name,alternatives:[.alternatives[]?.name]}'

# 2. Export the chosen stack as APIs.json
curl -s -H "x-api-key: $APISIO_KEY" \
  "https://apis.io/api/v1/stack/export?capabilities=payments,email,identity" \
  | jq '.apis_json' > stack.apis.json
```

## Output format (recommended)

1. The capability breakdown you used.
2. A per-capability table: top pick, score/band, one alternative, the tradeoff.
3. The exported `apis.json` (offer to write it to a file), plus the Arazzo hint for chaining the providers into a workflow.

Be decisive — recommend a stack, then show the export.

## Related skills

- `shortlist-vendors` — go deep on a single capability instead of a whole stack.
- `discover-mcp-servers` — add MCP servers/skills for the chosen providers.
- `audit-api-estate` — score and gap an existing stack.
