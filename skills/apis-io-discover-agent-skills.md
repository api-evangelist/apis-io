---
name: discover-agent-skills
description: Search the apis.io catalog for Agent Skills published by API providers — packaged SKILL.md files you can adopt directly. Use when the user wants ready-made skills for a vendor or capability rather than writing integration code.
license: CC-BY-NC-SA-4.0
---

# discover-agent-skills

apis.io indexes the Agent Skills that API providers publish across the network. Before you
write a skill for a vendor, check whether they already ship one.

## When to use this skill

Use for "is there a skill for Stripe", "find agent skills for analytics", "what skills can I
drop into my agent", or as the first move before hand-writing provider integration logic.
For MCP servers instead, use `discover-mcp-servers`.

## The call

```
GET https://apis.io/api/v1/skills
```

**Free**, no key. Standard envelope, standard filters (`q`, `tags`, `providers`, `limit`,
`page`). Each record:

```json
{ "type": "AgentSkill",
  "slug": "7-powers-analysis",
  "name": "7-powers-analysis",
  "provider_slug": "amplitude",
  "provider_name": "Amplitude",
  "description": "Analyze a business, product, or feature using Hamilton Helmer's 7 Powers framework...",
  "tags": [],
  "url": "https://github.com/amplitude/builder-skills/blob/main/product-skills/skills/7-powers/SKILL.md" }
```

`url` points at the provider's own SKILL.md — usually on GitHub. That is the file to read
and adopt.

## Recipe

```bash
# How many skills does the catalog hold?
curl -s "https://apis.io/api/v1/skills?limit=1" | jq '.meta.total'

# Skills for a capability
curl -s "https://apis.io/api/v1/skills?q=analytics&limit=10" \
  | jq '[.data[] | {provider_slug, name, url}]'

# Does this vendor ship any?
SLUG=$(curl -s "https://apis.io/api/v1/resolve?identifier=amplitude.com" | jq -r .slug)
curl -s "https://apis.io/api/v1/skills?providers=$SLUG" \
  | jq '{n: .meta.total, skills: [.data[] | {name, description, url}]}'

# Read one before recommending it — GitHub blob URLs need the raw form
curl -s "$(curl -s "https://apis.io/api/v1/skills?providers=amplitude&limit=1" \
  | jq -r '.data[0].url' \
  | sed 's|github.com|raw.githubusercontent.com|; s|/blob/|/|')" | head -60
```

MCP equivalent (`https://apis.io/mcp`): `find_skills`.

## Read the skill before you recommend it

A catalog entry means the file exists, not that it is good or current. Fetch the raw
SKILL.md and check:

- **Frontmatter** — a valid `name` and `description`. Without them it will not load as an
  Agent Skill in most runtimes.
- **What it actually calls** — a skill that hardcodes a base URL or a deprecated endpoint
  will fail silently in an agent loop.
- **Auth expectations** — does it assume an env var, an OAuth flow, a key you don't have?
- **Provenance** — cross-check with `/providers/{slug}/evidence`. `provenance.skills` of
  `first-party` means the provider published it; `derived` means apis.io inferred it.

## Browsing surface

The rendered index of provider skills, with per-skill and per-provider pages, is at
https://apis.io/agent-skills/. apis.io's own skills are a separate set at
https://apis.io/skills/ with a manifest at
https://apis.io/.well-known/agent-skills/index.json.

## Output format

For each skill: provider, skill name, one line on what it does, the raw SKILL.md URL, and
whether it is first-party. Close with whether adopting beats writing your own — if the
published skill is thin or stale, say so and fall back to `integrate-provider`.

## Related skills

- `discover-mcp-servers` — the server-shaped sibling.
- `agent-readiness-scan` — the full agent picture for one provider.
- `find-artifact` — every other artifact type.
- `verify-provenance` — first-party vs derived.
