# discover-apis-io

**Description:** Discover the structure of the apis.io network — its subdomains, machine-readable catalogs, and content-negotiation conventions — so other skills can find APIs efficiently.

## When to use this skill

Use this skill first when the user mentions apis.io, asks about API discovery, or wants to find APIs across a catalog. It primes the agent with the network's discovery endpoints so subsequent searches don't waste tokens scraping HTML.

## What apis.io is

apis.io is a federated catalog of public APIs maintained by API Evangelist. Content is sharded across subdomains:

| Subdomain | Purpose |
|---|---|
| `apis.io` | Search hub. Federates across all subdomains. |
| `apis.apis.io` | Individual APIs (≈6,500). |
| `providers.apis.io` | API providers (≈1,300 companies/projects). |
| `schemas.apis.io` | JSON Schema definitions (≈43,000). |
| `asyncapi.apis.io` | AsyncAPI event specs. |
| `json-ld.apis.io` | JSON-LD semantic vocabularies. |
| `rules.apis.io` | Spectral governance rulesets. |
| `tags.apis.io` | Tag-based browsing. |
| `vocabularies.apis.io` | Faceted vocabulary search. |
| `examples.apis.io` | API usage examples. |

## Discovery endpoints

Every page on every subdomain advertises three things in HTTP `Link` response headers (RFC 8288):

```
Link: <https://apis.io/.well-known/api-catalog>; rel="api-catalog"; type="application/linkset+json",
      </sitemap.xml>; rel="sitemap"; type="application/xml",
      <self-url>; rel="alternate"; type="text/markdown"
```

Hit any apis.io page with `curl -I` to see them.

### `/.well-known/api-catalog` (RFC 9727)

The canonical discovery endpoint. Two catalogs exist:

- `https://apis.io/.well-known/api-catalog` — every API in the network. Format is RFC 9264 linkset (JSON). Each entry has an `anchor` (the API's apis.io URL), optional `service-desc` (OpenAPI/AsyncAPI/Postman URLs), `service-doc` (human docs), and `describedby` (schemas).
- `https://apis.io/.well-known/api-catalog` — every provider, each with their APIs nested under `service-desc`.

Content-Type is `application/linkset+json`. Both files are ≈2–4 MB.

### `/sitemap.xml`

Per-subdomain sitemap.xml lists every page in that subdomain. Use for crawl-style discovery.

### `/robots.txt`

All subdomains publish a Cloudflare Content-Signal that explicitly permits search indexing, AI inference, and AI training:
```
Content-Signal: search=yes, ai-input=yes, ai-train=yes
```

## Content negotiation

Send `Accept: text/markdown` to any `apis.apis.io/apis/<provider>/<slug>/` or `providers.apis.io/providers/<slug>/` URL and the server returns clean structured markdown synthesized from the api-catalog. No HTML scraping needed:

```bash
curl -H "Accept: text/markdown" https://apis.io/apis/github/github-app-api/
```

Returns:
```markdown
# GitHub App API

**API:** <https://apis.io/apis/github/github-app-api/>

## Machine-readable descriptions
- [OpenAPI](https://raw.githubusercontent.com/.../github-app-api-openapi.yml) — `application/vnd.oai.openapi`

## Documentation
- [Documentation](https://docs.github.com/en/rest/apps)
```

## Recommended discovery flow

1. Fetch `https://apis.io/.well-known/api-catalog` once and cache it (≈4 MB JSON).
2. Filter `linkset[]` entries by anchor URL or title to find APIs of interest.
3. For each match, follow `service-desc[].href` to fetch OpenAPI/AsyncAPI directly.
4. For provider-level browsing, use `https://apis.io/.well-known/api-catalog` instead.

## Related skills

- `search-apis` — keyword search across the catalog.
- `fetch-api-spec` — pull and parse the OpenAPI/AsyncAPI for a specific API.
