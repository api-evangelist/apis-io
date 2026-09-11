"""apis.io operation bindings — GENERATED, DO NOT EDIT.

Regenerate with `python3 generate.py` from the OpenAPI documents in
`all/apis-io/openapi/_original/` — the documents apis.io publishes, not the refined mirror.

108 operations across 18 documents, generated 2026-09-11.

Every method is a thin call through `Client.request`. Collection endpoints return a `Page`
(a list, with `.meta`/`.total`/`.pages`); everything else returns the parsed body.
"""

from __future__ import annotations

from typing import Any

__all__ = ["Operations"]


class Operations:
    """Mixin carrying one method per published operation. `Client` inherits it."""

    def add_to_list(self, id: str, body: Any = None, **params: Any) -> Any:
        """Add providers/APIs to a list.

        ``POST /me/lists/{id}/entries``
        """
        return self.request("POST", f"/me/lists/{id}/entries", params=params, json=body)

    def claim_listing(self, slug: str, body: Any = None, **params: Any) -> Any:
        """Create or return your claim on this listing

        ``POST /providers/{slug}/claim``
        """
        return self.request("POST", f"/providers/{slug}/claim", params=params, json=body)

    def compare_cohorts(self, **params: Any) -> Any:
        """Two cohorts side by side (Pro).

        Query parameters: a, b

        ``GET /cohorts/compare``
        """
        return self.get("/cohorts/compare", **params)

    def compare_providers(self, **params: Any) -> Any:
        """Compare providers side by side (Pro).

        Query parameters: providers

        ``GET /compare``
        """
        return self.get("/compare", **params)

    def correct_facts(self, slug: str, body: Any = None, **params: Any) -> Any:
        """Create or update your pending fact correction for this listing

        ``POST /providers/{slug}/facts``
        """
        return self.request("POST", f"/providers/{slug}/facts", params=params, json=body)

    def create_list(self, body: Any = None, **params: Any) -> Any:
        """Create a named, persistent list.

        ``POST /me/lists``
        """
        return self.request("POST", "/me/lists", params=params, json=body)

    def create_saved_search(self, body: Any = None, **params: Any) -> Any:
        """Create a saved search.

        ``POST /me/searches``
        """
        return self.request("POST", "/me/searches", params=params, json=body)

    def delete_list(self, id: str, **params: Any) -> Any:
        """Delete a list you own.

        ``DELETE /me/lists/{id}``
        """
        return self.delete(f"/me/lists/{id}", **params)

    def delete_saved_search(self, id: str, **params: Any) -> Any:
        """Delete a saved search you own.

        ``DELETE /me/searches/{id}``
        """
        return self.delete(f"/me/searches/{id}", **params)

    def dispute_finding(self, slug: str, body: Any = None, **params: Any) -> Any:
        """Dispute something the rating says about this provider

        ``POST /providers/{slug}/dispute``
        """
        return self.request("POST", f"/providers/{slug}/dispute", params=params, json=body)

    def enrich_provider(self, **params: Any) -> Any:
        """Enrich a provider in one call, choosing field groups.

        Query parameters: fields, id

        ``GET /enrich``
        """
        return self.get("/enrich", **params)

    def export_dataset(self, **params: Any) -> Any:
        """Export a whole dataset in one pull.

        Query parameters: co_brand

        ``GET /export``
        """
        return self.get("/export", **params)

    def export_named_dataset(self, dataset: str, **params: Any) -> Any:
        """Export one named dataset.

        Query parameters: co_brand

        ``GET /export/{dataset}``
        """
        return self.get(f"/export/{dataset}", **params)

    def export_stack(self, **params: Any) -> Any:
        """Export a designed stack as APIs.json.

        Query parameters: capabilities, region

        ``GET /stack/export``
        """
        return self.get("/stack/export", **params)

    def find_rating_movers(self, **params: Any) -> Any:
        """The biggest rating movers.

        Query parameters: limit

        ``GET /ratings/movers``
        """
        return self.get("/ratings/movers", **params)

    def find_similar_apis(self, aid: str, **params: Any) -> Any:
        """APIs similar to a given one.

        Query parameters: limit

        ``GET /apis/{aid}/similar``
        """
        return self.page(f"/apis/{aid}/similar", **params)

    def find_similar_providers(self, slug: str, **params: Any) -> Any:
        """Providers similar to a given one.

        Query parameters: limit

        ``GET /providers/{slug}/similar``
        """
        return self.page(f"/providers/{slug}/similar", **params)

    def gap_analysis(self, **params: Any) -> Any:
        """Artifact + score gap analysis for a provider or stack (Pro).

        Query parameters: min_share, providers

        ``GET /gaps``
        """
        return self.get("/gaps", **params)

    def generate_artifacts(self, slug: str, **params: Any) -> Any:
        """What APIs.io can generate on this provider's behalf

        ``POST /providers/{slug}/generate``
        """
        return self.request("POST", f"/providers/{slug}/generate", params=params)

    def get_api(self, aid: str, **params: Any) -> Any:
        """Get one API by aid.

        Query parameters: artifact_types, fields, include

        ``GET /apis/{aid}``
        """
        return self.get(f"/apis/{aid}", **params)

    def get_api_artifacts(self, aid: str, **params: Any) -> Any:
        """One API's artifacts, grouped by type.

        Query parameters: include

        ``GET /apis/{aid}/artifacts``
        """
        return self.get(f"/apis/{aid}/artifacts", **params)

    def get_area(self, slug: str, **params: Any) -> Any:
        """Get one area, with its ranked providers (Pro).

        Query parameters: fields

        ``GET /areas/{slug}``
        """
        return self.get(f"/areas/{slug}", **params)

    def get_area_leaders(self, slug: str, **params: Any) -> Any:
        """Top-rated providers in a curated area.

        Query parameters: limit

        ``GET /areas/{slug}/leaders``
        """
        return self.get(f"/areas/{slug}/leaders", **params)

    def get_cohort(self, kind: str, slug: str, **params: Any) -> Any:
        """One cohort and its member roster.

        ``GET /cohorts/{kind}/{slug}``
        """
        return self.get(f"/cohorts/{kind}/{slug}", **params)

    def get_cohort_capabilities(self, kind: str, slug: str, **params: Any) -> Any:
        """What every member publishes (Pro).

        ``GET /cohorts/{kind}/{slug}/capabilities``
        """
        return self.get(f"/cohorts/{kind}/{slug}/capabilities", **params)

    def get_cohort_rankings(self, kind: str, slug: str, **params: Any) -> Any:
        """The leaderboard, on two axes (Pro).

        Query parameters: format, limit, page

        ``GET /cohorts/{kind}/{slug}/rankings``
        """
        return self.get(f"/cohorts/{kind}/{slug}/rankings", **params)

    def get_cohort_scores(self, kind: str, slug: str, **params: Any) -> Any:
        """Facet-level scores, cohort-relative (Pro).

        Query parameters: format, limit, page

        ``GET /cohorts/{kind}/{slug}/scores``
        """
        return self.get(f"/cohorts/{kind}/{slug}/scores", **params)

    def get_cohort_stats(self, kind: str, slug: str, **params: Any) -> Any:
        """The distribution for a whole market (Pro).

        ``GET /cohorts/{kind}/{slug}/stats``
        """
        return self.get(f"/cohorts/{kind}/{slug}/stats", **params)

    def get_company_gaps(self, slug: str, **params: Any) -> Any:
        """A company's weakest dimensions.

        ``GET /insights/company/{slug}/gaps``
        """
        return self.get(f"/insights/company/{slug}/gaps", **params)

    def get_company_insight(self, slug: str, **params: Any) -> Any:
        """One company's demand-side profile.

        ``GET /insights/company/{slug}``
        """
        return self.get(f"/insights/company/{slug}", **params)

    def get_industry(self, slug: str, **params: Any) -> Any:
        """Get one industry, with its ranked providers.

        Query parameters: fields

        ``GET /industries/{slug}``
        """
        return self.get(f"/industries/{slug}", **params)

    def get_industry_leaders(self, slug: str, **params: Any) -> Any:
        """Top-rated providers in an industry.

        Query parameters: limit

        ``GET /industries/{slug}/leaders``
        """
        return self.get(f"/industries/{slug}/leaders", **params)

    def get_insights_summary(self, **params: Any) -> Any:
        """Insights overview.

        ``GET /insights``
        """
        return self.get("/insights", **params)

    def get_list(self, id: str, **params: Any) -> Any:
        """Get a list, members resolved to current name/band/score.

        ``GET /me/lists/{id}``
        """
        return self.get(f"/me/lists/{id}", **params)

    def get_openapi(self, aid: str, **params: Any) -> Any:
        """An API's primary OpenAPI.

        Query parameters: include

        ``GET /openapis/{aid}``
        """
        return self.get(f"/openapis/{aid}", **params)

    def get_provider(self, slug: str, **params: Any) -> Any:
        """Get one provider.

        Query parameters: fields

        ``GET /providers/{slug}``
        """
        return self.get(f"/providers/{slug}", **params)

    def get_provider_agent_readiness(self, slug: str, **params: Any) -> Any:
        """Agent-readiness dimensions (Pro).

        ``GET /providers/{slug}/agent-readiness``
        """
        return self.get(f"/providers/{slug}/agent-readiness", **params)

    def get_provider_artifacts(self, slug: str, **params: Any) -> Any:
        """Every artifact a provider publishes.

        ``GET /providers/{slug}/artifacts``
        """
        return self.get(f"/providers/{slug}/artifacts", **params)

    def get_provider_capabilities(self, slug: str, **params: Any) -> Any:
        """What one provider publishes, counted.

        ``GET /providers/{slug}/capabilities``
        """
        return self.get(f"/providers/{slug}/capabilities", **params)

    def get_provider_evidence(self, slug: str, **params: Any) -> Any:
        """How the score was established.

        ``GET /providers/{slug}/evidence``
        """
        return self.get(f"/providers/{slug}/evidence", **params)

    def get_provider_facets(self, slug: str, **params: Any) -> Any:
        """One provider's score at facet depth (Pro).

        ``GET /providers/{slug}/rating/facets``
        """
        return self.get(f"/providers/{slug}/rating/facets", **params)

    def get_provider_investors(self, slug: str, **params: Any) -> Any:
        """Which VC firms back this provider (reverse portfolio edge).

        ``GET /providers/{slug}/investors``
        """
        return self.get(f"/providers/{slug}/investors", **params)

    def get_provider_onboarding(self, slug: str, **params: Any) -> Any:
        """A provider's getting-started view.

        ``GET /providers/{slug}/onboarding``
        """
        return self.get(f"/providers/{slug}/onboarding", **params)

    def get_provider_operations(self, slug: str, **params: Any) -> Any:
        """Every operation a provider exposes.

        Query parameters: action_class, api, consequence, deprecated, format, limit, method, page, path, q

        ``GET /providers/{slug}/operations``
        """
        return self.get(f"/providers/{slug}/operations", **params)

    def get_provider_rating(self, slug: str, **params: Any) -> Any:
        """One provider's rating.

        ``GET /providers/{slug}/rating``
        """
        return self.get(f"/providers/{slug}/rating", **params)

    def get_provider_schema(self, slug: str, **params: Any) -> Any:
        """Every JSON Schema a provider publishes.

        Query parameters: format, limit, page, q

        ``GET /providers/{slug}/schema``
        """
        return self.get(f"/providers/{slug}/schema", **params)

    def get_provider_tools(self, slug: str, **params: Any) -> Any:
        """Every MCP tool a provider ships.

        Query parameters: format, limit, page, provenance

        ``GET /providers/{slug}/tools``
        """
        return self.get(f"/providers/{slug}/tools", **params)

    def get_rating_history(self, slug: str, **params: Any) -> Any:
        """A provider's rating movement.

        ``GET /providers/{slug}/rating/history``
        """
        return self.get(f"/providers/{slug}/rating/history", **params)

    def get_rating_rubric(self, **params: Any) -> Any:
        """The rating rubric.

        ``GET /ratings/rubric``
        """
        return self.get("/ratings/rubric", **params)

    def get_region(self, slug: str, **params: Any) -> Any:
        """Get one region, with its ranked providers.

        Query parameters: fields

        ``GET /regions/{slug}``
        """
        return self.get(f"/regions/{slug}", **params)

    def get_region_leaders(self, slug: str, **params: Any) -> Any:
        """Top-rated providers in a region.

        Query parameters: limit

        ``GET /regions/{slug}/leaders``
        """
        return self.get(f"/regions/{slug}/leaders", **params)

    def get_tag(self, slug: str, **params: Any) -> Any:
        """Get one tag, with its linked providers, APIs, and neighbors.

        Query parameters: fields

        ``GET /tags/{slug}``
        """
        return self.get(f"/tags/{slug}", **params)

    def get_vc(self, slug: str, **params: Any) -> Any:
        """One VC firm — identity, fund facts, portfolio summary.

        Query parameters: view

        ``GET /vcs/{slug}``
        """
        return self.get(f"/vcs/{slug}", **params)

    def get_vc_portfolio(self, slug: str, **params: Any) -> Any:
        """A VC firm's portfolio graph.

        Query parameters: band, in_network, is_provider, limit, min_score, page, sort

        ``GET /vcs/{slug}/portfolio``
        """
        return self.get(f"/vcs/{slug}/portfolio", **params)

    def industry_gap_analysis(self, slug: str, **params: Any) -> Any:
        """Artifact gaps across a whole industry.

        Query parameters: min_share

        ``GET /gaps/industry/{slug}``
        """
        return self.get(f"/gaps/industry/{slug}", **params)

    def list_apis(self, **params: Any) -> Any:
        """List and filter APIs across the network.

        Query parameters: artifact_types, band, fields, format, include, industry, limit, match, min_score, page, providers, q, region, sort

        ``GET /apis``
        """
        return self.page("/apis", **params)

    def list_apis_json(self, **params: Any) -> Any:
        """APIs.json indexes across the catalog.

        Query parameters: include, limit, page, providers, q, tags

        ``GET /apis-json``
        """
        return self.get("/apis-json", **params)

    def list_arazzo(self, **params: Any) -> Any:
        """List arazzo workflows across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /arazzo``
        """
        return self.page("/arazzo", **params)

    def list_areas(self, **params: Any) -> Any:
        """List and filter areas (Pro).

        Query parameters: fields, limit, page, q, sort

        ``GET /areas``
        """
        return self.page("/areas", **params)

    def list_asyncapis(self, **params: Any) -> Any:
        """List asyncapi specifications across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /asyncapis``
        """
        return self.page("/asyncapis", **params)

    def list_channels(self, **params: Any) -> Any:
        """List AsyncAPI event channels across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /channels``
        """
        return self.page("/channels", **params)

    def list_cohorts(self, **params: Any) -> Any:
        """Every scored cohort in the catalog.

        Query parameters: format, kind, limit, min_providers, page, q, tier

        ``GET /cohorts``
        """
        return self.get("/cohorts", **params)

    def list_collections(self, **params: Any) -> Any:
        """List api collections across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /collections``
        """
        return self.page("/collections", **params)

    def list_examples(self, **params: Any) -> Any:
        """List examples across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /examples``
        """
        return self.page("/examples", **params)

    def list_finops(self, **params: Any) -> Any:
        """List finops artifacts across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /finops``
        """
        return self.page("/finops", **params)

    def list_graphql(self, **params: Any) -> Any:
        """List graphql schemas across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /graphql``
        """
        return self.page("/graphql", **params)

    def list_industries(self, **params: Any) -> Any:
        """List and filter industries.

        Query parameters: fields, limit, page, q, sort

        ``GET /industries``
        """
        return self.page("/industries", **params)

    def list_insight_adoption(self, **params: Any) -> Any:
        """Services / tools / standards by adoption.

        Query parameters: limit, page, type

        ``GET /insights/adoption``
        """
        return self.get("/insights/adoption", **params)

    def list_insight_companies(self, **params: Any) -> Any:
        """Browse profiled companies.

        Query parameters: limit, page, q

        ``GET /insights/companies``
        """
        return self.get("/insights/companies", **params)

    def list_insight_dimensions(self, **params: Any) -> Any:
        """Rank the investment dimensions.

        Query parameters: limit, page

        ``GET /insights/dimensions``
        """
        return self.get("/insights/dimensions", **params)

    def list_insight_industries(self, **params: Any) -> Any:
        """Industry rollup.

        ``GET /insights/industries``
        """
        return self.get("/insights/industries", **params)

    def list_json_ld(self, **params: Any) -> Any:
        """List json-ld contexts across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /json-ld``
        """
        return self.page("/json-ld", **params)

    def list_json_schemas(self, **params: Any) -> Any:
        """List json schema definitions across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /json-schemas``
        """
        return self.page("/json-schemas", **params)

    def list_json_structures(self, **params: Any) -> Any:
        """List json structure definitions across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /json-structures``
        """
        return self.page("/json-structures", **params)

    def list_lists(self, **params: Any) -> Any:
        """List the lists/shortlists you own.

        ``GET /me/lists``
        """
        return self.get("/me/lists", **params)

    def list_mcp_servers(self, **params: Any) -> Any:
        """List published MCP servers across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /mcp``
        """
        return self.page("/mcp", **params)

    def list_openapis(self, **params: Any) -> Any:
        """List openapi specifications across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /openapis``
        """
        return self.page("/openapis", **params)

    def list_plans(self, **params: Any) -> Any:
        """List plans across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /plans``
        """
        return self.page("/plans", **params)

    def list_postman(self, **params: Any) -> Any:
        """List postman collections across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /postman``
        """
        return self.page("/postman", **params)

    def list_provider_apis(self, slug: str, **params: Any) -> Any:
        """List the APIs published by a provider.

        Query parameters: artifact_types, fields, include, limit, match, page, tags

        ``GET /providers/{slug}/apis``
        """
        return self.page(f"/providers/{slug}/apis", **params)

    def list_providers(self, **params: Any) -> Any:
        """List and filter providers.

        Query parameters: artifact_types, band, facet, fields, format, industry, limit, match, max_score, min_facet, min_score, page, q, region

        ``GET /providers``
        """
        return self.page("/providers", **params)

    def list_rate_limits(self, **params: Any) -> Any:
        """List rate limits across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /rate-limits``
        """
        return self.page("/rate-limits", **params)

    def list_ratings(self, **params: Any) -> Any:
        """Ranked ratings leaderboard.

        Query parameters: band, facet, format, limit, max_score, min_facet, min_score, page, providers, sort, tags, trend

        ``GET /ratings``
        """
        return self.page("/ratings", **params)

    def list_regions(self, **params: Any) -> Any:
        """List and filter regions.

        Query parameters: fields, limit, page, q, sort

        ``GET /regions``
        """
        return self.page("/regions", **params)

    def list_rules(self, **params: Any) -> Any:
        """List governance rulesets across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /rules``
        """
        return self.page("/rules", **params)

    def list_saved_searches(self, **params: Any) -> Any:
        """List your saved searches.

        ``GET /me/searches``
        """
        return self.get("/me/searches", **params)

    def list_scopes(self, **params: Any) -> Any:
        """List OAuth scope sets across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /scopes``
        """
        return self.page("/scopes", **params)

    def list_security(self, **params: Any) -> Any:
        """List security scheme definitions across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /security``
        """
        return self.page("/security", **params)

    def list_skills(self, **params: Any) -> Any:
        """List published Agent Skills across the catalog.

        Query parameters: include, limit, match, page, providers, q, sort, tags

        ``GET /skills``
        """
        return self.page("/skills", **params)

    def list_tags(self, **params: Any) -> Any:
        """List and rank tags.

        Query parameters: band, fields, format, limit, min_api_count, page, q, sort

        ``GET /tags``
        """
        return self.page("/tags", **params)

    def list_vcs(self, **params: Any) -> Any:
        """List / search venture-capital firms.

        Query parameters: category, limit, page, q, sort, tags

        ``GET /vcs``
        """
        return self.get("/vcs", **params)

    def match_company_providers(self, slug: str, **params: Any) -> Any:
        """Match providers to a company's stack (the supply↔demand join).

        ``GET /insights/company/{slug}/match``
        """
        return self.get(f"/insights/company/{slug}/match", **params)

    def provider_rating_checks(self, slug: str, **params: Any) -> Any:
        """Per-check Kin Score results for this provider

        ``GET /providers/{slug}/rating/checks``
        """
        return self.get(f"/providers/{slug}/rating/checks", **params)

    def readiness_gates(self, slug: str, **params: Any) -> Any:
        """Band gates for this provider, and what is unmet

        ``GET /providers/{slug}/gates``
        """
        return self.get(f"/providers/{slug}/gates", **params)

    def recommend_stack(self, **params: Any) -> Any:
        """Design a recommended API stack per capability.

        Query parameters: capabilities, region

        ``GET /stack``
        """
        return self.get("/stack", **params)

    def report_correction(self, slug: str, body: Any = None, **params: Any) -> Any:
        """Report that the catalog has this provider wrong

        ``POST /providers/{slug}/correction``
        """
        return self.request("POST", f"/providers/{slug}/correction", params=params, json=body)

    def report_gap(self, body: Any = None, **params: Any) -> Any:
        """Tell us what you looked for and did not find

        ``POST /gaps/report``
        """
        return self.request("POST", "/gaps/report", params=params, json=body)

    def request_check(self, body: Any = None, **params: Any) -> Any:
        """Ask for a provider, industry, tag or area to be re-profiled

        ``POST /checks``
        """
        return self.request("POST", "/checks", params=params, json=body)

    def resolve_identifier(self, **params: Any) -> Any:
        """Resolve any identifier (domain / URL / GitHub org) to a provider.

        Query parameters: identifier

        ``GET /resolve``
        """
        return self.get("/resolve", **params)

    def run_saved_search(self, id: str, **params: Any) -> Any:
        """Re-run a saved search against the live catalog.

        Query parameters: limit

        ``GET /me/searches/{id}/results``
        """
        return self.get(f"/me/searches/{id}/results", **params)

    def saved_search_net_new(self, id: str, **params: Any) -> Any:
        """What's NEW for a saved search since you last checked.

        ``GET /me/searches/{id}/net_new``
        """
        return self.get(f"/me/searches/{id}/net_new", **params)

    def search(self, **params: Any) -> Any:
        """Unified search across apis, providers, tags, and artifacts.

        Query parameters: artifact_types, band, fields, include, industry, limit, match, min_score, page, providers, q, region, return, sort

        ``GET /search``
        """
        return self.get("/search", **params)

    def set_visibility(self, slug: str, body: Any = None, **params: Any) -> Any:
        """Request restricted listing or removal

        ``POST /providers/{slug}/visibility``
        """
        return self.request("POST", f"/providers/{slug}/visibility", params=params, json=body)

    def simulate_fixes(self, slug: str, body: Any = None, **params: Any) -> Any:
        """What a set of fixes would move the score to

        ``POST /providers/{slug}/projection``
        """
        return self.request("POST", f"/providers/{slug}/projection", params=params, json=body)

    def story_leads(self, **params: Any) -> Any:
        """Story leads from catalog movement (owner).

        Query parameters: limit

        ``GET /story-leads``
        """
        return self.get("/story-leads", **params)

    def submit_artifact(self, slug: str, body: Any = None, **params: Any) -> Any:
        """Create or update an artifact pointer for this listing

        ``POST /providers/{slug}/submit``
        """
        return self.request("POST", f"/providers/{slug}/submit", params=params, json=body)

    def what_can_i_fix(self, slug: str, **params: Any) -> Any:
        """The ranked, costed punch list for this provider

        ``GET /providers/{slug}/remediation``
        """
        return self.get(f"/providers/{slug}/remediation", **params)

    def whats_changed(self, **params: Any) -> Any:
        """What changed in the catalog since a date (Pro).

        Query parameters: limit, since

        ``GET /changes``
        """
        return self.get("/changes", **params)
