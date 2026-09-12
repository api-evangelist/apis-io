---
name: agent-readiness-scan
description: Check whether an API provider is ready for autonomous AI agents — machine-readable contracts, MCP servers, agent skills, llms.txt, agent-native access controls, and the operational signals an agent needs. Use when asked if an API is agent-ready, or to compare providers on agent readiness.
license: CC-BY-NC-SA-4.0
---

# agent-readiness-scan

Agent Readiness is a standalone apis.io score, separate from the Kin Score quality
composite. It asks a narrower question: **can an autonomous agent drive this API without a
human papering over the gaps?**

## When to use this skill

Use for "is this API agent-ready", "can my agent use Stripe safely", "which of these vendors
is built for agents", or before wiring any provider into an autonomous workflow.

## The rubric — free

```bash
curl -s "https://apis.io/api/v1/ratings/rubric" | jq '.agent_readiness'
```

Free, no key. It returns the schema version, the dimensions, the points total, and the four
bands:

| Band | Meaning |
|---|---|
| `agent-native` | Built to be driven by agents, and the provider built it. ~1.7% of the catalog. |
| `agent-ready` | An agent can drive it, with care. |
| `agent-aware` | Some agent affordances, meaningful gaps. |
| `human-only` | Designed for a human developer reading docs. |

Cite the live rubric rather than these labels alone — the schema is versioned and moves.

## The free scan

`GET /providers/{slug}/agent-readiness` is **Pro** (402). You can still assemble a solid,
honest scan entirely from free calls — do this before reaching for the gated detail.

```bash
SLUG=$(curl -s "https://apis.io/api/v1/resolve?identifier=twilio.com" | jq -r .slug)

# 1. What agent-facing artifacts exist?
curl -s "https://apis.io/api/v1/providers/$SLUG/artifacts" \
  | jq '{types: .artifact_types,
         agent: [.artifact_types[] | select(. == "MCP" or . == "MCPServer"
                                         or . == "AgentSkill" or . == "LLMsTxt"
                                         or . == "AgenticAccess")]}'

# 2. Is there a real MCP server, and how do you install it?
curl -s "https://apis.io/api/v1/mcp?providers=$SLUG" \
  | jq '[.data[] | {name, url, install: .meta.install_method, description}]'

# 3. Packaged agent skills?
curl -s "https://apis.io/api/v1/skills?providers=$SLUG" \
  | jq '{n: .meta.total, skills: [.data[] | {name, url}]}'

# 4. Is the contract machine-readable and callable?
curl -s "https://apis.io/api/v1/providers/$SLUG/evidence" | jq '.provenance'

# 5. Overall quality band, free
curl -s "https://apis.io/api/v1/resolve?identifier=$SLUG" | jq '{band, composite}'
```

Step 4 is the one people skip and shouldn't. `provenance` tells you whether the agent
surface is **first-party** or merely **derived** by the scorer:

```json
{ "mcp": "first-party", "skills": "first-party",
  "agentic_access": "derived", "conformance": "derived",
  "contracts": { "total": 115, "derived": 0, "marker_coverage": 0, "callable": 100 } }
```

`derived` means apis.io inferred it, not that the provider published it. An agent surface
the provider never shipped is not something to plug into production.

## What to check, in order

1. **Machine-readable contract** — an OpenAPI/AsyncAPI that is present *and* callable
   (`provenance.contracts.callable`). No contract, no autonomy.
2. **A real agent surface** — MCP server or Agent Skill, marked `first-party`. Read the MCP
   record's `description`: the catalog also profiles **candidate** surfaces it derived, and
   says so in the text.
3. **Agent-native access control** — `AgenticAccess`, scopes granular enough that an agent
   gets least privilege rather than the owner's full key.
4. **Operational signals** — documented `RateLimits`, stable errors, idempotency. An agent
   that can't read rate-limit state can't back off.
5. **`LLMsTxt`** — a stated policy for machine consumers.

## Output format

A verdict, then the evidence:

- **Band** — from the rubric, with the reasoning.
- **Has** — the agent-facing artifacts, marked first-party or derived.
- **Missing** — the specific gaps, in the order above.
- **Verdict** — agent-ready / agent-ready-with-guardrails / human-only, and the one change
  that would move it most.

Never report a `derived` surface as something the provider ships. Say which is which — that
distinction is the whole point of the scan.

## Pro detail

`GET /providers/{slug}/agent-readiness` returns the scored per-dimension breakdown. On 402
the body carries `error`, `detail`, `tier`, `plans` — surface it, keep the free scan you
already built, and don't invent per-dimension numbers.

## Related skills

- `discover-mcp-servers` · `discover-agent-skills` — the two agent surfaces in depth.
- `verify-provenance` — first-party vs derived, in full.
- `score-my-api` — the broader quality score this sits beside.
- `integrate-provider` — once it passes, wire it up.
