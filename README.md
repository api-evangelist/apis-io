# APIs.io

<!-- API-EVANGELIST-PROVENANCE:BEGIN -->
> ### About this repository
>
> **This is not our API.** This repository is an independent, third-party profile of a company's
> **publicly available** API surface, maintained by [API Evangelist](https://apievangelist.com).
> API Evangelist does not operate, host, resell, or support this company's APIs, and is not
> affiliated with or endorsed by the company unless stated on the profile.
>
> **Where the information came from.** Everything here is assembled from material a member of the
> public can reach with a browser and no credentials — the company's own website, developer portal
> and documentation, the specifications it publishes for public use (OpenAPI, AsyncAPI, JSON Schema,
> `apis.json`, `llms.txt` and similar), its public repositories, and its public status, pricing and
> changelog pages. **Nothing here is obtained by breaching a system, defeating an access control, or
> using credentials of any kind.**
>
> **The rating is an independent assessment.** The Kin Score and Agent Readiness rating are
> independently calculated scores of a company's *public* API artifacts, produced by API Evangelist
> against a published rubric. They are not certifications, endorsements, security assessments, or
> audits, and they score published artifacts — not the quality, safety, or security of the software.
>
> **Corrections, re-scores, and removal are free.** No partnership, contract, or purchase is
> required, and you do not need to justify the request.
>
> - **Something wrong?** Open an issue on this repository, or email
>   [info@apievangelist.com](mailto:info@apievangelist.com).
> - **Published something new?** Ask for a re-score and we will re-run the rating.
> - **Want the listing taken down?** Say so and we will honor it. The profile is reduced to your
>   company name, a factual description, and a link to your own site, and the company is recorded as
>   **unrated** — never scored zero for having asked.
>
> **Response times.** Acknowledgement within **one business day**; removal or restriction within
> **two business days**; corrections and re-scores within **five business days**.
>
> **Not from the company, and here with a question?** You are welcome here — we would rather be the
> front line and point you the right way than have a good report go nowhere. What this repository
> can answer is narrow, though, so it is worth knowing who you are actually looking for:
>
> - **A question about how the API works, an account, billing, or a bug in the service** — that is
>   the company's own support, not us. We profile this API; we do not operate it and cannot see
>   your account.
> - **A bug in an open-source project we only catalog** — file it on that project's own repository.
>   This has happened with a real and correct bug report that reached us instead of the people who
>   could fix it, which helped nobody.
> - **Anything about this listing itself** — the description, the tags, the rating, a missing or
>   wrong artifact — is ours. Open an issue here.
> - **Not sure, or something general about API Evangelist or APIs.io** — open an issue on the
>   [APIs.io Inbox](https://github.com/api-search/inbox) and we will route it.
>
> **This repository contains no software, and we will never ask you to download anything.** There is
> no build, release, installer, or binary here — only text and machine-readable API descriptions, so
> there is nothing here that can be "corrupt" or need "repairing". Any issue, comment, or email
> claiming otherwise and offering a download link is not from us and is hostile. Do not follow the
> link; it is a lure. Report it to GitHub and, if you like, tell us at
> [info@apievangelist.com](mailto:info@apievangelist.com) so we can take it down.
>
> **On a security or compliance team?** Email
> [info@apievangelist.com](mailto:info@apievangelist.com) with *security* in the subject line and
> you will get a person, not a form. We will tell you exactly which public URLs this profile was
> built from so your team can see the same surface we did, and we will take the listing down on
> request while you work through it.
>
> Full detail: **[Where this data comes from](https://apievangelist.com/about/where-our-data-comes-from)**
<!-- API-EVANGELIST-PROVENANCE:END -->

APIs.io is an open-source API search engine and federated discovery network built on the APIs.json specification. It indexes API providers and their individual APIs across the public internet along with the machine-readable artifacts they publish — OpenAPI, AsyncAPI, GraphQL, Arazzo workflows, Postman collections, JSON Schema, JSON-LD contexts, Spectral rulesets, vocabularies, OAuth scopes, plans, rate limits and FinOps profiles — and lets developers and agents search that catalog by keyword, capability, tag, industry, region, artifact type and quality band. As of August 2026 the network published roughly 26,414 providers, 109,100 APIs and 120,595 schemas across 71 industries and 77 curated areas. Every provider is scored with the Kin Score, a 0–100 composite across six weighted facets plus a standalone agent-readiness score. The same read-only OpenAPI 3.1 contract powers three surfaces — a REST API at https://apis.io/api/v1, a Streamable-HTTP MCP server at https://apis.io/mcp, and a set of published Agent Skills — alongside an RFC 9727 api-catalog linkset, an llms.txt and an APIs.json self-description. It is maintained by API Evangelist and serves both API producers submitting profiles and API consumers discovering APIs.

**Areas:** API Aggregation · API Directory · API Discovery · API Indexing · API Rating · API Search · APIs.json · Search Engines · API Catalog · Agent Discovery · MCP · Agent Skills

## APIs.io on APIs.io

Everything profiled for APIs.io is published on APIs.io rather than in this repository. Start at the provider page — **[apis.io/providers/apis-io/](https://apis.io/providers/apis-io/)** — or go straight to one of the APIs or properties below.

### APIs (21)

- [APIs.io Submit API](https://apis.io/apis/apis-io/apisio-submit-api/) — Discover a domain's machine-readable API surface and submit a provider for review — the Add-API door, documented first-party from the serving Lambda.
- [APIs.io Areas API](https://apis.io/apis/apis-io/apis-io-areas-api/) — The API Evangelist areas taxonomy — curated topic collections (authentication, webhooks, payments, …), each a scored provider index with its own site. Pro.
- [APIs.io Artifact Types API](https://apis.io/apis/apis-io/apis-io-artifact-types-api/) — First-class, per-type artifact collections (OpenAPI, AsyncAPI, Arazzo, Postman, JSON Schema, and more). Each path filters and normalizes one artifact type…
- [APIs.io Industries API](https://apis.io/apis/apis-io/apis-io-industries-api/) — Industry verticals grouping providers across the catalog.
- [APIs.io Insights API](https://apis.io/apis/apis-io/apis-io-insights-api/) — Demand-side intelligence — what 6,572 companies (Fortune 1000 + API providers) build, buy, and hire for around APIs, data, and AI, derived from job…
- [APIs.io Providers API](https://apis.io/apis/apis-io/apis-io-providers-api/) — Organizations publishing APIs on the network.
- [APIs.io Ratings API](https://apis.io/apis/apis-io/apis-io-ratings-api/) — The APIs.io API rating system — a 0–100 composite score, five bands, a trend marker, and six weighted facets measuring how complete, governed, and…
- [APIs.io Regions API](https://apis.io/apis/apis-io/apis-io-regions-api/) — Geographic regions grouping providers across the catalog.
- [APIs.io Search API](https://apis.io/apis/apis-io/apis-io-search-api/) — Search using a cloud search engine.
- [APIs.io Synthesis API](https://apis.io/apis/apis-io/apis-io-synthesis-api/) — Decision-grade composites over the catalog — provider comparison, gap analysis, catalog change feed, and recommended-stack design. Pro.
- [APIs.io Tags API](https://apis.io/apis/apis-io/apis-io-tags-api/) — The tag taxonomy, with network-wide ranking metadata.
- [APIs.io Cohorts API](https://apis.io/apis/apis-io/apis-io-cohorts-api/) — Any scored population of providers — a tag, industry, region, area, or VC portfolio — with the distribution, rankings, facet scores, and capability matrix…
- [APIs.io Editorial API](https://apis.io/apis/apis-io/apis-io-editorial-api/) — Story leads mined from catalog movement (owner tier). 1 operation of the APIs.io API, split out by tag so this surface is documented, rated, and governed on…
- [APIs.io Export API](https://apis.io/apis/apis-io/apis-io-export-api/) — Bulk dataset pulls of the catalog — ratings and providers as one download (Business tier). 2 operations of the APIs.io API, split out by tag so this surface…
- [APIs.io Resolve & Enrich API](https://apis.io/apis/apis-io/apis-io-resolve-enrich-api/) — Agent ergonomics — resolve any identifier (domain, URL, GitHub org) to a provider, and enrich a provider in one call by choosing field groups. 2 operations…
- [APIs.io Saved Workspace API](https://apis.io/apis/apis-io/apis-io-saved-workspace-api/) — Saved searches and provider lists for a signed-in apis.io API key — save a query, re-run it, and watch what is net-new. 10 operations of the APIs.io API,…
- [APIs.io Venture Capital API](https://apis.io/apis/apis-io/apis-io-venture-capital-api/) — Venture-capital firms as a first-class entity — fund identity plus a network-matched, rated portfolio graph, and the reverse edge from a provider to the VCs…
- [APIs.io Provider Control API](https://apis.io/apis/apis-io/apis-io-provider-control-api/) — Claim, correct and improve your own listing. Most operations require the Influence plan; reporting that our data is wrong is free and always will be.
- [APIs.io Watches API](https://apis.io/apis/apis-io/apis-io-watches-api/) — The Watches API from APIs.io — 0 operation(s) for watches.
- [APIs.io APIs API](https://apis.io/apis/apis-io/apis-io-apis-api/) — Individual APIs, each owned by a provider and described by artifacts.
- [APIs.io Prices API](https://apis.io/apis/apis-io/apis-io-prices-api/) — The per-call price map for metered resources, and the bands it is built from.

### Published properties

Each property below is a page on APIs.io carrying the machine-readable artifact and what it says.

#### Arazzo workflows (4)

Multi-step workflows that chain operations into a business task.

- [APIs.io Compare Keyword Coverage](https://apis.io/arazzos/apis-io/apis-io-compare-keyword-coverage-workflow/)
- [APIs.io Paginate Search Results](https://apis.io/arazzos/apis-io/apis-io-paginate-search-results-workflow/)
- [APIs.io Search APIs by Keyword](https://apis.io/arazzos/apis-io/apis-io-search-apis-workflow/)
- [APIs.io Submit and Verify API](https://apis.io/arazzos/apis-io/apis-io-submit-and-verify-api-workflow/)

#### AsyncAPI (1)

Event-driven and webhook contracts.

- [APIs.io Watch Events](https://apis.io/asyncapis/apis-io/apis-io-watch-events-asyncapi/)

#### Event channels (1)

Individual events and webhooks the provider emits.

- [/](https://apis.io/channels/apis-io/watchdelivery/)

#### MCP servers (2)

Model Context Protocol servers that expose the API to agents.

- [APIs.io API catalog MCP server](https://apis.io/servers/apis-io/apis-io/)
- [Moved to /providers/apis-io/](https://apis.io/servers/apis-io/mcp/)

#### Agentic access (1)

Which operations an agent can call, which act, and which need a human in the loop.

- [Apis Io Agentic Access](https://apis.io/agentic-access/apis-io/apis-io-agentic-access/)

#### JSON Schema (13)

The data models the API reads and writes.

- [AddAPIsJSON](https://apis.io/schemas/apis-io/apis-io-search-add-ap-is-json/)
- [APIs](https://apis.io/schemas/apis-io/apis-io-search-ap-is/)
- [APIsJSON](https://apis.io/schemas/apis-io/apis-io-search-ap-is-json/)
- [API](https://apis.io/schemas/apis-io/apis-io-search-api/)
- [Contact](https://apis.io/schemas/apis-io/apis-io-search-contact/)
- [Include](https://apis.io/schemas/apis-io/apis-io-search-include/)
- [Link](https://apis.io/schemas/apis-io/apis-io-search-link/)
- [Maintainer](https://apis.io/schemas/apis-io/apis-io-search-maintainer/)
- [Meta](https://apis.io/schemas/apis-io/apis-io-search-meta/)
- [metaInformation](https://apis.io/schemas/apis-io/apis-io-search-meta-information/)
- [Property](https://apis.io/schemas/apis-io/apis-io-search-property/)
- [Search](https://apis.io/schemas/apis-io/apis-io-search-search/)
- [Tag](https://apis.io/schemas/apis-io/apis-io-search-tag/)

#### JSON Structure (13)

Data models expressed in JSON Structure.

- [Apis Io Search Add Ap Is Json Structure](https://apis.io/json-structure/apis-io/apis-io-search-add-ap-is-json-structure/)
- [Apis Io Search Ap Is Json Structure](https://apis.io/json-structure/apis-io/apis-io-search-ap-is-json-structure/)
- [Apis Io Search Ap Is Structure](https://apis.io/json-structure/apis-io/apis-io-search-ap-is-structure/)
- [Apis Io Search Api Structure](https://apis.io/json-structure/apis-io/apis-io-search-api-structure/)
- [Apis Io Search Contact Structure](https://apis.io/json-structure/apis-io/apis-io-search-contact-structure/)
- [Apis Io Search Include Structure](https://apis.io/json-structure/apis-io/apis-io-search-include-structure/)
- [Apis Io Search Link Structure](https://apis.io/json-structure/apis-io/apis-io-search-link-structure/)
- [Apis Io Search Maintainer Structure](https://apis.io/json-structure/apis-io/apis-io-search-maintainer-structure/)
- [Apis Io Search Meta Information Structure](https://apis.io/json-structure/apis-io/apis-io-search-meta-information-structure/)
- [Apis Io Search Meta Structure](https://apis.io/json-structure/apis-io/apis-io-search-meta-structure/)
- [Apis Io Search Property Structure](https://apis.io/json-structure/apis-io/apis-io-search-property-structure/)
- [Apis Io Search Search Structure](https://apis.io/json-structure/apis-io/apis-io-search-search-structure/)
- [Apis Io Search Tag Structure](https://apis.io/json-structure/apis-io/apis-io-search-tag-structure/)

#### JSON-LD (1)

Linked-data contexts for the provider's vocabulary.

- [Apis Io Context](https://apis.io/jsonld/apis-io/apis-io-context/)

#### Vocabulary (1)

The provider's domain terms, defined.

- [Apis Io Vocabulary](https://apis.io/vocabularies/apis-io/apis-io-vocabulary/)

#### Examples (13)

Example requests and responses.

- [Apis Io Search Add Ap Is Json Example](https://apis.io/examples/apis-io/apis-io-search-add-ap-is-json-example/)
- [Apis Io Search Ap Is Example](https://apis.io/examples/apis-io/apis-io-search-ap-is-example/)
- [Apis Io Search Ap Is Json Example](https://apis.io/examples/apis-io/apis-io-search-ap-is-json-example/)
- [Apis Io Search Api Example](https://apis.io/examples/apis-io/apis-io-search-api-example/)
- [Apis Io Search Contact Example](https://apis.io/examples/apis-io/apis-io-search-contact-example/)
- [Apis Io Search Include Example](https://apis.io/examples/apis-io/apis-io-search-include-example/)
- [Apis Io Search Link Example](https://apis.io/examples/apis-io/apis-io-search-link-example/)
- [Apis Io Search Maintainer Example](https://apis.io/examples/apis-io/apis-io-search-maintainer-example/)
- [Apis Io Search Meta Example](https://apis.io/examples/apis-io/apis-io-search-meta-example/)
- [Apis Io Search Meta Information Example](https://apis.io/examples/apis-io/apis-io-search-meta-information-example/)
- [Apis Io Search Property Example](https://apis.io/examples/apis-io/apis-io-search-property-example/)
- [Apis Io Search Search Example](https://apis.io/examples/apis-io/apis-io-search-search-example/)
- [Apis Io Search Tag Example](https://apis.io/examples/apis-io/apis-io-search-tag-example/)

#### Collections (22)

Postman and Open Collection request collections.

- [.io Search APIs API](https://apis.io/collections/apis-io/open-apis-io-apis-api/)
- [.io Search APIs Areas API](https://apis.io/collections/apis-io/open-apis-io-areas-api/)
- [.io Search APIs Artifact Types API](https://apis.io/collections/apis-io/open-apis-io-artifact-types-api/)
- [.io Search APIs Industries API](https://apis.io/collections/apis-io/open-apis-io-industries-api/)
- [.io Search APIs Insights API](https://apis.io/collections/apis-io/open-apis-io-insights-api/)
- [.io Search APIs Providers API](https://apis.io/collections/apis-io/open-apis-io-providers-api/)
- [.io Search APIs Ratings API](https://apis.io/collections/apis-io/open-apis-io-ratings-api/)
- [.io Search APIs Regions API](https://apis.io/collections/apis-io/open-apis-io-regions-api/)
- [.io APIs Search API](https://apis.io/collections/apis-io/open-apis-io-search-api/)
- [.io Search APIs Synthesis API](https://apis.io/collections/apis-io/open-apis-io-synthesis-api/)
- [.io Search APIs Tags API](https://apis.io/collections/apis-io/open-apis-io-tags-api/)
- [.io Search APIs API](https://apis.io/collections/apis-io/postman-apis-io-apis-api/)
- [.io Search APIs Areas API](https://apis.io/collections/apis-io/postman-apis-io-areas-api/)
- [.io Search APIs Artifact Types API](https://apis.io/collections/apis-io/postman-apis-io-artifact-types-api/)
- [.io Search APIs Industries API](https://apis.io/collections/apis-io/postman-apis-io-industries-api/)
- [.io Search APIs Insights API](https://apis.io/collections/apis-io/postman-apis-io-insights-api/)
- [.io Search APIs Providers API](https://apis.io/collections/apis-io/postman-apis-io-providers-api/)
- [.io Search APIs Ratings API](https://apis.io/collections/apis-io/postman-apis-io-ratings-api/)
- [.io Search APIs Regions API](https://apis.io/collections/apis-io/postman-apis-io-regions-api/)
- [.io APIs Search API](https://apis.io/collections/apis-io/postman-apis-io-search-api/)
- [.io Search APIs Synthesis API](https://apis.io/collections/apis-io/postman-apis-io-synthesis-api/)
- [.io Search APIs Tags API](https://apis.io/collections/apis-io/postman-apis-io-tags-api/)

#### Overlays (32)

OpenAPI overlays, including conversational phrasing for each operation.

- [Apis Io Apis Api Overlay](https://apis.io/overlays/apis-io/apis-io-apis-api-overlay/)
- [Apis Io Apis Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-apis-api-phrasing-overlay/)
- [Apis Io Areas Api Overlay](https://apis.io/overlays/apis-io/apis-io-areas-api-overlay/)
- [Apis Io Areas Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-areas-api-phrasing-overlay/)
- [Apis Io Artifact Types Api Overlay](https://apis.io/overlays/apis-io/apis-io-artifact-types-api-overlay/)
- [Apis Io Artifact Types Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-artifact-types-api-phrasing-overlay/)
- [Apis Io Cohorts Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-cohorts-api-phrasing-overlay/)
- [Apis Io Editorial Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-editorial-api-phrasing-overlay/)
- [Apis Io Export Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-export-api-phrasing-overlay/)
- [Apis Io Industries Api Overlay](https://apis.io/overlays/apis-io/apis-io-industries-api-overlay/)
- [Apis Io Industries Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-industries-api-phrasing-overlay/)
- [Apis Io Insights Api Overlay](https://apis.io/overlays/apis-io/apis-io-insights-api-overlay/)
- [Apis Io Insights Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-insights-api-phrasing-overlay/)
- [Apis Io Prices Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-prices-api-phrasing-overlay/)
- [Apis Io Provider Control Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-provider-control-api-phrasing-overlay/)
- [Apis Io Providers Api Overlay](https://apis.io/overlays/apis-io/apis-io-providers-api-overlay/)
- [Apis Io Providers Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-providers-api-phrasing-overlay/)
- [Apis Io Ratings Api Overlay](https://apis.io/overlays/apis-io/apis-io-ratings-api-overlay/)
- [Apis Io Ratings Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-ratings-api-phrasing-overlay/)
- [Apis Io Regions Api Overlay](https://apis.io/overlays/apis-io/apis-io-regions-api-overlay/)
- [Apis Io Regions Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-regions-api-phrasing-overlay/)
- [Apis Io Resolve Enrich Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-resolve-enrich-api-phrasing-overlay/)
- [Apis Io Saved Workspace Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-saved-workspace-api-phrasing-overlay/)
- [Apis Io Search Api Overlay](https://apis.io/overlays/apis-io/apis-io-search-api-overlay/)
- [Apis Io Search Api Phrasing Overlay](https://apis.io/overlays/apis-io/apis-io-search-api-phrasing-overlay/)
- …and 7 more published on APIs.io

#### Governance rules (2)

Spectral rulesets for the provider's contracts.

- [APIs.io — jsonschema rules](https://apis.io/rules/apis-io/apis-io-jsonschema-spectral-rules/)
- [APIs.io API Rules](https://apis.io/rules/apis-io/apis-io-spectral-rules/)

#### Security (3)

Authentication, trust centre, and vulnerability disclosure.

- [Apis Io Authentication](https://apis.io/security/apis-io/apis-io-authentication/)
- [Apis Io Domain Security](https://apis.io/security/apis-io/apis-io-domain-security/)
- [Apis Io Vulnerability Disclosure](https://apis.io/security/apis-io/apis-io-vulnerability-disclosure/)

#### OAuth scopes (1)

The permissions the API asks for.

- [Apis Io Scopes](https://apis.io/scopes/apis-io/apis-io-scopes/)

#### Plans and pricing (1)

Published plans, tiers and prices.

- [Apis Io Plans Pricing](https://apis.io/plans/apis-io/apis-io-plans-pricing/)

#### Rate limits (1)

Published request limits.

- [Apis Io Rate Limits](https://apis.io/rate-limits/apis-io/apis-io-rate-limits/)

#### FinOps (1)

What the API costs to run, by operation.

- [Apis Io Finops](https://apis.io/finops/apis-io/apis-io-finops/)

## Where to find this API

Links to the company's own pages. This repository publishes no copy of their specifications — the canonical document is theirs and lives at the URLs below.

- [Website](https://apis.io)
- [Documentation](https://apis.io/developer/)
- [Getting started](https://apis.io/developer/getting-started/)
- [API reference](https://apis.io/developer/api/)
- [Pricing](https://apis.io/developer/plans/)
- [Sign up](https://apis.io/developer/account)
- [Support](https://apis.io/support/)
- [Changelog](https://apis.io/changelog/)
- [Blog](https://apis.io/blog/)
- [Security](https://apis.io/developer/security)
- [Terms of service](https://apis.io/terms/)
- [Privacy policy](https://apis.io/privacy/)
- [GitHub](https://github.com/api-search)
- [Status](https://www.postman.com/api-evangelist/apis-io/monitor/APIs-io-Search---Status~1ef6bc29-9da9-4040-b98b-cef03be1155e)

## API Evangelist rating

**Kin Score 93.8** — exemplar · rubric 0.25.0 · scored 2026-10-23

| Facet | Score |
|---|---|
| Discoverability | 88.3 |
| Contract quality | 71.5 |
| Contract governance | 84.8 |
| Operational transparency | 76.3 |
| Developer ergonomics | 95.2 |
| Access clarity | 76.3 |

**Agent readiness 78.7** — agent-native

| Agent-readiness dimension | Result |
|---|---|
| Spec Presence | yes |
| Agentic Access | derived (partial credit) |
| Reversibility Documented | documented (partial credit) |
| MCP Server | verified |
| Auth Clarity | served (partial credit) |
| Idempotency | verified |
| Error Semantics | verified |
| OpenAPI Examples | partial |
| Rate Limit Signal | documented (partial credit) |
| Event Surface Described | yes |
| Agent Skills | yes |
| Well Known Catalog | yes |
| Consent Identity | yes |
| Agent Card | near-conformant (partial credit) |
| Dry Run Mode | — |
| Delegated Identity | served (partial credit) |
| Protected Resource Metadata | verified |
| Dynamic Client Registration | yes |
| Agentic Commerce | — |
| Pagination Ratio | paginated |
| Operation Distinctiveness | distinct |

**Regulatory alignment 37.7** — Horizontal (data, software, accessibility, platform)

The rubric is published at [github.com/api-evangelist/kin-score](https://github.com/api-evangelist/kin-score). The per-check breakdown behind these numbers — which checks were earned, partial or missed — along with score history and how this provider compares to its peers, is available at [apis.io/providers/apis-io/](https://apis.io/providers/apis-io/).

## How this profile is made

API Evangelist profiles a company's public API surface the way a developer would find it: the website, developer portal and documentation, the specifications it publishes, its public repositories, and its pricing, status and changelog pages. From that it derives the properties above — contracts split per API, workflows, schemas, collections, governance rules, plans and rate limits — and scores them against the published [Kin Score rubric](https://github.com/api-evangelist/kin-score).

The artifacts are published on [APIs.io](https://apis.io), not in this repository. This repository is the public record for APIs.io: the place to say something is wrong, missing or out of date, and to ask for a re-score or a removal.

## Open an issue

- **Something about this listing** — a wrong description, a missing API, a stale artifact or a question about the rating: [open an issue on this repository](https://github.com/api-evangelist/apis-io/issues/new).
- **A new API, or one that is not in the catalog yet** — [submit it on APIs.io](https://apis.io/add/).
- **Anything else** — [the APIs.io inbox](https://github.com/api-search/inbox/issues/new) or [info@apievangelist.com](mailto:info@apievangelist.com).
