#!/usr/bin/env node
// Split the monolithic APIs.io OpenAPI into one SELF-CONTAINED OpenAPI per tag.
//
// The single 62-operation contract made for one undifferentiated blob of docs and
// one undifferentiated governance report. One spec per tag means each surface is
// documented, indexed in apis.yml, linted, and scored on its own terms.
//
// Self-contained is deliberate: each output carries the transitive subset of
// components it actually references, so every spec lints, renders, and reports
// with no external $ref resolution. apis-io-v1-openapi.yml stays the source of
// truth — re-run this whenever it changes.
//
//   node scripts/split-openapi.mjs          # write the per-tag specs
//   node scripts/split-openapi.mjs --check  # verify they are in sync (CI-friendly)
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse, stringify } from 'yaml';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'openapi', 'apis-io-v1-openapi.yml');
const OUT_DIR = join(ROOT, 'openapi');
const CHECK = process.argv.includes('--check');

const doc = parse(readFileSync(SRC, 'utf8'));
const METHODS = ['get', 'put', 'post', 'delete', 'patch', 'options', 'head', 'trace'];
export const kebab = (s) => String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

// Every local $ref reachable from a node.
function collectRefs(node, acc = new Set()) {
  if (!node || typeof node !== 'object') return acc;
  if (Array.isArray(node)) { for (const n of node) collectRefs(n, acc); return acc; }
  for (const [k, v] of Object.entries(node)) {
    if (k === '$ref' && typeof v === 'string') acc.add(v);
    else collectRefs(v, acc);
  }
  return acc;
}

const resolveRef = (ref) => ref.startsWith('#/')
  ? ref.slice(2).split('/').reduce((o, seg) => o?.[seg.replace(/~1/g, '/').replace(/~0/g, '~')], doc)
  : undefined;

// Walk $refs transitively — a schema can reference other schemas, a response can
// reference a schema, and so on — until the closure is complete.
function neededComponents(seed) {
  const needed = {};
  const queue = [...collectRefs(seed)];
  const seen = new Set();
  while (queue.length) {
    const ref = queue.shift();
    if (seen.has(ref)) continue;
    seen.add(ref);
    const m = /^#\/components\/([^/]+)\/(.+)$/.exec(ref);
    if (!m) continue;
    const [, section, name] = m;
    (needed[section] ??= new Set()).add(name);
    const node = resolveRef(ref);
    if (node) for (const r of collectRefs(node)) if (!seen.has(r)) queue.push(r);
  }
  return needed;
}

// securitySchemes are referenced by NAME in `security:` requirements, not by $ref,
// so collectRefs can't see them — gather them separately.
function neededSchemes(ops) {
  const names = new Set();
  for (const req of doc.security ?? []) for (const n of Object.keys(req)) names.add(n);
  for (const op of ops) for (const req of op.security ?? []) for (const n of Object.keys(req)) names.add(n);
  return names;
}

// An operation's PRIMARY tag is its first — that is its one home. Five operations
// carry two tags (e.g. GET /providers/{slug}/apis is both Providers and APIs); routing
// each to its primary keeps every operation in exactly one spec, so the eleven specs
// partition the 62 operations rather than double-counting them in reports. The output
// op's tags are trimmed to that primary so no spec references a tag it doesn't declare.
const primaryTag = (op) => (op.tags ?? [])[0];

const specForTag = (tag) => {
  const paths = {};
  const ops = [];
  for (const [p, item] of Object.entries(doc.paths ?? {})) {
    for (const m of METHODS) {
      const op = item[m];
      if (!op || primaryTag(op) !== tag.name) continue;
      (paths[p] ??= {})[m] = { ...op, tags: [tag.name] };
      if (item.parameters) paths[p].parameters = item.parameters; // path-level params travel with it
      ops.push(op);
    }
  }
  if (!Object.keys(paths).length) return null;

  const needed = neededComponents(paths);
  for (const n of neededSchemes(ops)) (needed.securitySchemes ??= new Set()).add(n);

  const components = {};
  for (const section of Object.keys(needed).sort()) {
    const src = doc.components?.[section] ?? {};
    components[section] = {};
    for (const name of [...needed[section]].sort()) {
      if (src[name] !== undefined) components[section][name] = src[name];
    }
    if (!Object.keys(components[section]).length) delete components[section];
  }

  return {
    openapi: doc.openapi,
    info: {
      title: `APIs.io ${tag.name} API`,
      version: doc.info.version,
      description: `${tag.description}\n\nThis is the ${tag.name} surface of the [APIs.io API](https://apis.io/api/v1) — one of eleven contracts split from the full API by tag, each documented and governed on its own. See the APIs.json index for the whole set.`,
      ...(doc.info.contact ? { contact: doc.info.contact } : {}),
      ...(doc.info.license ? { license: doc.info.license } : {}),
      ...(doc.info.termsOfService ? { termsOfService: doc.info.termsOfService } : {}),
    },
    ...(doc.servers ? { servers: doc.servers } : {}),
    ...(doc.security?.length ? { security: doc.security } : {}),
    tags: [tag],
    paths,
    ...(Object.keys(components).length ? { components } : {}),
    ...(doc.externalDocs ? { externalDocs: doc.externalDocs } : {}),
  };
};

let written = 0, drift = 0;
const manifest = [];
for (const tag of doc.tags ?? []) {
  const spec = specForTag(tag);
  if (!spec) { console.warn(`  ! no operations for tag "${tag.name}" — skipped`); continue; }
  // Named for the contract they are split FROM (apis-io-v1-openapi.yml), so the lineage is
  // stated in the filename. (This also kept them clear of the legacy
  // apis-io-search-openapi.yaml — a different API on the long-dead search-api.apis.io host —
  // which has since been retired and its Arazzo workflows repointed at v1.)
  const slug = kebab(tag.name);
  const file = join(OUT_DIR, `apis-io-v1-${slug}-openapi.yml`);
  const out = stringify(spec, { lineWidth: 0 });
  const opCount = Object.values(spec.paths).reduce((n, i) => n + Object.keys(i).filter((k) => METHODS.includes(k)).length, 0);
  manifest.push({ tag: tag.name, slug, file: `openapi/apis-io-v1-${slug}-openapi.yml`, operations: opCount, schemas: Object.keys(spec.components?.schemas ?? {}).length });

  if (CHECK) {
    const same = existsSync(file) && readFileSync(file, 'utf8') === out;
    if (!same) { drift++; console.error(`  ✗ out of sync: ${slug}`); }
    continue;
  }
  writeFileSync(file, out);
  written++;
  console.log(`  ✓ ${String(opCount).padStart(2)} ops, ${String(Object.keys(spec.components?.schemas ?? {}).length).padStart(2)} schemas  →  apis-io-v1-${slug}-openapi.yml`);
}

if (CHECK) {
  if (drift) { console.error(`\n${drift} spec(s) out of sync with ${SRC} — run: node scripts/split-openapi.mjs`); process.exit(1); }
  console.log('All per-tag specs are in sync with the source contract.');
} else {
  writeFileSync(join(OUT_DIR, 'split-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
  const totalOps = manifest.reduce((n, m) => n + m.operations, 0);
  // The eleven specs must PARTITION the source: every operation lands in exactly one.
  // If these ever diverge the split is silently lying and every report built on it is wrong.
  const sourceOps = Object.values(doc.paths ?? {})
    .reduce((n, i) => n + Object.keys(i).filter((k) => METHODS.includes(k)).length, 0);
  console.log(`\nWrote ${written} per-tag specs covering ${totalOps} of ${sourceOps} source operations.`);
  if (totalOps !== sourceOps) {
    console.error(`  ✗ PARTITION BROKEN: ${totalOps} split vs ${sourceOps} source — an operation is duplicated or lost.`);
    process.exit(1);
  }
  console.log('  ✓ partition verified — every operation has exactly one home.');
}
