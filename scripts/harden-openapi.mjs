#!/usr/bin/env node
// Bring every published APIs.io contract up to the ruleset in
// rules/apis-io-spectral-rules.yml — deterministically, and re-runnably.
//
// The per-tag contracts in openapi/ are GENERATED (split from
// apis-io-v1-openapi.yml, then normalised to 3.2.0 by /refine-openapis). Hand
// edits to a generated file are lost on the next sweep, so every correction the
// governance pass needs lives here or in scripts/openapi-conventions.yml and is
// re-applied by running this script again. Idempotent: running it twice changes
// nothing the second time.
//
//   node scripts/harden-openapi.mjs           # apply
//   node scripts/harden-openapi.mjs --check   # report drift, exit 1 if any
//
// What it applies, and why each is not a guess:
//   - openapi 3.2.0 on every document (the network-wide directive).
//   - info contact + license + APIs.io title on all 17.
//   - The dead `search-api.apis.io` half of the search contract is dropped. That
//     host is NXDOMAIN; the APIs.json submit/search shapes it documented are not
//     what apis.io/api/v1 returns. Measured 2026-09-03.
//   - Gated operations answer 402, not 403. Measured against the live API:
//     GET /ratings, /compare, /insights/company/{slug}/gaps and
//     /areas/{slug}/leaders all return 402 keyless.
//   - The four rate-limit response headers every apis.io response actually
//     carries, which no contract documented.
//   - x-tier, x-mcp-tool, security, parameter bounds, and the authored copy in
//     scripts/openapi-conventions.yml.
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse, stringify } from 'yaml';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const OPENAPI = join(ROOT, 'openapi');
const CHECK = process.argv.includes('--check');
const CONV = parse(readFileSync(join(ROOT, 'scripts', 'openapi-conventions.yml'), 'utf8'));

const METHODS = ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace', 'query'];
const isOp = (k) => METHODS.includes(k);
const changes = [];
const note = (file, what) => changes.push(`${file}: ${what}`);

// ---------------------------------------------------------------------------
// Rename a component and every $ref that points at it.
const renameComponent = (doc, kind, from, to) => {
  const bag = doc.components?.[kind];
  if (!bag || !(from in bag) || from === to) return false;
  const reordered = {};
  for (const [k, v] of Object.entries(bag)) reordered[k === from ? to : k] = v;
  doc.components[kind] = reordered;
  const oldRef = `#/components/${kind}/${from}`;
  const newRef = `#/components/${kind}/${to}`;
  const walk = (n) => {
    if (!n || typeof n !== 'object') return;
    if (Array.isArray(n)) return n.forEach(walk);
    for (const [k, v] of Object.entries(n)) {
      if (k === '$ref' && v === oldRef) n.$ref = newRef;
      else walk(v);
    }
  };
  walk(doc);
  return true;
};

const dropComponents = (doc, kind, names) => {
  const bag = doc.components?.[kind];
  if (!bag) return;
  for (const n of names) delete bag[n];
  if (!Object.keys(bag).length) delete doc.components[kind];
};

// Every component reachable from paths/webhooks — used to sweep what the
// legacy-half removal orphaned rather than deleting from a hand-written list.
const reachable = (doc) => {
  const hit = new Set();
  const seen = new Set();
  const walk = (n) => {
    if (!n || typeof n !== 'object' || seen.has(n)) return;
    seen.add(n);
    if (Array.isArray(n)) return n.forEach(walk);
    for (const [k, v] of Object.entries(n)) {
      if (k === '$ref' && typeof v === 'string' && v.startsWith('#/components/')) {
        const key = v.slice('#/components/'.length);
        if (!hit.has(key)) {
          hit.add(key);
          const [kind, name] = key.split('/');
          walk(doc.components?.[kind]?.[name]);
        }
      } else walk(v);
    }
  };
  walk(doc.paths);
  walk(doc.webhooks);
  for (const req of doc.security || []) for (const k of Object.keys(req)) hit.add(`securitySchemes/${k}`);
  for (const item of Object.values(doc.paths || {})) {
    for (const [m, op] of Object.entries(item)) {
      if (!isOp(m)) continue;
      for (const req of op.security || []) for (const k of Object.keys(req)) hit.add(`securitySchemes/${k}`);
    }
  }
  return hit;
};

const pruneUnreachable = (doc, file) => {
  for (let pass = 0; pass < 5; pass++) {
    const hit = reachable(doc);
    let dropped = 0;
    for (const [kind, bag] of Object.entries(doc.components || {})) {
      // headers are referenced by name from responses.headers; the security
      // scheme is declared capability — X-API-Key selects the tier on every
      // endpoint — even where no operation lists it as a requirement.
      if (kind === 'headers' || kind === 'securitySchemes') continue;
      for (const name of Object.keys(bag)) {
        if (!hit.has(`${kind}/${name}`)) { delete bag[name]; dropped++; note(file, `dropped orphan ${kind}/${name}`); }
      }
      if (!Object.keys(bag).length) delete doc.components[kind];
    }
    if (!dropped) break;
  }
};

// ---------------------------------------------------------------------------
const applyInfo = (doc, file) => {
  const i = (doc.info ??= {});
  const want = CONV.info.titles[file];
  if (want && i.title !== want) { note(file, `info.title ${JSON.stringify(i.title)} -> ${JSON.stringify(want)}`); i.title = want; }
  if (!i.description && CONV.info.descriptions[file]) { i.description = CONV.info.descriptions[file]; note(file, 'info.description added'); }
  if (!i.contact) { i.contact = { ...CONV.info.contact }; note(file, 'info.contact added'); }
  if (!i.license) { i.license = { ...CONV.info.license }; note(file, 'info.license added'); }
  if (!i.summary && CONV.info.summaries[file]) { i.summary = CONV.info.summaries[file]; note(file, 'info.summary added'); }
  // Key order the whole network reads.
  const order = ['title', 'summary', 'description', 'version', 'contact', 'license', 'x-logo'];
  doc.info = Object.fromEntries([...order.filter((k) => k in i).map((k) => [k, i[k]]),
    ...Object.entries(i).filter(([k]) => !order.includes(k))]);
};

const applyServers = (doc, file) => {
  const live = CONV.servers;
  const before = JSON.stringify(doc.servers);
  doc.servers = live.map((s) => ({ ...s }));
  if (before !== JSON.stringify(doc.servers)) note(file, 'servers normalised to the live production server');
  // A path-level servers override that repeats the document server is noise; a
  // path-level override pointing anywhere else was the dead host.
  for (const [p, item] of Object.entries(doc.paths || {})) {
    if (item.servers) { delete item.servers; note(file, `dropped path-level servers on ${p}`); }
  }
};

const applyTags = (doc, file) => {
  for (const t of doc.tags || []) {
    if (!t.description && CONV.tags[t.name]) { t.description = CONV.tags[t.name]; note(file, `tags[${t.name}].description added`); }
  }
};

const applyHeaders = (doc, file) => {
  const comps = (doc.components ??= {});
  const before = JSON.stringify(comps.headers ?? null);
  comps.headers = JSON.parse(JSON.stringify(CONV.headers.components));
  if (before !== JSON.stringify(comps.headers)) note(file, 'components.headers: rate-limit headers declared');
  const attach = (resp) => {
    if (!resp || resp.$ref) return;
    const want = Object.fromEntries(CONV.headers.attach.map((h) => [h, { $ref: `#/components/headers/${CONV.headers.names[h]}` }]));
    const merged = { ...want, ...(resp.headers || {}) };
    if (JSON.stringify(resp.headers ?? null) !== JSON.stringify(merged)) resp.headers = merged;
    else resp.headers = merged;
  };
  let touched = 0;
  for (const item of Object.values(doc.paths || {})) {
    for (const [m, op] of Object.entries(item)) {
      if (!isOp(m)) continue;
      for (const r of Object.values(op.responses || {})) { if (!r.$ref) { attach(r); touched++; } }
    }
  }
  for (const r of Object.values(doc.components?.responses || {})) { attach(r); touched++; }
  if (touched) note(file, `rate-limit headers attached to ${touched} responses`);
};

const applySecuritySchemes = (doc, file) => {
  const comps = (doc.components ??= {});
  const schemes = (comps.securitySchemes ??= {});
  const want = CONV.securityScheme;
  if (JSON.stringify(schemes[want.name]) !== JSON.stringify(want.definition)) {
    schemes[want.name] = JSON.parse(JSON.stringify(want.definition));
    note(file, `components.securitySchemes.${want.name} declared`);
  }
};

// Shared error components, created on demand so a 402/404/400 added below never
// dangles. The final unreachability prune sweeps any template nothing ended up
// referencing.
const ensureErrorComponents = (doc, file) => {
  const comps = (doc.components ??= {});
  const schemas = (comps.schemas ??= {});
  if (!schemas.Problem) { schemas.Problem = JSON.parse(JSON.stringify(CONV.componentTemplates.Problem)); note(file, 'schemas.Problem declared'); }
  const responses = (comps.responses ??= {});
  for (const name of ['UpgradeRequired', 'NotFound', 'BadRequest']) {
    if (!responses[name]) { responses[name] = JSON.parse(JSON.stringify(CONV.componentTemplates[name])); note(file, `responses.${name} declared`); }
  }
};

const applyOperations = (doc, file) => {
  for (const [p, item] of Object.entries(doc.paths || {})) {
    for (const [m, op] of Object.entries(item)) {
      if (!isOp(m)) continue;
      const id = op.operationId;
      const tier = CONV.tiers[id] ?? op['x-tier'];
      if (tier && op['x-tier'] !== tier) { op['x-tier'] = tier; note(file, `${id}: x-tier ${tier} (measured)`); }
      // Gated calls answer 402, never 403. Measured against the live API
      // 2026-09-03 — inline 403s included, whatever shape they carried.
      if (op['x-tier'] && op['x-tier'] !== 'free' && op.responses?.['403']) {
        delete op.responses['403'];
        op.responses['402'] ??= { $ref: '#/components/responses/UpgradeRequired' };
        note(file, `${m.toUpperCase()} ${p}: 403 -> 402 (measured)`);
      }
      // Every gated operation must document the 402 it actually returns.
      if (op['x-tier'] && op['x-tier'] !== 'free' && !op.responses?.['402']) {
        (op.responses ??= {})['402'] = { $ref: '#/components/responses/UpgradeRequired' };
        note(file, `${id}: 402 documented (gated, ${op['x-tier']})`);
      }
      const tool = CONV.mcpTools[id];
      if (tool && op['x-mcp-tool'] !== tool) { op['x-mcp-tool'] = tool; note(file, `${id}: x-mcp-tool ${tool}`); }
      if (op.security === undefined) {
        op.security = JSON.parse(JSON.stringify(CONV.security[id] ?? []));
        note(file, `${id}: security declared`);
      }
      if (op.summary && !/[.!?]$/.test(op.summary)) { op.summary = `${op.summary}.`; note(file, `${id}: summary punctuated`); }
      if (!op.description && CONV.operationDescriptions[id]) {
        op.description = CONV.operationDescriptions[id];
        note(file, `${id}: description added`);
      }
      // A GET addressing a named resource documents the 404 a miss returns.
      if (m === 'get' && p.includes('{') && !op.responses?.['404']) {
        op.responses['404'] = { $ref: '#/components/responses/NotFound' };
        note(file, `${id}: 404 documented`);
      }
    }
  }
};

const applyParameters = (doc, file) => {
  const bound = (schema, name) => {
    if (!schema || schema.$ref) return false;
    const b = CONV.parameterBounds;
    let did = false;
    if (schema.type === 'string' && schema.maxLength === undefined && !schema.enum) { schema.maxLength = b.stringMaxLength; did = true; }
    if (schema.type === 'integer' && schema.maximum === undefined) { schema.maximum = b.integerMaximum; did = true; }
    if (schema.type === 'number' && schema.maximum === undefined) { schema.maximum = b.numberMaximum; did = true; }
    if (schema.type === 'array') {
      if (schema.maxItems === undefined) { schema.maxItems = b.arrayMaxItems; did = true; }
      if (schema.items?.type === 'string' && schema.items.maxLength === undefined) { schema.items.maxLength = b.stringMaxLength; did = true; }
    }
    return did;
  };
  const fix = (param, where) => {
    if (!param || param.$ref) return;
    const key = `${param.in}:${param.name}`;
    if (!param.description) {
      const d = CONV.parameterDescriptions[key] ?? CONV.parameterDescriptions[param.name];
      if (d) { param.description = d; note(file, `${where} ${param.name}: description added`); }
    }
    if (param.in === 'path' && param.required !== true) { param.required = true; note(file, `${where} ${param.name}: required: true`); }
    if (bound(param.schema, param.name)) note(file, `${where} ${param.name}: schema bounded`);
  };
  for (const [p, item] of Object.entries(doc.paths || {})) {
    for (const [m, op] of Object.entries(item)) {
      if (!isOp(m)) continue;
      for (const param of op.parameters || []) fix(param, `${m.toUpperCase()} ${p}`);
    }
  }
  for (const [name, param] of Object.entries(doc.components?.parameters || {})) fix(param, `components.parameters.${name}`);
};

// Descriptions and examples for schemas and their properties, from the authored
// copy in scripts/openapi-conventions.yml. Keyed by schema name so one entry
// serves every contract that carries that shape.
const applySchemas = (doc, file) => {
  const copy = CONV.schemas || {};
  const props = CONV.properties || {};
  const scalar = (s) => ['string', 'integer', 'number', 'boolean'].includes(s?.type);

  const walkProps = (schemaName, schema) => {
    if (!schema || typeof schema !== 'object') return;
    for (const [pk, p] of Object.entries(schema.properties || {})) {
      if (!p || typeof p !== 'object') continue;
      const entry = props[`${schemaName}.${pk}`];
      if (entry) {
        if (!p.description && entry.description) { p.description = entry.description; note(file, `${schemaName}.${pk}: description`); }
        if (entry.example !== undefined && p.examples === undefined && p.example === undefined) {
          p.examples = [entry.example]; note(file, `${schemaName}.${pk}: example`);
        }
      }
      // A scalar with no bound is an unbounded field on the wire.
      const b = CONV.parameterBounds;
      if (p.type === 'string' && p.maxLength === undefined && !p.enum && !p.format) p.maxLength = b.stringMaxLength;
      walkProps(`${schemaName}.${pk}`, p);
      if (p.items?.properties) walkProps(`${schemaName}.${pk}[]`, p.items);
      for (const branch of [...(p.allOf || []), ...(p.oneOf || []), ...(p.anyOf || [])]) {
        if (branch?.properties) walkProps(`${schemaName}.${pk}`, branch);
      }
      void scalar;
    }
  };

  for (const [name, schema] of Object.entries(doc.components?.schemas || {})) {
    const entry = copy[name];
    if (entry) {
      if (!schema.description && entry.description) { schema.description = entry.description; note(file, `schema ${name}: description`); }
      if (!schema.type && entry.type) { schema.type = entry.type; note(file, `schema ${name}: type ${entry.type}`); }
    }
    walkProps(name, schema);
  }
  // Inline request/response body schemas carry properties too.
  for (const [p, item] of Object.entries(doc.paths || {})) {
    for (const [m, op] of Object.entries(item)) {
      if (!isOp(m)) continue;
      for (const mo of Object.values(op.requestBody?.content || {})) walkProps(`body:${m} ${p}`, mo?.schema);
      for (const [code, r] of Object.entries(op.responses || {})) {
        for (const mo of Object.values(r.content || {})) walkProps(`resp:${m} ${p} ${code}`, mo?.schema);
      }
    }
  }
};

const applyRequestBodies = (doc, file) => {
  for (const [p, item] of Object.entries(doc.paths || {})) {
    for (const [m, op] of Object.entries(item)) {
      if (!isOp(m) || !op.requestBody || op.requestBody.$ref) continue;
      const key = `${m} ${p}`;
      if (!op.requestBody.description && CONV.requestBodies[key]) {
        op.requestBody.description = CONV.requestBodies[key];
        note(file, `${key}: requestBody.description added`);
      }
      if (op.requestBody.required === undefined) { op.requestBody.required = true; note(file, `${key}: requestBody.required`); }
    }
  }
};

const applyResponses = (doc, file) => {
  for (const [p, item] of Object.entries(doc.paths || {})) {
    for (const [m, op] of Object.entries(item)) {
      if (!isOp(m)) continue;
      for (const [code, r] of Object.entries(op.responses || {})) {
        if (r.$ref) continue;
        if (!r.description) { r.description = CONV.responseDescriptions[code] ?? 'Response.'; note(file, `${m} ${p} ${code}: description`); }
        if (!r.content && code !== '204') {
          r.content = { 'application/problem+json': { schema: { $ref: '#/components/schemas/Problem' } } };
          note(file, `${m} ${p} ${code}: content added`);
        }
      }
    }
  }
  // Failures speak RFC 9457. The two shared responses still answering in plain
  // application/json move to problem+json with the Problem schema; their
  // machine-readable extension members survive in the example — RFC 9457
  // extension members are legal, and Problem is additionalProperties: true.
  for (const [name, conv] of Object.entries(CONV.responseConversions)) {
    const r = doc.components?.responses?.[name];
    if (!r || !r.content?.['application/json']) continue;
    delete r.content['application/json'];
    r.content['application/problem+json'] = {
      schema: { $ref: '#/components/schemas/Problem' },
      example: JSON.parse(JSON.stringify(conv.example)),
    };
    r.description = conv.description;
    note(file, `components.responses.${name}: application/json -> application/problem+json`);
  }
  for (const [name, r] of Object.entries(doc.components?.responses || {})) {
    // 403 -> 402 changed what UpgradeRequired has to say, so its copy is forced
    // rather than only filled in when absent.
    const override = CONV.responseOverrides[name];
    if (override) {
      if (r.description !== override.description) { r.description = override.description; note(file, `components.responses.${name}: description corrected`); }
      for (const mo of Object.values(r.content || {})) {
        if (JSON.stringify(mo.example) !== JSON.stringify(override.example)) {
          mo.example = JSON.parse(JSON.stringify(override.example));
          note(file, `components.responses.${name}: example corrected`);
        }
      }
      continue;
    }
    for (const mo of Object.values(r.content || {})) {
      if (mo.example === undefined && mo.examples === undefined && CONV.responseExamples[name]) {
        mo.example = JSON.parse(JSON.stringify(CONV.responseExamples[name]));
        note(file, `components.responses.${name}: example added`);
      }
    }
  }
};

// ---------------------------------------------------------------------------
const files = readdirSync(OPENAPI).filter((f) => f.endsWith('-api-openapi.yml')).sort();
let drift = 0;

for (const file of files) {
  const path = join(OPENAPI, file);
  const original = readFileSync(path, 'utf8');
  const doc = parse(original);
  const before = changes.length;

  if (doc.openapi !== '3.2.0') { note(file, `openapi ${doc.openapi} -> 3.2.0`); doc.openapi = '3.2.0'; }

  // The dead half of the search contract, and the name collisions it caused.
  for (const drop of CONV.dropPaths[file] || []) {
    if (doc.paths?.[drop]) { delete doc.paths[drop]; note(file, `dropped ${drop} (host is NXDOMAIN)`); }
  }
  if (CONV.dropPaths[file]) pruneUnreachable(doc, file);
  for (const [kind, map] of Object.entries(CONV.renames[file] || {})) {
    for (const [from, to] of Object.entries(map)) {
      if (renameComponent(doc, kind, from, to)) note(file, `renamed ${kind}/${from} -> ${to}`);
    }
  }
  delete doc['x-refined-from'];

  // Copy corrected by measurement: sentences claiming a surface is Free where
  // the live API answers 402. Exact-substring, so a fix that no longer matches
  // simply stops applying.
  const fixes = CONV.copyFixes[file] || [];
  if (fixes.length) {
    const deepFix = (n) => {
      if (!n || typeof n !== 'object') return;
      for (const [k, v] of Object.entries(n)) {
        if (typeof v === 'string') {
          let s = v;
          for (const [from, to] of fixes) if (s.includes(from)) s = s.split(from).join(to);
          if (s !== v) { n[k] = s; note(file, `copy fix in ${k}`); }
        } else deepFix(v);
      }
    };
    deepFix(doc.info);
    deepFix(doc.tags);
    for (const item of Object.values(doc.paths || {})) {
      for (const [m, op] of Object.entries(item)) if (isOp(m)) deepFix(op);
    }
  }

  applyInfo(doc, file);
  applyServers(doc, file);
  applyTags(doc, file);
  applySecuritySchemes(doc, file);
  ensureErrorComponents(doc, file);
  applyOperations(doc, file);
  applyParameters(doc, file);
  applyRequestBodies(doc, file);
  applyResponses(doc, file);
  applySchemas(doc, file);
  applyHeaders(doc, file);
  pruneUnreachable(doc, file);

  const out = stringify(doc, { lineWidth: 0, singleQuote: false });
  if (out !== original) {
    drift++;
    if (!CHECK) writeFileSync(path, out);
  } else if (changes.length > before) {
    changes.length = before; // no textual change, nothing to report
  }
}

for (const c of changes) console.log(`  ${c}`);
console.log(`\n  ${changes.length} corrections across ${drift}/${files.length} contracts`);
if (CHECK && drift) { console.error('  drift: run node scripts/harden-openapi.mjs'); process.exit(1); }
