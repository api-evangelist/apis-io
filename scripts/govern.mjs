#!/usr/bin/env node
// Govern the APIs.io contracts with the API Evangelist Governance API — the same
// hosted service anyone else would call. This is the dogfood: apis.io's own specs are
// linted, coverage-measured, and scored by api.apievangelist.com/v1/governance/*, and
// the run is written to governance/<date>/ next to the OWASP runs already kept there.
//
// Every endpoint used here is FREE tier and keyless, which is the point — checking an
// API costs nothing. Calls are serialized to stay under the free 5 req/s limit.
//
//   node scripts/govern.mjs                    # run + write governance/<today>/
//   node scripts/govern.mjs --ruleset <file>   # lint against a specific Spectral ruleset
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse } from 'yaml';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const API = process.env.GOV_API || 'https://api.apievangelist.com/v1';
const manifest = JSON.parse(readFileSync(join(ROOT, 'openapi', 'split-manifest.json'), 'utf8'));

const rulesetArg = process.argv.indexOf('--ruleset');
const rulesetPath = rulesetArg > -1 ? process.argv[rulesetArg + 1] : null;
const ruleset = rulesetPath ? parse(readFileSync(rulesetPath, 'utf8')) : null;

// governance/<run>/<date>/ — matching the owasp/<date>/ provenance convention already
// in this repo. `catalog` is the full curated best-of-breed run; a named run is the
// ruleset we actually own. Keeping both is the point: the contrast IS the finding.
const runName = ruleset ? basename(rulesetPath).replace(/\.(ya?ml|json)$/, '') : 'catalog';
const today = new Date().toISOString().slice(0, 10);
const OUT = join(ROOT, 'governance', runName, today);
mkdirSync(OUT, { recursive: true });

const post = async (path, body) => {
  const res = await fetch(`${API}/${path}`, {
    method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`${path} -> ${res.status} ${text.slice(0, 160)}`);
  return JSON.parse(text);
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const rows = [];
for (const entry of manifest) {
  const document = readFileSync(join(ROOT, entry.file), 'utf8');

  // The ruleset travels through all three: lint, coverage, and score must all be
  // measured against the SAME rules or the numbers don't describe the same thing.
  const withRuleset = ruleset ? { ruleset } : {};
  const lint = await post('governance/validate', { document, ...withRuleset });
  await sleep(250);
  const coverage = await post('governance/coverage', { document, ...withRuleset });
  await sleep(250);
  const scorecard = await post('governance/scorecard', { document, ...withRuleset });
  await sleep(250);

  const result = { api: `APIs.io ${entry.tag} API`, file: entry.file, operations: entry.operations, lint, coverage, scorecard };
  writeFileSync(join(OUT, `${entry.slug}.json`), JSON.stringify(result, null, 2) + '\n');

  // The HTML report the Spectral Reporter would render, straight from the API.
  const report = await fetch(`${API}/governance/report`, {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ results: lint.diagnostics, title: `APIs.io ${entry.tag} API — Governance` }),
  }).then((r) => r.text());
  writeFileSync(join(OUT, `${entry.slug}.html`), report);
  await sleep(250);

  rows.push({
    tag: entry.tag, ops: entry.operations, rules: lint.ruleCount,
    // Carry info/hint too. A summary that reports only errors+warnings hides findings —
    // which is the exact failure mode this whole exercise is arguing against.
    errors: lint.summary.error, warnings: lint.summary.warning,
    info: lint.summary.info, hints: lint.summary.hint, findings: lint.summary.total,
    passed: lint.passed,
    coverage: Math.round(coverage.coveragePct ?? 0), score: scorecard.overall, grade: scorecard.grade,
  });
  console.log(`  ${entry.tag.padEnd(16)} ${String(entry.operations).padStart(2)} ops  ` +
    `${lint.passed ? '✓' : '✗'} ${String(lint.summary.error).padStart(2)}E/${String(lint.summary.warning).padStart(3)}W  ` +
    `cov ${String(Math.round(coverage.coveragePct ?? 0)).padStart(3)}%  score ${String(scorecard.overall).padStart(3)} (${scorecard.grade})`);
}

const summary = {
  ran: new Date().toISOString(),
  api: API,
  ruleset: ruleset ? basename(process.argv[rulesetArg + 1]) : 'apievangelist curated catalog (default)',
  totals: {
    apis: rows.length,
    operations: rows.reduce((n, r) => n + r.ops, 0),
    errors: rows.reduce((n, r) => n + r.errors, 0),
    warnings: rows.reduce((n, r) => n + r.warnings, 0),
    info: rows.reduce((n, r) => n + (r.info || 0), 0),
    hints: rows.reduce((n, r) => n + (r.hints || 0), 0),
    findings: rows.reduce((n, r) => n + (r.findings || 0), 0),
    passing: rows.filter((r) => r.passed).length,
  },
  apis: rows,
};
writeFileSync(join(OUT, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(`\n  ${summary.totals.passing}/${summary.totals.apis} passing · ` +
  `${summary.totals.errors} errors · ${summary.totals.warnings} warnings · ${summary.totals.info} info · ` +
  `${summary.totals.findings} findings across ${summary.totals.operations} operations`);
console.log(`  ruleset: ${summary.ruleset}`);
console.log(`  → governance/${runName}/${today}/`);
