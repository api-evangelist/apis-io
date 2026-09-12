/* apis.io operation bindings — GENERATED, DO NOT EDIT.
 *
 * Regenerate with `python3 ../python/generate.py` from the OpenAPI documents in
 * all/apis-io/openapi/_original/ — the documents apis.io publishes, not the refined mirror.
 *
 * 108 operations across 18 documents, generated 2026-09-12.
 */

import { Transport } from './client.js';

export class Client extends Transport {

  /** Add providers/APIs to a list.
   *  `POST /me/lists/{id}/entries` */
  addToList(id, body = null, params = {}) {
    return this.request('POST', `/me/lists/${id}/entries`, { params, json: body });
  }

  /** Create or return your claim on this listing
   *  `POST /providers/{slug}/claim` */
  claimListing(slug, body = null, params = {}) {
    return this.request('POST', `/providers/${slug}/claim`, { params, json: body });
  }

  /** Two cohorts side by side (Pro).
   *  `GET /cohorts/compare` */
  compareCohorts(params = {}) {
    return this.get(`/cohorts/compare`, params);
  }

  /** Compare providers side by side (Pro).
   *  `GET /compare` */
  compareProviders(params = {}) {
    return this.get(`/compare`, params);
  }

  /** Create or update your pending fact correction for this listing
   *  `POST /providers/{slug}/facts` */
  correctFacts(slug, body = null, params = {}) {
    return this.request('POST', `/providers/${slug}/facts`, { params, json: body });
  }

  /** Create a named, persistent list.
   *  `POST /me/lists` */
  createList(body = null, params = {}) {
    return this.request('POST', `/me/lists`, { params, json: body });
  }

  /** Create a saved search.
   *  `POST /me/searches` */
  createSavedSearch(body = null, params = {}) {
    return this.request('POST', `/me/searches`, { params, json: body });
  }

  /** Delete a list you own.
   *  `DELETE /me/lists/{id}` */
  deleteList(id, params = {}) {
    return this.delete(`/me/lists/${id}`, params);
  }

  /** Delete a saved search you own.
   *  `DELETE /me/searches/{id}` */
  deleteSavedSearch(id, params = {}) {
    return this.delete(`/me/searches/${id}`, params);
  }

  /** Dispute something the rating says about this provider
   *  `POST /providers/{slug}/dispute` */
  disputeFinding(slug, body = null, params = {}) {
    return this.request('POST', `/providers/${slug}/dispute`, { params, json: body });
  }

  /** Enrich a provider in one call, choosing field groups.
   *  `GET /enrich` */
  enrichProvider(params = {}) {
    return this.get(`/enrich`, params);
  }

  /** Export a whole dataset in one pull.
   *  `GET /export` */
  exportDataset(params = {}) {
    return this.get(`/export`, params);
  }

  /** Export one named dataset.
   *  `GET /export/{dataset}` */
  exportNamedDataset(dataset, params = {}) {
    return this.get(`/export/${dataset}`, params);
  }

  /** Export a designed stack as APIs.json.
   *  `GET /stack/export` */
  exportStack(params = {}) {
    return this.get(`/stack/export`, params);
  }

  /** The biggest rating movers.
   *  `GET /ratings/movers` */
  findRatingMovers(params = {}) {
    return this.get(`/ratings/movers`, params);
  }

  /** APIs similar to a given one.
   *  `GET /apis/{aid}/similar` */
  findSimilarApis(aid, params = {}) {
    return this.page(`/apis/${aid}/similar`, params);
  }

  /** Providers similar to a given one.
   *  `GET /providers/{slug}/similar` */
  findSimilarProviders(slug, params = {}) {
    return this.page(`/providers/${slug}/similar`, params);
  }

  /** Artifact + score gap analysis for a provider or stack (Pro).
   *  `GET /gaps` */
  gapAnalysis(params = {}) {
    return this.get(`/gaps`, params);
  }

  /** What APIs.io can generate on this provider's behalf
   *  `POST /providers/{slug}/generate` */
  generateArtifacts(slug, params = {}) {
    return this.request('POST', `/providers/${slug}/generate`, { params });
  }

  /** Get one API by aid.
   *  `GET /apis/{aid}` */
  getApi(aid, params = {}) {
    return this.get(`/apis/${aid}`, params);
  }

  /** One API's artifacts, grouped by type.
   *  `GET /apis/{aid}/artifacts` */
  getApiArtifacts(aid, params = {}) {
    return this.get(`/apis/${aid}/artifacts`, params);
  }

  /** Get one area, with its ranked providers (Pro).
   *  `GET /areas/{slug}` */
  getArea(slug, params = {}) {
    return this.get(`/areas/${slug}`, params);
  }

  /** Top-rated providers in a curated area.
   *  `GET /areas/{slug}/leaders` */
  getAreaLeaders(slug, params = {}) {
    return this.get(`/areas/${slug}/leaders`, params);
  }

  /** One cohort and its member roster.
   *  `GET /cohorts/{kind}/{slug}` */
  getCohort(kind, slug, params = {}) {
    return this.get(`/cohorts/${kind}/${slug}`, params);
  }

  /** What every member publishes (Pro).
   *  `GET /cohorts/{kind}/{slug}/capabilities` */
  getCohortCapabilities(kind, slug, params = {}) {
    return this.get(`/cohorts/${kind}/${slug}/capabilities`, params);
  }

  /** The leaderboard, on two axes (Pro).
   *  `GET /cohorts/{kind}/{slug}/rankings` */
  getCohortRankings(kind, slug, params = {}) {
    return this.get(`/cohorts/${kind}/${slug}/rankings`, params);
  }

  /** Facet-level scores, cohort-relative (Pro).
   *  `GET /cohorts/{kind}/{slug}/scores` */
  getCohortScores(kind, slug, params = {}) {
    return this.get(`/cohorts/${kind}/${slug}/scores`, params);
  }

  /** The distribution for a whole market (Pro).
   *  `GET /cohorts/{kind}/{slug}/stats` */
  getCohortStats(kind, slug, params = {}) {
    return this.get(`/cohorts/${kind}/${slug}/stats`, params);
  }

  /** A company's weakest dimensions.
   *  `GET /insights/company/{slug}/gaps` */
  getCompanyGaps(slug, params = {}) {
    return this.get(`/insights/company/${slug}/gaps`, params);
  }

  /** One company's demand-side profile.
   *  `GET /insights/company/{slug}` */
  getCompanyInsight(slug, params = {}) {
    return this.get(`/insights/company/${slug}`, params);
  }

  /** Get one industry, with its ranked providers.
   *  `GET /industries/{slug}` */
  getIndustry(slug, params = {}) {
    return this.get(`/industries/${slug}`, params);
  }

  /** Top-rated providers in an industry.
   *  `GET /industries/{slug}/leaders` */
  getIndustryLeaders(slug, params = {}) {
    return this.get(`/industries/${slug}/leaders`, params);
  }

  /** Insights overview.
   *  `GET /insights` */
  getInsightsSummary(params = {}) {
    return this.get(`/insights`, params);
  }

  /** Get a list, members resolved to current name/band/score.
   *  `GET /me/lists/{id}` */
  getList(id, params = {}) {
    return this.get(`/me/lists/${id}`, params);
  }

  /** An API's primary OpenAPI.
   *  `GET /openapis/{aid}` */
  getOpenapi(aid, params = {}) {
    return this.get(`/openapis/${aid}`, params);
  }

  /** Get one provider.
   *  `GET /providers/{slug}` */
  getProvider(slug, params = {}) {
    return this.get(`/providers/${slug}`, params);
  }

  /** Agent-readiness dimensions (Pro).
   *  `GET /providers/{slug}/agent-readiness` */
  getProviderAgentReadiness(slug, params = {}) {
    return this.get(`/providers/${slug}/agent-readiness`, params);
  }

  /** Every artifact a provider publishes.
   *  `GET /providers/{slug}/artifacts` */
  getProviderArtifacts(slug, params = {}) {
    return this.get(`/providers/${slug}/artifacts`, params);
  }

  /** What one provider publishes, counted.
   *  `GET /providers/{slug}/capabilities` */
  getProviderCapabilities(slug, params = {}) {
    return this.get(`/providers/${slug}/capabilities`, params);
  }

  /** How the score was established.
   *  `GET /providers/{slug}/evidence` */
  getProviderEvidence(slug, params = {}) {
    return this.get(`/providers/${slug}/evidence`, params);
  }

  /** One provider's score at facet depth (Pro).
   *  `GET /providers/{slug}/rating/facets` */
  getProviderFacets(slug, params = {}) {
    return this.get(`/providers/${slug}/rating/facets`, params);
  }

  /** Which VC firms back this provider (reverse portfolio edge).
   *  `GET /providers/{slug}/investors` */
  getProviderInvestors(slug, params = {}) {
    return this.get(`/providers/${slug}/investors`, params);
  }

  /** A provider's getting-started view.
   *  `GET /providers/{slug}/onboarding` */
  getProviderOnboarding(slug, params = {}) {
    return this.get(`/providers/${slug}/onboarding`, params);
  }

  /** Every operation a provider exposes.
   *  `GET /providers/{slug}/operations` */
  getProviderOperations(slug, params = {}) {
    return this.page(`/providers/${slug}/operations`, params);
  }

  /** One provider's rating.
   *  `GET /providers/{slug}/rating` */
  getProviderRating(slug, params = {}) {
    return this.get(`/providers/${slug}/rating`, params);
  }

  /** Every JSON Schema a provider publishes.
   *  `GET /providers/{slug}/schema` */
  getProviderSchema(slug, params = {}) {
    return this.page(`/providers/${slug}/schema`, params);
  }

  /** Every MCP tool a provider ships.
   *  `GET /providers/{slug}/tools` */
  getProviderTools(slug, params = {}) {
    return this.page(`/providers/${slug}/tools`, params);
  }

  /** A provider's rating movement.
   *  `GET /providers/{slug}/rating/history` */
  getRatingHistory(slug, params = {}) {
    return this.get(`/providers/${slug}/rating/history`, params);
  }

  /** The rating rubric.
   *  `GET /ratings/rubric` */
  getRatingRubric(params = {}) {
    return this.get(`/ratings/rubric`, params);
  }

  /** Get one region, with its ranked providers.
   *  `GET /regions/{slug}` */
  getRegion(slug, params = {}) {
    return this.get(`/regions/${slug}`, params);
  }

  /** Top-rated providers in a region.
   *  `GET /regions/{slug}/leaders` */
  getRegionLeaders(slug, params = {}) {
    return this.get(`/regions/${slug}/leaders`, params);
  }

  /** Get one tag, with its linked providers, APIs, and neighbors.
   *  `GET /tags/{slug}` */
  getTag(slug, params = {}) {
    return this.get(`/tags/${slug}`, params);
  }

  /** One VC firm — identity, fund facts, portfolio summary.
   *  `GET /vcs/{slug}` */
  getVc(slug, params = {}) {
    return this.get(`/vcs/${slug}`, params);
  }

  /** A VC firm's portfolio graph.
   *  `GET /vcs/{slug}/portfolio` */
  getVcPortfolio(slug, params = {}) {
    return this.get(`/vcs/${slug}/portfolio`, params);
  }

  /** Artifact gaps across a whole industry.
   *  `GET /gaps/industry/{slug}` */
  industryGapAnalysis(slug, params = {}) {
    return this.get(`/gaps/industry/${slug}`, params);
  }

  /** List and filter APIs across the network.
   *  `GET /apis` */
  listApis(params = {}) {
    return this.page(`/apis`, params);
  }

  /** APIs.json indexes across the catalog.
   *  `GET /apis-json` */
  listApisJson(params = {}) {
    return this.page(`/apis-json`, params);
  }

  /** List arazzo workflows across the catalog.
   *  `GET /arazzo` */
  listArazzo(params = {}) {
    return this.page(`/arazzo`, params);
  }

  /** List and filter areas (Pro).
   *  `GET /areas` */
  listAreas(params = {}) {
    return this.page(`/areas`, params);
  }

  /** List asyncapi specifications across the catalog.
   *  `GET /asyncapis` */
  listAsyncapis(params = {}) {
    return this.page(`/asyncapis`, params);
  }

  /** List AsyncAPI event channels across the catalog.
   *  `GET /channels` */
  listChannels(params = {}) {
    return this.page(`/channels`, params);
  }

  /** Every scored cohort in the catalog.
   *  `GET /cohorts` */
  listCohorts(params = {}) {
    return this.page(`/cohorts`, params);
  }

  /** List api collections across the catalog.
   *  `GET /collections` */
  listCollections(params = {}) {
    return this.page(`/collections`, params);
  }

  /** List examples across the catalog.
   *  `GET /examples` */
  listExamples(params = {}) {
    return this.page(`/examples`, params);
  }

  /** List finops artifacts across the catalog.
   *  `GET /finops` */
  listFinops(params = {}) {
    return this.page(`/finops`, params);
  }

  /** List graphql schemas across the catalog.
   *  `GET /graphql` */
  listGraphql(params = {}) {
    return this.page(`/graphql`, params);
  }

  /** List and filter industries.
   *  `GET /industries` */
  listIndustries(params = {}) {
    return this.page(`/industries`, params);
  }

  /** Services / tools / standards by adoption.
   *  `GET /insights/adoption` */
  listInsightAdoption(params = {}) {
    return this.page(`/insights/adoption`, params);
  }

  /** Browse profiled companies.
   *  `GET /insights/companies` */
  listInsightCompanies(params = {}) {
    return this.page(`/insights/companies`, params);
  }

  /** Rank the investment dimensions.
   *  `GET /insights/dimensions` */
  listInsightDimensions(params = {}) {
    return this.page(`/insights/dimensions`, params);
  }

  /** Industry rollup.
   *  `GET /insights/industries` */
  listInsightIndustries(params = {}) {
    return this.page(`/insights/industries`, params);
  }

  /** List json-ld contexts across the catalog.
   *  `GET /json-ld` */
  listJsonLd(params = {}) {
    return this.page(`/json-ld`, params);
  }

  /** List json schema definitions across the catalog.
   *  `GET /json-schemas` */
  listJsonSchemas(params = {}) {
    return this.page(`/json-schemas`, params);
  }

  /** List json structure definitions across the catalog.
   *  `GET /json-structures` */
  listJsonStructures(params = {}) {
    return this.page(`/json-structures`, params);
  }

  /** List the lists/shortlists you own.
   *  `GET /me/lists` */
  listLists(params = {}) {
    return this.get(`/me/lists`, params);
  }

  /** List published MCP servers across the catalog.
   *  `GET /mcp` */
  listMcpServers(params = {}) {
    return this.page(`/mcp`, params);
  }

  /** List openapi specifications across the catalog.
   *  `GET /openapis` */
  listOpenapis(params = {}) {
    return this.page(`/openapis`, params);
  }

  /** List plans across the catalog.
   *  `GET /plans` */
  listPlans(params = {}) {
    return this.page(`/plans`, params);
  }

  /** List postman collections across the catalog.
   *  `GET /postman` */
  listPostman(params = {}) {
    return this.page(`/postman`, params);
  }

  /** List the APIs published by a provider.
   *  `GET /providers/{slug}/apis` */
  listProviderApis(slug, params = {}) {
    return this.page(`/providers/${slug}/apis`, params);
  }

  /** List and filter providers.
   *  `GET /providers` */
  listProviders(params = {}) {
    return this.page(`/providers`, params);
  }

  /** List rate limits across the catalog.
   *  `GET /rate-limits` */
  listRateLimits(params = {}) {
    return this.page(`/rate-limits`, params);
  }

  /** Ranked ratings leaderboard.
   *  `GET /ratings` */
  listRatings(params = {}) {
    return this.page(`/ratings`, params);
  }

  /** List and filter regions.
   *  `GET /regions` */
  listRegions(params = {}) {
    return this.page(`/regions`, params);
  }

  /** List governance rulesets across the catalog.
   *  `GET /rules` */
  listRules(params = {}) {
    return this.page(`/rules`, params);
  }

  /** List your saved searches.
   *  `GET /me/searches` */
  listSavedSearches(params = {}) {
    return this.get(`/me/searches`, params);
  }

  /** List OAuth scope sets across the catalog.
   *  `GET /scopes` */
  listScopes(params = {}) {
    return this.page(`/scopes`, params);
  }

  /** List security scheme definitions across the catalog.
   *  `GET /security` */
  listSecurity(params = {}) {
    return this.page(`/security`, params);
  }

  /** List published Agent Skills across the catalog.
   *  `GET /skills` */
  listSkills(params = {}) {
    return this.page(`/skills`, params);
  }

  /** List and rank tags.
   *  `GET /tags` */
  listTags(params = {}) {
    return this.page(`/tags`, params);
  }

  /** List / search venture-capital firms.
   *  `GET /vcs` */
  listVcs(params = {}) {
    return this.page(`/vcs`, params);
  }

  /** Match providers to a company's stack (the supply↔demand join).
   *  `GET /insights/company/{slug}/match` */
  matchCompanyProviders(slug, params = {}) {
    return this.get(`/insights/company/${slug}/match`, params);
  }

  /** Per-check Kin Score results for this provider
   *  `GET /providers/{slug}/rating/checks` */
  providerRatingChecks(slug, params = {}) {
    return this.get(`/providers/${slug}/rating/checks`, params);
  }

  /** Band gates for this provider, and what is unmet
   *  `GET /providers/{slug}/gates` */
  readinessGates(slug, params = {}) {
    return this.get(`/providers/${slug}/gates`, params);
  }

  /** Design a recommended API stack per capability.
   *  `GET /stack` */
  recommendStack(params = {}) {
    return this.get(`/stack`, params);
  }

  /** Report that the catalog has this provider wrong
   *  `POST /providers/{slug}/correction` */
  reportCorrection(slug, body = null, params = {}) {
    return this.request('POST', `/providers/${slug}/correction`, { params, json: body });
  }

  /** Tell us what you looked for and did not find
   *  `POST /gaps/report` */
  reportGap(body = null, params = {}) {
    return this.request('POST', `/gaps/report`, { params, json: body });
  }

  /** Ask for a provider, industry, tag or area to be re-profiled
   *  `POST /checks` */
  requestCheck(body = null, params = {}) {
    return this.request('POST', `/checks`, { params, json: body });
  }

  /** Resolve any identifier (domain / URL / GitHub org) to a provider.
   *  `GET /resolve` */
  resolveIdentifier(params = {}) {
    return this.get(`/resolve`, params);
  }

  /** Re-run a saved search against the live catalog.
   *  `GET /me/searches/{id}/results` */
  runSavedSearch(id, params = {}) {
    return this.get(`/me/searches/${id}/results`, params);
  }

  /** What's NEW for a saved search since you last checked.
   *  `GET /me/searches/{id}/net_new` */
  savedSearchNetNew(id, params = {}) {
    return this.get(`/me/searches/${id}/net_new`, params);
  }

  /** Unified search across apis, providers, tags, and artifacts.
   *  `GET /search` */
  search(params = {}) {
    return this.get(`/search`, params);
  }

  /** Request restricted listing or removal
   *  `POST /providers/{slug}/visibility` */
  setVisibility(slug, body = null, params = {}) {
    return this.request('POST', `/providers/${slug}/visibility`, { params, json: body });
  }

  /** What a set of fixes would move the score to
   *  `POST /providers/{slug}/projection` */
  simulateFixes(slug, body = null, params = {}) {
    return this.request('POST', `/providers/${slug}/projection`, { params, json: body });
  }

  /** Story leads from catalog movement (owner).
   *  `GET /story-leads` */
  storyLeads(params = {}) {
    return this.get(`/story-leads`, params);
  }

  /** Create or update an artifact pointer for this listing
   *  `POST /providers/{slug}/submit` */
  submitArtifact(slug, body = null, params = {}) {
    return this.request('POST', `/providers/${slug}/submit`, { params, json: body });
  }

  /** The ranked, costed punch list for this provider
   *  `GET /providers/{slug}/remediation` */
  whatCanIFix(slug, params = {}) {
    return this.get(`/providers/${slug}/remediation`, params);
  }

  /** What changed in the catalog since a date (Pro).
   *  `GET /changes` */
  whatsChanged(params = {}) {
    return this.get(`/changes`, params);
  }
}
