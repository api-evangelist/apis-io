# @apis-io/client — JavaScript client for the apis.io catalog

```bash
npm install @apis-io/client
```

```js
import { Client, PaymentRequired, Unauthenticated } from '@apis-io/client';

const api = new Client();                       // the free tier is KEYLESS
const api2 = new Client({ apiKey: 'apisio_live_…' });

for (const p of await api.listProviders({ q: 'payments', limit: 5 })) {
  console.log(p.slug, p.band);
}
```

No dependencies. Node 18+ or a browser — the API sends CORS headers, and since roadmap#292 it
exposes the challenge header a browser needs to read a 401.

## Collections are real arrays

```js
const p = await api.listProviders({ q: 'banking' });
p.length; p.total; p.pages;          // 25, 1840, 74

for await (const provider of api.paginate('/providers', { q: 'banking', limit: 100 })) { … }
```

## 401 and 402 are different answers

```js
try {
  await api.whatCanIFix('stripe');
} catch (e) {
  if (e instanceof Unauthenticated) {
    e.resourceMetadata;   // https://apis.io/.well-known/oauth-protected-resource/api/v1
    e.scope;              // apis:pro
  } else if (e instanceof PaymentRequired) {
    e.tier;               // "business"
    e.plansUrl;
  }
}
```

A 401 is not a paywall — it is the way in. Collapsing the two is the most common way an agent gets
stuck on this API, and keeping them apart is most of why this client exists.

The challenge arrives under a non-standard header name (API Gateway reserves `WWW-Authenticate`
and renames it); `resourceMetadata` reads all three spellings so you never have to care.

## Rate limits

```js
api.lastRateLimit;   // RateLimit { tier: 'pro', limit: 5000, window: 86400 }
```

`429` is retried with the server's own `Retry-After`. `402` never is — a paywall will not become a
`200` by asking again.

## Generated, not hand-written

The 108 operation methods come from the OpenAPI documents apis.io publishes, emitted by the same
generator that produces the Python and Go clients — one spec parse, three targets, so they cannot
drift from each other or from the contract.

```bash
python3 ../python/generate.py          # regenerate all three
python3 ../python/generate.py --check  # non-zero if any is stale
```

Apache-2.0.
