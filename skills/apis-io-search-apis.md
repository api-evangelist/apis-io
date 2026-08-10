# search-apis

**Description:** Find APIs in the apis.io catalog by keyword, tag, or provider. Returns structured matches the agent can hand to the user or feed to other skills.

## When to use this skill

Use when the user asks "what APIs are there for X", "find an API to do Y", "which providers offer Z", or any other intent that requires filtering the catalog. Prefer this over scraping search HTML.

## Inputs

- A free-text query (e.g., `"github actions"`, `"send sms"`, `"weather"`).
- Optional filters: provider name or tag.

## How it works

The catalog endpoint `https://apis.io/.well-known/api-catalog` returns RFC 9264 JSON. Each entry looks like:

```json
{
  "anchor": "https://apis.io/apis/<provider>/<slug>/",
  "title": "<API name>",
  "service-desc": [{"href": "...", "type": "application/vnd.oai.openapi"}],
  "service-doc":  [{"href": "...", "type": "text/html"}],
  "describedby": [{"href": "...", "title": "JSONSchema"}]
}
```

Filter `linkset[]` client-side. Title and anchor are searchable; the anchor encodes the provider slug and API slug.

## Recipe

```python
import json, urllib.request, re

CATALOG = "https://apis.io/.well-known/api-catalog"

def search(query, *, provider=None, limit=20):
    with urllib.request.urlopen(CATALOG) as r:
        catalog = json.load(r)
    q = query.lower()
    results = []
    for entry in catalog["linkset"]:
        anchor = entry["anchor"]
        title = entry.get("title", "")
        provider_slug = anchor.split("/apis/")[-1].split("/")[0]
        if provider and provider != provider_slug:
            continue
        haystack = (title + " " + anchor).lower()
        if q in haystack:
            results.append({
                "title": title,
                "url": anchor,
                "provider": provider_slug,
                "openapi": next((d["href"] for d in entry.get("service-desc", []) if "openapi" in d.get("type","")), None),
                "docs":    next((d["href"] for d in entry.get("service-doc", [])), None),
            })
        if len(results) >= limit:
            break
    return results
```

## Output format (recommended)

When presenting results to the user, give:
- API name (from `title`)
- Provider slug
- Live apis.io URL
- OpenAPI URL if present
- Docs URL if present

Skip entries with no `service-desc` and no `service-doc` — they're profile placeholders, not consumable APIs.

## Tag filtering

Tag-based browsing: `https://apis.io/tag/<tag-slug>/` returns an HTML page; for structured tag data fetch each subdomain's `search-index.json`:
- `https://apis.io/search-index.json`
- `https://apis.io/search-index.json`

## Related skills

- `discover-apis-io` — use this first to learn the network's structure.
- `fetch-api-spec` — once a search returns a hit, fetch its OpenAPI for parsing.
