#!/usr/bin/env node
// Rebuild apis.yml so each per-tag contract is indexed as its own API.
//
// Before: specificationVersion 0.19, ONE api entry ("APIs.io Search API") carrying all 62
// operations and 16 properties — so every consumer, report, and rating saw one
// undifferentiated blob. After: 0.21, eleven entries, one per tag, each pointing at its own
// self-contained OpenAPI from scripts/split-openapi.mjs.
//
// Properties that are genuinely shared across all eleven (docs, MCP, skills, Postman,
// status, rate limits, schemas) move to `common` — that is what common is for — rather than
// being copied eleven times. Each api entry then carries only what is actually its own: its
// OpenAPI contract. The two X-NaftikoCapability properties are dropped; Naftiko was purged
// from apis.io on 2026-06-23 and they have been dangling since.
//
//   node scripts/rebuild-apis-yml.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse, stringify } from 'yaml';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const RAW = 'https://raw.githubusercontent.com/api-evangelist/apis-io/refs/heads/main';
const doc = parse(readFileSync(join(ROOT, 'apis.yml'), 'utf8'));
const manifest = JSON.parse(readFileSync(join(ROOT, 'openapi', 'split-manifest.json'), 'utf8'));
const source = parse(readFileSync(join(ROOT, 'openapi', 'apis-io-v1-openapi.yml'), 'utf8'));
const tagDesc = Object.fromEntries((source.tags ?? []).map((t) => [t.name, t.description]));

const old = doc.apis[0];
const props = old.properties ?? [];
const byType = (t) => props.filter((p) => p.type === t);

// Naftiko was purged from apis.io in June; these two properties point at capabilities/ files
// that are no longer part of this API. Dropping them rather than carrying them into 0.21.
const dropped = byType('X-NaftikoCapability');

// Shared across every tag surface — these describe the APIs.io API as a whole, not any one
// tag, so they belong in common. Skip types common already declares (Authentication,
// ChangeLog, Plans) so the move doesn't introduce duplicates.
const commonTypes = new Set((doc.common ?? []).map((p) => p.type));
const SHARE = ['Documentation', 'MCPServer', 'MCPServerCard', 'AgentSkills', 'PostmanCollection', 'StatusPage', 'RateLimits', 'JSONSchema'];
const moved = [];
for (const type of SHARE) {
  for (const p of byType(type)) {
    if (commonTypes.has(type)) continue; // already covered in common
    moved.push(p);
  }
}

doc.specificationVersion = '0.21';
doc.modified = new Date().toISOString().slice(0, 10);
doc.common = [...(doc.common ?? []), ...moved];

// One entry per tag, in the manifest's (source-declared) tag order.
doc.apis = manifest.map((m) => ({
  aid: `apis-io:${m.slug}`,
  name: `APIs.io ${m.tag} API`,
  description: `${tagDesc[m.tag] ?? ''} ${m.operations} operation${m.operations === 1 ? '' : 's'} of the APIs.io API, split out by tag so this surface is documented, rated, and governed on its own.`.trim(),
  humanURL: old.humanURL,
  baseURL: old.baseURL,
  tags: old.tags,
  // Each surface points at its own contract AND the ruleset it is governed by, so
  // "what rules apply to this API?" is answerable from the index without reading a README.
  properties: [
    { type: 'OpenAPI', url: `${RAW}/${m.file}` },
    { type: 'SpectralRules', url: `${RAW}/rules/apis-io-spectral-rules.yml` },
  ],
}));

// Make the governance run itself discoverable from the index rather than only on disk.
if (!doc.common.some((p) => p.type === 'X-GovernanceReport')) {
  doc.common.push({ type: 'X-GovernanceReport', url: `${RAW}/governance/README.md`, name: 'Governance runs, reports, and rule coverage' });
}

writeFileSync(join(ROOT, 'apis.yml'), stringify(doc, { lineWidth: 120 }));

console.log(`apis.yml rebuilt:`);
console.log(`  specificationVersion 0.19 -> ${doc.specificationVersion}`);
console.log(`  apis: 1 -> ${doc.apis.length} (one per tag, ${manifest.reduce((n, m) => n + m.operations, 0)} operations total)`);
console.log(`  moved to common: ${moved.length} shared propert${moved.length === 1 ? 'y' : 'ies'} (${[...new Set(moved.map((p) => p.type))].join(', ')})`);
console.log(`  dropped: ${dropped.length} stale X-NaftikoCapability`);
console.log(`  common now: ${doc.common.length} properties`);
