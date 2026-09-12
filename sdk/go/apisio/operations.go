// apis.io operation bindings — GENERATED, DO NOT EDIT.
//
// Regenerate with `python3 ../../python/generate.py` from the OpenAPI documents in
// all/apis-io/openapi/_original/ — the documents apis.io publishes, not the refined mirror.
//
// 108 operations across 18 documents, generated 2026-09-12.

package apisio

import (
	"context"
	"fmt"
)

// AddToList — Add providers/APIs to a list.
//
// POST /me/lists/{id}/entries
func (c *Client) AddToList(ctx context.Context, id string, body any, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", fmt.Sprintf("/me/lists/%s/entries", id), params, body)
}

// ClaimListing — Create or return your claim on this listing
//
// POST /providers/{slug}/claim
func (c *Client) ClaimListing(ctx context.Context, slug string, body any, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", fmt.Sprintf("/providers/%s/claim", slug), params, body)
}

// CompareCohorts — Two cohorts side by side (Pro).
//
// GET /cohorts/compare
func (c *Client) CompareCohorts(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/cohorts/compare", params)
}

// CompareProviders — Compare providers side by side (Pro).
//
// GET /compare
func (c *Client) CompareProviders(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/compare", params)
}

// CorrectFacts — Create or update your pending fact correction for this listing
//
// POST /providers/{slug}/facts
func (c *Client) CorrectFacts(ctx context.Context, slug string, body any, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", fmt.Sprintf("/providers/%s/facts", slug), params, body)
}

// CreateList — Create a named, persistent list.
//
// POST /me/lists
func (c *Client) CreateList(ctx context.Context, body any, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", "/me/lists", params, body)
}

// CreateSavedSearch — Create a saved search.
//
// POST /me/searches
func (c *Client) CreateSavedSearch(ctx context.Context, body any, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", "/me/searches", params, body)
}

// DeleteList — Delete a list you own.
//
// DELETE /me/lists/{id}
func (c *Client) DeleteList(ctx context.Context, id string, params map[string]any) (any, error) {
	return c.Request(ctx, "DELETE", fmt.Sprintf("/me/lists/%s", id), params, nil)
}

// DeleteSavedSearch — Delete a saved search you own.
//
// DELETE /me/searches/{id}
func (c *Client) DeleteSavedSearch(ctx context.Context, id string, params map[string]any) (any, error) {
	return c.Request(ctx, "DELETE", fmt.Sprintf("/me/searches/%s", id), params, nil)
}

// DisputeFinding — Dispute something the rating says about this provider
//
// POST /providers/{slug}/dispute
func (c *Client) DisputeFinding(ctx context.Context, slug string, body any, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", fmt.Sprintf("/providers/%s/dispute", slug), params, body)
}

// EnrichProvider — Enrich a provider in one call, choosing field groups.
//
// GET /enrich
func (c *Client) EnrichProvider(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/enrich", params)
}

// ExportDataset — Export a whole dataset in one pull.
//
// GET /export
func (c *Client) ExportDataset(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/export", params)
}

// ExportNamedDataset — Export one named dataset.
//
// GET /export/{dataset}
func (c *Client) ExportNamedDataset(ctx context.Context, dataset string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/export/%s", dataset), params)
}

// ExportStack — Export a designed stack as APIs.json.
//
// GET /stack/export
func (c *Client) ExportStack(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/stack/export", params)
}

// FindRatingMovers — The biggest rating movers.
//
// GET /ratings/movers
func (c *Client) FindRatingMovers(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/ratings/movers", params)
}

// FindSimilarApis — APIs similar to a given one.
//
// GET /apis/{aid}/similar
func (c *Client) FindSimilarApis(ctx context.Context, aid string, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, fmt.Sprintf("/apis/%s/similar", aid), params)
}

// FindSimilarProviders — Providers similar to a given one.
//
// GET /providers/{slug}/similar
func (c *Client) FindSimilarProviders(ctx context.Context, slug string, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, fmt.Sprintf("/providers/%s/similar", slug), params)
}

// GapAnalysis — Artifact + score gap analysis for a provider or stack (Pro).
//
// GET /gaps
func (c *Client) GapAnalysis(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/gaps", params)
}

// GenerateArtifacts — What APIs.io can generate on this provider's behalf
//
// POST /providers/{slug}/generate
func (c *Client) GenerateArtifacts(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", fmt.Sprintf("/providers/%s/generate", slug), params, nil)
}

// GetApi — Get one API by aid.
//
// GET /apis/{aid}
func (c *Client) GetApi(ctx context.Context, aid string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/apis/%s", aid), params)
}

// GetApiArtifacts — One API's artifacts, grouped by type.
//
// GET /apis/{aid}/artifacts
func (c *Client) GetApiArtifacts(ctx context.Context, aid string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/apis/%s/artifacts", aid), params)
}

// GetArea — Get one area, with its ranked providers (Pro).
//
// GET /areas/{slug}
func (c *Client) GetArea(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/areas/%s", slug), params)
}

// GetAreaLeaders — Top-rated providers in a curated area.
//
// GET /areas/{slug}/leaders
func (c *Client) GetAreaLeaders(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/areas/%s/leaders", slug), params)
}

// GetCohort — One cohort and its member roster.
//
// GET /cohorts/{kind}/{slug}
func (c *Client) GetCohort(ctx context.Context, kind string, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/cohorts/%s/%s", kind, slug), params)
}

// GetCohortCapabilities — What every member publishes (Pro).
//
// GET /cohorts/{kind}/{slug}/capabilities
func (c *Client) GetCohortCapabilities(ctx context.Context, kind string, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/cohorts/%s/%s/capabilities", kind, slug), params)
}

// GetCohortRankings — The leaderboard, on two axes (Pro).
//
// GET /cohorts/{kind}/{slug}/rankings
func (c *Client) GetCohortRankings(ctx context.Context, kind string, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/cohorts/%s/%s/rankings", kind, slug), params)
}

// GetCohortScores — Facet-level scores, cohort-relative (Pro).
//
// GET /cohorts/{kind}/{slug}/scores
func (c *Client) GetCohortScores(ctx context.Context, kind string, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/cohorts/%s/%s/scores", kind, slug), params)
}

// GetCohortStats — The distribution for a whole market (Pro).
//
// GET /cohorts/{kind}/{slug}/stats
func (c *Client) GetCohortStats(ctx context.Context, kind string, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/cohorts/%s/%s/stats", kind, slug), params)
}

// GetCompanyGaps — A company's weakest dimensions.
//
// GET /insights/company/{slug}/gaps
func (c *Client) GetCompanyGaps(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/insights/company/%s/gaps", slug), params)
}

// GetCompanyInsight — One company's demand-side profile.
//
// GET /insights/company/{slug}
func (c *Client) GetCompanyInsight(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/insights/company/%s", slug), params)
}

// GetIndustry — Get one industry, with its ranked providers.
//
// GET /industries/{slug}
func (c *Client) GetIndustry(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/industries/%s", slug), params)
}

// GetIndustryLeaders — Top-rated providers in an industry.
//
// GET /industries/{slug}/leaders
func (c *Client) GetIndustryLeaders(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/industries/%s/leaders", slug), params)
}

// GetInsightsSummary — Insights overview.
//
// GET /insights
func (c *Client) GetInsightsSummary(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/insights", params)
}

// GetList — Get a list, members resolved to current name/band/score.
//
// GET /me/lists/{id}
func (c *Client) GetList(ctx context.Context, id string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/me/lists/%s", id), params)
}

// GetOpenapi — An API's primary OpenAPI.
//
// GET /openapis/{aid}
func (c *Client) GetOpenapi(ctx context.Context, aid string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/openapis/%s", aid), params)
}

// GetProvider — Get one provider.
//
// GET /providers/{slug}
func (c *Client) GetProvider(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s", slug), params)
}

// GetProviderAgentReadiness — Agent-readiness dimensions (Pro).
//
// GET /providers/{slug}/agent-readiness
func (c *Client) GetProviderAgentReadiness(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s/agent-readiness", slug), params)
}

// GetProviderArtifacts — Every artifact a provider publishes.
//
// GET /providers/{slug}/artifacts
func (c *Client) GetProviderArtifacts(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s/artifacts", slug), params)
}

// GetProviderCapabilities — What one provider publishes, counted.
//
// GET /providers/{slug}/capabilities
func (c *Client) GetProviderCapabilities(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s/capabilities", slug), params)
}

// GetProviderEvidence — How the score was established.
//
// GET /providers/{slug}/evidence
func (c *Client) GetProviderEvidence(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s/evidence", slug), params)
}

// GetProviderFacets — One provider's score at facet depth (Pro).
//
// GET /providers/{slug}/rating/facets
func (c *Client) GetProviderFacets(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s/rating/facets", slug), params)
}

// GetProviderInvestors — Which VC firms back this provider (reverse portfolio edge).
//
// GET /providers/{slug}/investors
func (c *Client) GetProviderInvestors(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s/investors", slug), params)
}

// GetProviderOnboarding — A provider's getting-started view.
//
// GET /providers/{slug}/onboarding
func (c *Client) GetProviderOnboarding(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s/onboarding", slug), params)
}

// GetProviderOperations — Every operation a provider exposes.
//
// GET /providers/{slug}/operations
func (c *Client) GetProviderOperations(ctx context.Context, slug string, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, fmt.Sprintf("/providers/%s/operations", slug), params)
}

// GetProviderRating — One provider's rating.
//
// GET /providers/{slug}/rating
func (c *Client) GetProviderRating(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s/rating", slug), params)
}

// GetProviderSchema — Every JSON Schema a provider publishes.
//
// GET /providers/{slug}/schema
func (c *Client) GetProviderSchema(ctx context.Context, slug string, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, fmt.Sprintf("/providers/%s/schema", slug), params)
}

// GetProviderTools — Every MCP tool a provider ships.
//
// GET /providers/{slug}/tools
func (c *Client) GetProviderTools(ctx context.Context, slug string, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, fmt.Sprintf("/providers/%s/tools", slug), params)
}

// GetRatingHistory — A provider's rating movement.
//
// GET /providers/{slug}/rating/history
func (c *Client) GetRatingHistory(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s/rating/history", slug), params)
}

// GetRatingRubric — The rating rubric.
//
// GET /ratings/rubric
func (c *Client) GetRatingRubric(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/ratings/rubric", params)
}

// GetRegion — Get one region, with its ranked providers.
//
// GET /regions/{slug}
func (c *Client) GetRegion(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/regions/%s", slug), params)
}

// GetRegionLeaders — Top-rated providers in a region.
//
// GET /regions/{slug}/leaders
func (c *Client) GetRegionLeaders(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/regions/%s/leaders", slug), params)
}

// GetTag — Get one tag, with its linked providers, APIs, and neighbors.
//
// GET /tags/{slug}
func (c *Client) GetTag(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/tags/%s", slug), params)
}

// GetVc — One VC firm — identity, fund facts, portfolio summary.
//
// GET /vcs/{slug}
func (c *Client) GetVc(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/vcs/%s", slug), params)
}

// GetVcPortfolio — A VC firm's portfolio graph.
//
// GET /vcs/{slug}/portfolio
func (c *Client) GetVcPortfolio(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/vcs/%s/portfolio", slug), params)
}

// IndustryGapAnalysis — Artifact gaps across a whole industry.
//
// GET /gaps/industry/{slug}
func (c *Client) IndustryGapAnalysis(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/gaps/industry/%s", slug), params)
}

// ListApis — List and filter APIs across the network.
//
// GET /apis
func (c *Client) ListApis(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/apis", params)
}

// ListApisJson — APIs.json indexes across the catalog.
//
// GET /apis-json
func (c *Client) ListApisJson(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/apis-json", params)
}

// ListArazzo — List arazzo workflows across the catalog.
//
// GET /arazzo
func (c *Client) ListArazzo(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/arazzo", params)
}

// ListAreas — List and filter areas (Pro).
//
// GET /areas
func (c *Client) ListAreas(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/areas", params)
}

// ListAsyncapis — List asyncapi specifications across the catalog.
//
// GET /asyncapis
func (c *Client) ListAsyncapis(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/asyncapis", params)
}

// ListChannels — List AsyncAPI event channels across the catalog.
//
// GET /channels
func (c *Client) ListChannels(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/channels", params)
}

// ListCohorts — Every scored cohort in the catalog.
//
// GET /cohorts
func (c *Client) ListCohorts(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/cohorts", params)
}

// ListCollections — List api collections across the catalog.
//
// GET /collections
func (c *Client) ListCollections(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/collections", params)
}

// ListExamples — List examples across the catalog.
//
// GET /examples
func (c *Client) ListExamples(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/examples", params)
}

// ListFinops — List finops artifacts across the catalog.
//
// GET /finops
func (c *Client) ListFinops(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/finops", params)
}

// ListGraphql — List graphql schemas across the catalog.
//
// GET /graphql
func (c *Client) ListGraphql(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/graphql", params)
}

// ListIndustries — List and filter industries.
//
// GET /industries
func (c *Client) ListIndustries(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/industries", params)
}

// ListInsightAdoption — Services / tools / standards by adoption.
//
// GET /insights/adoption
func (c *Client) ListInsightAdoption(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/insights/adoption", params)
}

// ListInsightCompanies — Browse profiled companies.
//
// GET /insights/companies
func (c *Client) ListInsightCompanies(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/insights/companies", params)
}

// ListInsightDimensions — Rank the investment dimensions.
//
// GET /insights/dimensions
func (c *Client) ListInsightDimensions(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/insights/dimensions", params)
}

// ListInsightIndustries — Industry rollup.
//
// GET /insights/industries
func (c *Client) ListInsightIndustries(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/insights/industries", params)
}

// ListJsonLd — List json-ld contexts across the catalog.
//
// GET /json-ld
func (c *Client) ListJsonLd(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/json-ld", params)
}

// ListJsonSchemas — List json schema definitions across the catalog.
//
// GET /json-schemas
func (c *Client) ListJsonSchemas(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/json-schemas", params)
}

// ListJsonStructures — List json structure definitions across the catalog.
//
// GET /json-structures
func (c *Client) ListJsonStructures(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/json-structures", params)
}

// ListLists — List the lists/shortlists you own.
//
// GET /me/lists
func (c *Client) ListLists(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/me/lists", params)
}

// ListMcpServers — List published MCP servers across the catalog.
//
// GET /mcp
func (c *Client) ListMcpServers(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/mcp", params)
}

// ListOpenapis — List openapi specifications across the catalog.
//
// GET /openapis
func (c *Client) ListOpenapis(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/openapis", params)
}

// ListPlans — List plans across the catalog.
//
// GET /plans
func (c *Client) ListPlans(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/plans", params)
}

// ListPostman — List postman collections across the catalog.
//
// GET /postman
func (c *Client) ListPostman(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/postman", params)
}

// ListProviderApis — List the APIs published by a provider.
//
// GET /providers/{slug}/apis
func (c *Client) ListProviderApis(ctx context.Context, slug string, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, fmt.Sprintf("/providers/%s/apis", slug), params)
}

// ListProviders — List and filter providers.
//
// GET /providers
func (c *Client) ListProviders(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/providers", params)
}

// ListRateLimits — List rate limits across the catalog.
//
// GET /rate-limits
func (c *Client) ListRateLimits(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/rate-limits", params)
}

// ListRatings — Ranked ratings leaderboard.
//
// GET /ratings
func (c *Client) ListRatings(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/ratings", params)
}

// ListRegions — List and filter regions.
//
// GET /regions
func (c *Client) ListRegions(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/regions", params)
}

// ListRules — List governance rulesets across the catalog.
//
// GET /rules
func (c *Client) ListRules(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/rules", params)
}

// ListSavedSearches — List your saved searches.
//
// GET /me/searches
func (c *Client) ListSavedSearches(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/me/searches", params)
}

// ListScopes — List OAuth scope sets across the catalog.
//
// GET /scopes
func (c *Client) ListScopes(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/scopes", params)
}

// ListSecurity — List security scheme definitions across the catalog.
//
// GET /security
func (c *Client) ListSecurity(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/security", params)
}

// ListSkills — List published Agent Skills across the catalog.
//
// GET /skills
func (c *Client) ListSkills(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/skills", params)
}

// ListTags — List and rank tags.
//
// GET /tags
func (c *Client) ListTags(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/tags", params)
}

// ListVcs — List / search venture-capital firms.
//
// GET /vcs
func (c *Client) ListVcs(ctx context.Context, params map[string]any) (*Page, error) {
	return c.GetPage(ctx, "/vcs", params)
}

// MatchCompanyProviders — Match providers to a company's stack (the supply↔demand join).
//
// GET /insights/company/{slug}/match
func (c *Client) MatchCompanyProviders(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/insights/company/%s/match", slug), params)
}

// ProviderRatingChecks — Per-check Kin Score results for this provider
//
// GET /providers/{slug}/rating/checks
func (c *Client) ProviderRatingChecks(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s/rating/checks", slug), params)
}

// ReadinessGates — Band gates for this provider, and what is unmet
//
// GET /providers/{slug}/gates
func (c *Client) ReadinessGates(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s/gates", slug), params)
}

// RecommendStack — Design a recommended API stack per capability.
//
// GET /stack
func (c *Client) RecommendStack(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/stack", params)
}

// ReportCorrection — Report that the catalog has this provider wrong
//
// POST /providers/{slug}/correction
func (c *Client) ReportCorrection(ctx context.Context, slug string, body any, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", fmt.Sprintf("/providers/%s/correction", slug), params, body)
}

// ReportGap — Tell us what you looked for and did not find
//
// POST /gaps/report
func (c *Client) ReportGap(ctx context.Context, body any, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", "/gaps/report", params, body)
}

// RequestCheck — Ask for a provider, industry, tag or area to be re-profiled
//
// POST /checks
func (c *Client) RequestCheck(ctx context.Context, body any, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", "/checks", params, body)
}

// ResolveIdentifier — Resolve any identifier (domain / URL / GitHub org) to a provider.
//
// GET /resolve
func (c *Client) ResolveIdentifier(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/resolve", params)
}

// RunSavedSearch — Re-run a saved search against the live catalog.
//
// GET /me/searches/{id}/results
func (c *Client) RunSavedSearch(ctx context.Context, id string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/me/searches/%s/results", id), params)
}

// SavedSearchNetNew — What's NEW for a saved search since you last checked.
//
// GET /me/searches/{id}/net_new
func (c *Client) SavedSearchNetNew(ctx context.Context, id string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/me/searches/%s/net_new", id), params)
}

// Search — Unified search across apis, providers, tags, and artifacts.
//
// GET /search
func (c *Client) Search(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/search", params)
}

// SetVisibility — Request restricted listing or removal
//
// POST /providers/{slug}/visibility
func (c *Client) SetVisibility(ctx context.Context, slug string, body any, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", fmt.Sprintf("/providers/%s/visibility", slug), params, body)
}

// SimulateFixes — What a set of fixes would move the score to
//
// POST /providers/{slug}/projection
func (c *Client) SimulateFixes(ctx context.Context, slug string, body any, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", fmt.Sprintf("/providers/%s/projection", slug), params, body)
}

// StoryLeads — Story leads from catalog movement (owner).
//
// GET /story-leads
func (c *Client) StoryLeads(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/story-leads", params)
}

// SubmitArtifact — Create or update an artifact pointer for this listing
//
// POST /providers/{slug}/submit
func (c *Client) SubmitArtifact(ctx context.Context, slug string, body any, params map[string]any) (any, error) {
	return c.Request(ctx, "POST", fmt.Sprintf("/providers/%s/submit", slug), params, body)
}

// WhatCanIFix — The ranked, costed punch list for this provider
//
// GET /providers/{slug}/remediation
func (c *Client) WhatCanIFix(ctx context.Context, slug string, params map[string]any) (any, error) {
	return c.Get(ctx, fmt.Sprintf("/providers/%s/remediation", slug), params)
}

// WhatsChanged — What changed in the catalog since a date (Pro).
//
// GET /changes
func (c *Client) WhatsChanged(ctx context.Context, params map[string]any) (any, error) {
	return c.Get(ctx, "/changes", params)
}
