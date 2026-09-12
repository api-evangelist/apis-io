# Licensing

This repository holds two different kinds of thing, and they are licensed differently.

| What | Where | License |
|---|---|---|
| **Artifacts** — OpenAPI, AsyncAPI, Arazzo, overlays, Spectral rulesets, conformance profiles, JSON Schema, agent cards, plans, rate limits, and every other description of the API | everywhere except `sdk/` | [CC BY-NC-SA 4.0](LICENSE) |
| **Code** — the Python, JavaScript and Go clients and the CLI | [`sdk/`](sdk/) | [Apache 2.0](sdk/LICENSE) |

This is the API Evangelist network convention, not a choice made for this repo alone.

## Why the split

The artifacts are the editorial work — what API Evangelist observed, described and published
about this API. Share and adapt them, credit the source, share alike, and don't resell them.

The code exists to be embedded in other people's software, where a non-commercial clause would
make it unusable for the exact purpose it was written for. Apache 2.0, including its patent
grant, is the standard for that and carries no obligations back to us.

## What this replaced

Until 2026-09-12 this repository declared **MIT**, by pointing at the `LICENSE` file of
`github.com/apisio/apis.io`. That is the *original* apis.io repository, lost to us with the Red
Hat and IBM acquisitions and last pushed 2016-05-31 — we have read-only access and cannot change
anything there. The pointer resolved with a 200, so no link check ever flagged it, and this
repository itself carried no license file at all.
