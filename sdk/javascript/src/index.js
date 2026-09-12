/**
 * apis.io — the API catalog, as a JavaScript client.
 *
 *   import { Client } from '@apis-io/client';
 *
 *   const api = new Client();                     // keyless free tier
 *   for (const p of await api.listProviders({ q: 'payments', limit: 5 })) console.log(p.slug);
 *
 * Most of the catalog is free and needs no key: search, providers, apis, tags, taxonomy and
 * artifacts. Anything that synthesises across it — ratings, cohorts, insights — needs a plan, and
 * refusing to serve it throws a `PaymentRequired` naming which one.
 *
 * The 108 operation methods are generated from the OpenAPI documents apis.io publishes, by the
 * same generator that emits the Python and Go clients, so the three cannot drift apart.
 */
export { Client } from './operations.js';
export {
  ApisIoError, Unauthenticated, PaymentRequired, RateLimited, NotFound,
  Page, RateLimit, Transport, DEFAULT_BASE_URL,
} from './client.js';
