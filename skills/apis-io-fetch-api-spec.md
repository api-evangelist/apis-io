# fetch-api-spec

**Description:** Given an apis.io API URL or catalog entry, fetch the OpenAPI / AsyncAPI / Postman specification for that API and return it parsed.

## When to use this skill

Use after `search-apis` returns a hit, or whenever the user supplies an `apis.apis.io/apis/...` URL and wants to inspect, summarize, or generate code from the underlying API description.

## Inputs

One of:
- An apis.io API URL (e.g., `https://apis.io/apis/github/github-app-api/`).
- A catalog entry from `search-apis`.

## Recipe — from apis.io URL

```python
import json, urllib.request, yaml

def fetch_spec(api_url):
    """Fetch and parse the spec for an apis.io API URL."""
    # Get the markdown summary first — gives us catalog metadata cheaply.
    req = urllib.request.Request(api_url, headers={"Accept": "text/markdown"})
    with urllib.request.urlopen(req) as r:
        markdown = r.read().decode("utf-8")

    # Resolve the OpenAPI URL by hitting the api-catalog directly.
    catalog_url = "https://apis.io/.well-known/api-catalog"
    with urllib.request.urlopen(catalog_url) as r:
        catalog = json.load(r)

    entry = next((e for e in catalog["linkset"] if e["anchor"] == api_url), None)
    if not entry:
        return None

    spec_link = next(
        (d for d in entry.get("service-desc", [])
         if d.get("type") in ("application/vnd.oai.openapi", "application/vnd.aai.asyncapi")),
        None,
    )
    if not spec_link:
        return {"summary": markdown, "spec": None}

    with urllib.request.urlopen(spec_link["href"]) as r:
        body = r.read().decode("utf-8")
    spec = yaml.safe_load(body)  # OpenAPI specs are valid YAML even when JSON.
    return {"summary": markdown, "spec": spec, "spec_url": spec_link["href"], "spec_type": spec_link["type"]}
```

## What to do with the spec

Common follow-ups after fetching:
- **Summarize endpoints**: list `paths.*` keys with their HTTP methods and `summary` fields.
- **Find an operation**: search `paths` and `operations[]` for matching `operationId` or path pattern.
- **Generate a curl**: combine `servers[0].url`, the path, and any required parameters.
- **Extract schemas**: pull from `components.schemas` and surface the relevant ones.

## Caching

The api-catalog (≈4 MB) is the same across all skill invocations within a session. Cache it once and reuse. The OpenAPI specs themselves vary in size — cache per-API.

## Related skills

- `discover-apis-io` — learn the network structure first.
- `search-apis` — find candidate APIs by keyword.
