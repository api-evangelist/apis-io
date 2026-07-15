# OWASP API Security Review — APIs.io API

**Generated:** 2026-07-15 08:38 EDT  
**Total findings:** 216

## Provenance

- **Ruleset:** [`@api-common/spectral-owasp-ruleset`](https://github.com/api-commons/spectral-owasp-ruleset) v0.2.0 — OWASP API Security Top 10 (2023)
- **Engine:** Stoplight Spectral (`@stoplight/spectral-cli`)
- **Reporter:** [`@api-common/spectral-reporter`](https://reporter.apicommons.org)
- **Source spec:** `apis-io-v1-openapi.yml`
- **Command:** `spectral lint -r owasp-api-top10.yaml -f json <spec>`

## Severity

| Severity | Count |
|---|---|
| Warning | 70 |
| Info | 146 |

## By OWASP category

| Category | Findings |
|---|---|
| API1 Broken Object Level Authorization | 34 |
| API4 Unrestricted Resource Consumption | 181 |
| API7 Server Side Request Forgery | 1 |

## Top rules

| Count | Rule |
|---|---|
| 117 | `owasp-api4-resource-string-maxlength` |
| 36 | `owasp-api4-resource-array-maxitems` |
| 34 | `owasp-api1-bola-operation-security-defined` |
| 28 | `owasp-api4-resource-integer-bounds` |
| 1 | `owasp-api7-ssrf-url-property-format` |

## Files

- `report.html` — standalone HTML governance report (open in a browser)
- `spectral.json` — raw Spectral findings
- `results.sarif` — SARIF 2.1.0 for GitHub code scanning
