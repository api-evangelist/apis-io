---
name: resolve-provider
description: Turn a domain, URL, company name, or GitHub org into an apis.io provider slug, with its quality band and composite score. Use first whenever the user names a company rather than a catalog slug — which is almost always.
license: CC-BY-NC-SA-4.0
---

# resolve-provider

Every other apis.io skill needs a slug. Users give you `stripe.com`, a docs URL, or "that
email company". This converts one into the other, free, in a single call.

## When to use this skill

Use as step zero for anything provider-shaped: "is Stripe in the catalog", "score
twilio.com", "what does github.com publish". Also use it to sanity-check a slug you guessed —
a wrong slug produces a confident 404 downstream.

## The call

```
GET https://apis.io/api/v1/resolve?identifier=<value>
```

**Free**, no key. The parameter is `identifier` — not `q`. Passing `q` returns:

```json
{ "error": "bad_request", "detail": "Pass ?identifier= a domain, URL, or github org." }
```

It accepts a bare domain, a full URL, a GitHub org, or a brand slug:

```bash
curl -s "https://apis.io/api/v1/resolve?identifier=twilio.com"
# {"slug":"twilio","name":"Twilio","website":"https://console.twilio.com",
#  "band":"exemplar","composite":73.8,"match":"identity_link"}

curl -s "https://apis.io/api/v1/resolve?identifier=sendgrid"
# {"slug":"sendgrid","name":"SendGrid","website":"https://sendgrid.com/en-us",
#  "band":"exemplar","composite":77.4,"match":"brand_slug"}
```

## Read `match` — it tells you how much to trust the hit

| `match` | Meaning | Trust |
|---|---|---|
| `identity_link` | A declared identity link on the provider's own record matched. | Strongest. |
| `brand_slug` | The input matched a catalog slug by name. | Good, but a namesake is possible — confirm the `website`. |

When `match` is `brand_slug` and the name is generic, show the user the resolved `website`
and confirm before acting on it.

## The free score

`resolve` hands back `band` and `composite` **at no tier** — `/providers/{slug}/rating` is
Pro. If all you need is "how good is this provider", this is the free answer. Bands run
`exemplar` › `strong` › `developing` › `thin` › `emerging` › `minimal`; see
`GET /ratings/rubric` (also free) for the cut points and what each band means.

## When it misses

A 404 or empty result means the company is not profiled under that identifier. Fall back to
keyword search before concluding it's absent:

```bash
curl -s "https://apis.io/api/v1/providers?q=acme&limit=5" | jq '.data[] | {slug, name}'
```

If that is also empty, the company genuinely isn't in the catalog. Say so — and point the
user at https://apis.io/add/ to submit it, rather than guessing a slug.

## Recipe — resolve, then act

```bash
SLUG=$(curl -s "https://apis.io/api/v1/resolve?identifier=$1" | jq -r '.slug // empty')
[ -z "$SLUG" ] && { echo "not in catalog"; exit 1; }
curl -s "https://apis.io/api/v1/providers/$SLUG/artifacts" | jq '.artifact_types'
```

MCP equivalent (`https://apis.io/mcp`): `resolve`.

## Related skills

- `discover-apis-io` — the conventions every apis.io skill assumes.
- `find-api` · `integrate-provider` · `score-my-api` — all take the slug this produces.
- `verify-provenance` — how the catalog knows what it claims about this provider.
