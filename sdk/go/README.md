# apisio — Go client for the apis.io catalog

```bash
go get github.com/api-evangelist/apis-io/sdk/go
```

```go
api := apisio.New()                                  // the free tier is KEYLESS
api = apisio.New(apisio.WithAPIKey("apisio_live_…"))

p, err := api.ListProviders(ctx, map[string]any{"q": "payments", "limit": 5})
for _, r := range p.Data { fmt.Println(r["slug"], r["band"]) }
fmt.Println(p.Meta.Total)
```

Standard library only.

## 401 and 402 are different answers

```go
_, err := api.WhatCanIFix(ctx, "stripe", nil)

var un *apisio.Unauthenticated
var pr *apisio.PaymentRequired
switch {
case errors.As(err, &un):
    un.ResourceMetadata()   // https://apis.io/.well-known/oauth-protected-resource/api/v1
    un.Scope()              // apis:pro
case errors.As(err, &pr):
    pr.Tier()               // "business"
    pr.PlansURL()
}
```

A 401 is not a paywall — it is the way in. Keeping the two apart is most of why this client exists.

The challenge arrives under a non-standard header name (API Gateway reserves `WWW-Authenticate`
and renames it); `ResourceMetadata` reads all three spellings.

## Rate limits

```go
api.LastRateLimit    // {Tier: "pro", Limit: 5000, Window: 86400}
```

`429` is retried with the server's own `Retry-After`. `402` never is.

## Generated, not hand-written

The 108 operation methods come from the OpenAPI documents apis.io publishes, emitted by the same
generator that produces the Python and JavaScript clients — one spec parse, three targets.

```bash
python3 ../python/generate.py          # regenerate all three
python3 ../python/generate.py --check  # non-zero if any is stale
```

Apache-2.0.
