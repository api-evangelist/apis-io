---
name: watch-providers
description: Set up ongoing monitoring of the apis.io catalog using saved searches and lists — track a vendor set, get only what is new since last check, and watch for rating movement. Use for recurring vendor monitoring rather than one-off queries. Pro tier, with a free fallback.
license: CC-BY-NC-SA-4.0
---

# watch-providers

The stateful half of the catalog. Instead of re-running a query and diffing by hand, save it
server-side and ask what's new.

## When to use this skill

Use for "watch these vendors for me", "tell me what's new since last week", "monitor the
payments space", "keep an eye on our API dependencies". For a one-off change digest use
`track-api-changes`; for a point-in-time portfolio snapshot use `audit-api-estate`.

## The stateful endpoints — Pro

Base `https://apis.io/api/v1`, key as `x-api-key: <key>`. All `/me/*` routes return **402**
without a Pro or Business tier.

| Call | Purpose |
|---|---|
| `GET /me/searches` | Your saved searches. |
| `POST /me/searches` | Save a query so it can be re-run and diffed. |
| `GET /me/searches/{id}/results` | Run it now, full result set. |
| `GET /me/searches/{id}/net_new` | **Only what appeared since the last run.** |
| `DELETE /me/searches/{id}` | Remove it. |
| `GET /me/lists` | Your provider lists. |
| `POST /me/lists` | Create a list — a named vendor set. |
| `GET /me/lists/{id}` · `POST /me/lists/{id}/entries` | Read and add members. |

`net_new` is the point of the whole surface. A saved search plus `net_new` is a proper watch:
the server remembers what you'd already seen, so you get additions rather than a full list to
diff.

```bash
# Save a watch
curl -s -X POST -H "x-api-key: $APISIO_KEY" -H 'Content-Type: application/json' \
  -d '{"name":"EU payments providers","query":{"q":"payments","region":"europe"}}' \
  "https://apis.io/api/v1/me/searches"

# Later — only what is new
curl -s -H "x-api-key: $APISIO_KEY" \
  "https://apis.io/api/v1/me/searches/$ID/net_new" | jq
```

Inspect the first response with `jq 'keys'` — the `/me/*` request and response shapes are
not pinned in the published OpenAPI.

MCP equivalents (`https://apis.io/mcp`): `save_search`, `list_saved_searches`,
`run_saved_search`, `saved_search_net_new`, `delete_saved_search`, `create_list`,
`add_to_list`, `get_list`, `list_lists`, `delete_list`.

## Free fallback — a local watch file

Without a Pro key you can run the same pattern yourself. Keep a snapshot, diff on each run.

```bash
WATCH=~/.apis-io-watch.json
QUERY="payments"

curl -s "https://apis.io/api/v1/providers?q=$QUERY&limit=100" \
  | jq '[.data[] | {slug, name}]' > /tmp/now.json

# Providers that weren't there last time
if [ -f "$WATCH" ]; then
  jq -n --slurpfile old "$WATCH" --slurpfile new /tmp/now.json \
    '($new[0] - $old[0]) | map(.slug)'
else
  echo "first run — baseline saved"
fi
mv /tmp/now.json "$WATCH"
```

For score movement, snapshot the free `band` and `composite` per watched provider:

```bash
for p in twilio sendgrid stripe; do
  curl -s "https://apis.io/api/v1/resolve?identifier=$p" | jq -c '{slug, band, composite}'
done > /tmp/scores.jsonl
```

Diff that file between runs and you have movers without a Pro key. Say plainly that it's a
locally-computed diff, not the catalog's own change feed.

## Cadence

The catalog rescores on a build cadence, not continuously. `scored_at` from
`/providers/{slug}/evidence` tells you when a provider was last scored. Polling more often
than the build cadence produces noise, not signal — check `scored_at` before reporting that
nothing changed.

## Output format

A digest, not a dump:

- **New** — what entered the watched set, with what it publishes.
- **Moved** — band or composite changes, with the delta and direction.
- **Gone** — anything that dropped out, and whether that's a delisting or a re-slug.
- **Act on** — the one or two items that warrant attention: a dependency slipping a band, a
  strong new entrant in a category you buy in.

If nothing changed, say that in one line. A watch that reports noise every run gets ignored.

## Errors and tiering

`/me/*` returns HTTP **402** with `error`, `detail`, `tier`, `plans`. `GET /export/{dataset}`
is **Business** tier. Surface the upgrade link, fall back to the local watch above, and label
which mode produced the digest.

## Related skills

- `track-api-changes` — the one-off change digest.
- `audit-api-estate` — the snapshot a watch monitors over time.
- `benchmark-against-peers` — when a watched provider slips behind its peers.
- `shortlist-vendors` — when a slip means finding a replacement.
