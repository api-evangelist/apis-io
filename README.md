# APIs.io (apis-io)
APIs.io is an open source API search engine and directory that uses APIs.json files to discover, index, and catalog APIs across the web. Built on the APIs.json specification, it provides a searchable entry point for developers to find public APIs by keyword, resource, action, persona, domain, and schema. The platform indexes 779 providers, 3,188 APIs, 587 capabilities, 36,602 schemas, 49 event specs, 2,078 vocabularies, and 450 rulesets. It is maintained by Kin Lane, Nicolas Grenier, and Steven Willmott and supports both API producers (submitting APIs) and API consumers (discovering APIs). APIs.io uses a Spectral-powered rating system to evaluate API documentation quality.

**URL:** [Visit APIs.json URL](https://raw.githubusercontent.com/api-evangelist/apis-io/refs/heads/main/apis.yml)

**Run:** [Capabilities Using Naftiko](https://github.com/naftiko/fleet?utm_source=api-evangelist&utm_medium=readme&utm_campaign=company-api-evangelist&utm_content=repo)

## Tags:

 - API Aggregation, API Directory, API Discovery, API Indexing, API Rating, API Search, APIs.json, Search Engine

## Timestamps

- **Created:** 2026-03-26
- **Modified:** 2026-04-19

## APIs

### APIs.io Search API
The APIs.io Search API allows developers to search for APIs across all indexed APIs.json files using keywords or phrases, and to submit new APIs to the index by providing a valid APIs.json document. The API supports pagination, filtering, and returns results with name, description, tags, score, and URLs. Authentication is handled via the separate Authentication API which converts GitHub Personal Access Tokens into API keys.

**Human URL:** [https://apis.io/developer/documentation/](https://apis.io/developer/documentation/)

#### Tags:

 - API Discovery, API Indexing, API Search, APIs.json

#### Properties

- [Documentation](https://apis.io/developer/documentation/)
- [OpenAPI](https://raw.githubusercontent.com/api-evangelist/apis-io/refs/heads/main/openapi/apis-io-search-openapi.yaml)
- [Postman Collection](https://www.postman.com/api-evangelist/apis-io-api-evangelist-engine/collection/hn8xpmd/apis-io-search-api)
- [Authentication](https://apis.io/developer/authentication/)
- [Rate Limits](https://apis.io/developer/plans/)
- [Change Log](https://apis.io/developer/change-log/)
- [Status Page](https://www.postman.com/api-evangelist/apis-io/monitor/APIs-io-Search---Status~1ef6bc29-9da9-4040-b98b-cef03be1155e)
- [JSONSchema - Search Response Schema](https://raw.githubusercontent.com/api-evangelist/apis-io/refs/heads/main/json-schema/apis-io-search-search-schema.json)
- [JSONSchema - APIs.json Schema](https://raw.githubusercontent.com/api-evangelist/apis-io/refs/heads/main/json-schema/apis-io-search-ap-is-json-schema.json)

## Common Properties

- [Website](https://apis.io)
- [About](https://apis.io/about/)
- [Blog](https://apis.io/blog/)
- [Developer Portal](https://apis.io/developer/)
- [Developer Blog](https://apis.io/developer/blog/)
- [Getting Started](https://apis.io/developer/getting-started/)
- [Authentication](https://apis.io/developer/authentication/)
- [Plans](https://apis.io/developer/plans/)
- [Change Log](https://apis.io/developer/change-log/)
- [Release Notes](https://apis.io/developer/change-log/)
- [Versioning](https://apis.io/developer/versioning/)
- [Support](https://apis.io/developer/support/)
- [Terms of Service](https://apis.io/developer/terms-of-service/)
- [Privacy Policy](https://apis.io/developer/privacy-policy/)
- [GitHub Organization](https://github.com/api-search)
- [GitHub Repository](https://github.com/apisio/apis.io)
- [GitHub Repository - Search API](https://github.com/api-search/apis-io-search)
- [GitHub Repository - Search Engine](https://github.com/api-search/apis-io-engine)
- [GitHub Repository - Authentication API](https://github.com/api-search/apis-io-authentication)
- [GitHub Repository - Ratings API](https://github.com/api-search/apis-io-ratings)

## Features

| Name | Description |
|------|-------------|
| API Search | Full-text search across 3,000+ indexed APIs by keyword, resource, action, persona, domain, and schema using a cloud search engine. |
| APIs.json Indexing | Automatically indexes APIs.json files submitted by API producers to build a comprehensive, machine-readable catalog of API operations. |
| API Submission | API producers can submit their APIs to the index by providing a valid APIs.json document via the Search API POST endpoint or GitHub issues. |
| Spectral API Ratings | Spectral-powered quality rating system that evaluates API documentation completeness and scores APIs to help consumers identify high-quality APIs. |
| Microservice Architecture | Built as a set of microservices including Search, Engine, Authentication, Publishing, Tags, Rules, Properties, Maintainers, and Ratings APIs. |
| Topic Search Nodes | Specialized search nodes for domain-specific API discovery including AI, Healthcare, Banking, Payments, Weather, CRM, Cloud, and many more topic areas. |
| Open Source | The platform is open source, licensed under Apache-2.0, with all microservice APIs available on GitHub under the api-search organization. |

## Use Cases

| Name | Description |
|------|-------------|
| API Discovery | Developers can search for APIs relevant to their project by keyword, discovering APIs across thousands of providers without knowing where to look. |
| API Submission | API producers can submit their APIs.json files to ensure their APIs are discoverable in the index and properly cataloged with metadata. |
| Quality Assessment | Development teams use the Spectral ratings system to identify high-quality APIs and avoid poorly documented or unmaintained options. |
| Catalog Building | Platform teams use APIs.io as a reference implementation for building their own internal API catalogs using the APIs.json format. |
| Domain-Specific Search | Developers searching for APIs in specific domains (healthcare, finance, AI) can use topic-specific search nodes for more targeted discovery. |

## Integrations

| Name | Description |
|------|-------------|
| APIs.json | Core integration with the APIs.json specification for machine-readable API description and discovery across the web. |
| OpenAPI | APIs indexed in APIs.io reference OpenAPI specifications as a key property, linking consumers to technical API contracts. |
| Spectral | Spectral ruleset integration powers the APIs.io rating system, evaluating API documentation quality against standardized rules. |
| GitHub | GitHub integration for API submission via issues, source of truth for indexed APIs.json files, and authentication via Personal Access Tokens. |
| Postman | Postman public workspace integration for running and testing the APIs.io Search API via pre-built collections. |
| AWS API Gateway | The APIs.io Search API is deployed and managed through AWS API Gateway for scalable, managed API access. |

## Artifacts

Machine-readable API specifications organized by format.

### OpenAPI

- [APIs.io Search API](openapi/apis-io-search-openapi.yaml)

### JSON Schema

- [Search Response Schema](json-schema/apis-io-search-search-schema.json)
- [Meta Schema](json-schema/apis-io-search-meta-schema.json)
- [Link Schema](json-schema/apis-io-search-link-schema.json)
- [APIs.json Schema](json-schema/apis-io-search-ap-is-json-schema.json)
- [API Schema](json-schema/apis-io-search-api-schema.json)
- [Property Schema](json-schema/apis-io-search-property-schema.json)
- [Contact Schema](json-schema/apis-io-search-contact-schema.json)
- [Maintainer Schema](json-schema/apis-io-search-maintainer-schema.json)

### JSON Structure

- [Search Response Structure](json-structure/apis-io-search-search-structure.json)
- [APIs.json Structure](json-structure/apis-io-search-ap-is-json-structure.json)
- [API Structure](json-structure/apis-io-search-api-structure.json)
- [Property Structure](json-structure/apis-io-search-property-structure.json)

### JSON-LD

- [APIs.io Context](json-ld/apis-io-context.jsonld)

### Examples

- [Search Response Example](examples/apis-io-search-search-example.json)
- [APIs.json Example](examples/apis-io-search-ap-is-json-example.json)
- [API Example](examples/apis-io-search-api-example.json)
- [Property Example](examples/apis-io-search-property-example.json)

## Capabilities

Naftiko capabilities organized as shared per-API definitions composed into customer-facing workflows.

### Shared Per-API Definitions

- [APIs.io Search API](capabilities/shared/search-api.yaml) — 2 operations for API discovery and submission

### Workflow Capabilities

| Workflow | APIs Combined | Tools | Persona |
|----------|--------------|-------|---------|
| [API Discovery and Search](capabilities/api-discovery-search.yaml) | APIs.io Search API | 2 | API Developer, API Producer |

## Vocabulary

- [APIs.io Vocabulary](vocabulary/apis-io-vocabulary.yaml) — Unified taxonomy mapping 1 resource, 2 actions, 1 workflow, and 2 personas across operational (OpenAPI) and capability (Naftiko) dimensions

## Rules

- [APIs.io Spectral Rules](rules/apis-io-spectral-rules.yml) — 35 rules across 10 categories enforcing APIs.io API conventions

## Maintainers

**FN:** Kin Lane

**Email:** kin@apievangelist.com
