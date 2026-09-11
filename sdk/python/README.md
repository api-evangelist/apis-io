# apisio — Python client and CLI for the apis.io catalog

A thin client for [apis.io](https://apis.io), the API catalog: 27,000+ providers, their contracts,
their artifacts and their ratings.

No runtime dependencies. The 108 operation methods are **generated from the OpenAPI documents
apis.io publishes**, so they cannot drift from the contract.

```bash
pip install apisio
```

## Use it

```python
from apisio import Client

api = Client()                       # the free tier is KEYLESS — no signup to read the catalog
api = Client(api_key="apisio_live_…")  # a plan, from https://apis.io/developer/

for p in api.list_providers(q="payments", limit=5):
    print(p["slug"], p["band"])

stripe = api.get_provider("stripe")
api.get_provider_artifacts("stripe")
api.search(q="webhooks")
```

Collections come back as a `Page` — a real list you can iterate, carrying the server's own count:

```python
p = api.list_providers(q="banking")
len(p), p.total, p.pages          # 25, 1840, 74

for provider in api.paginate("/providers", q="banking", limit=100):
    ...                            # walks every page, stops on the server's own page count
```

## What is free and what is not

Reading the catalog is free and needs no key: search, providers, apis, tags, taxonomy, artifacts,
and everything about **one** provider. Anything that synthesises **across** it — ratings, cohorts,
capabilities, insights, stack design — needs a plan.

A refusal always tells you which of the two it is, and that distinction matters more than it looks:

```python
from apisio import PaymentRequired, Unauthenticated

try:
    api.what_can_i_fix("stripe")
except Unauthenticated as e:
    # You have NO credential. This is not a paywall — it is the way in.
    e.resource_metadata     # https://apis.io/.well-known/oauth-protected-resource/api/v1
    e.scope                 # apis:pro
except PaymentRequired as e:
    # You ARE authenticated and this resource needs a bigger plan.
    e.tier                  # "business"
    e.plans_url             # https://apis.io/developer/plans/
```

A `raise_for_status()` collapses those into one "it failed", and an agent that cannot tell them
apart either never registers or tries to buy something it has no identity to buy with. Keeping them
apart is most of why this client exists.

The challenge itself arrives under a non-standard header name (API Gateway reserves
`WWW-Authenticate` and renames it). `resource_metadata` reads all three spellings so you never have
to care.

## Rate limits

Read from the response headers, where they actually are:

```python
api.list_providers(limit=1)
api.last_rate_limit          # RateLimit(tier='pro', limit=5000, window=86400)
```

`429` is retried with the server's own `Retry-After`. `402` never is — a paywall will not become a
`200` by asking again.

## The command line

```bash
pip install apisio
export APIS_IO_API_KEY=apisio_live_…      # optional; the catalog reads free

apisio search payments
apisio provider stripe
apisio providers --tag banking --min-score 60 --limit 10
```

The provider-improvement flow, in the order you actually walk it:

```bash
apisio rating stripe            # where this listing stands
apisio fix stripe               # the ranked, costed punch list
apisio gates stripe             # what stands between it and the next band
apisio simulate stripe --fix openapi_present --fix rate_limits_documented
apisio claim stripe             # claim the listing
apisio submit stripe --type OpenAPI --url https://example.com/openapi.yaml
```

Anything else, by operation name:

```bash
apisio operations                        # all 108
apisio call get_cohort industry payments
apisio call list_tags limit=5 --json
```

`--json` on any command gives you the raw response.

Exit codes: `4` for 401 (you need to authenticate), `5` for 402 (you need a plan), `1` for anything
else — so a script can branch on "go register" versus "go buy" without parsing text.

## How the bindings are made

```bash
make generate     # re-derive apisio/operations.py from ../../openapi/_original/
make check        # non-zero if the committed bindings no longer match the contract
make test
```

The source is `openapi/_original/` — the documents apis.io **publishes**, not our refined mirror.
Those are different document sets, and a client generated from a derivative would describe an API
nobody can call.

Generating rather than hand-writing is not only about effort. Binding all 108 operations at once is
a contract test nobody else runs, and the first pass found three defects in the published
documents: hoisted `$ref` parameters, response schemas behind `$ref`, and a `/search` contract that
described a shape the endpoint has never returned (roadmap#308).

## Licence

Apache-2.0.
