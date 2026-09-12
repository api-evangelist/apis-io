/**
 * apis.io JavaScript client — the core transport.
 *
 * Deliberately small, and deliberately the same shape as the Python client beside it: the
 * operation bindings in `operations.js` are GENERATED from the OpenAPI documents apis.io
 * publishes, by the same generator, so the two cannot drift from each other or from the contract.
 *
 * Three things this handles that a bare `fetch` does not, and they are the reason a client library
 * is worth having for this API rather than a thin wrapper:
 *
 *   1. 401 and 402 MEAN DIFFERENT THINGS. A 401 says "you have not authenticated" and carries an
 *      RFC 9728 challenge naming the resource-metadata document to bootstrap from. A 402 says "you
 *      are authenticated and this costs more" and names the plan. Collapsing them — which
 *      `if (!res.ok) throw` does — is the most common way an agent gets stuck here.
 *   2. THE CHALLENGE DOES NOT ARRIVE UNDER ITS STANDARD NAME. API Gateway reserves
 *      `WWW-Authenticate` and renames it; the value arrives as `x-auth-challenge` (and
 *      `x-amzn-remapped-www-authenticate`). `Unauthenticated#resourceMetadata` reads all three.
 *   3. RATE-LIMIT STATE IS IN RESPONSE HEADERS, not the body, and is what you back off on.
 *
 * No dependencies. Works on Node 18+ and in a browser (the API sends CORS headers, and since
 * roadmap#292 it exposes the challenge header a browser needs).
 */

export const DEFAULT_BASE_URL = 'https://apis.io/api/v1';
export const USER_AGENT = 'apisio-js/0.1.0 (+https://apis.io)';

/** Any non-2xx answer. Carries the parsed body, because this API always explains itself. */
export class ApisIoError extends Error {
  constructor(status, body, headers, url) {
    const b = body && typeof body === 'object' ? body : { detail: String(body ?? '') };
    super(`${status} ${b.error ?? 'error'}: ${b.detail ?? b.error ?? ''}`);
    this.name = 'ApisIoError';
    this.status = status;
    this.body = b;
    this.headers = headers ?? {};
    this.url = url;
  }

  get error() { return this.body.error ?? null; }
}

/**
 * 401 — you have no credential. This is NOT a paywall: the challenge tells you how to get one.
 * An agent that has never authenticated should read `resourceMetadata`, fetch that document and
 * register. See RFC 9728.
 */
export class Unauthenticated extends ApisIoError {
  #challenge() {
    for (const n of ['www-authenticate', 'x-auth-challenge', 'x-amzn-remapped-www-authenticate']) {
      const v = this.headers[n];
      if (v) return v;
    }
    return null;
  }

  get resourceMetadata() {
    const m = /resource_metadata="([^"]+)"/.exec(this.#challenge() ?? '');
    return m ? m[1] : null;
  }

  get scope() {
    const m = /scope="([^"]+)"/.exec(this.#challenge() ?? '');
    return m ? m[1] : null;
  }
}

/** 402 — you are authenticated and this resource needs a higher plan. */
export class PaymentRequired extends ApisIoError {
  get tier() { return this.body.tier ?? null; }
  get plansUrl() { return this.body.plans ?? null; }
}

/** 429 — slow down. `retryAfter` is seconds, when the server said. */
export class RateLimited extends ApisIoError {
  get retryAfter() {
    const v = Number(this.headers['retry-after']);
    return Number.isFinite(v) ? v : null;
  }
}

/** 404 — no such provider, api, tag or dataset. */
export class NotFound extends ApisIoError {}

/** What the response headers said about your remaining budget. */
export class RateLimit {
  constructor(headers) {
    const int = (v) => (Number.isFinite(Number(v)) && v !== null && v !== '' ? Number(v) : null);
    this.tier = headers['x-ratelimit-tier'] ?? null;
    this.limit = int(headers['x-ratelimit-limit']);
    this.window = int(headers['x-ratelimit-window']);
    this.policy = headers['ratelimit-policy'] ?? null;
  }
}

/**
 * A page of results: a real Array, plus the `meta` block saying where you are.
 *
 * Extending Array is deliberate — the common case is iterating results, and making callers reach
 * for `.data` to do that is friction with no payoff.
 */
export class Page extends Array {
  static of(data, meta, rateLimit, raw) {
    const p = Page.from(data ?? []);
    p.meta = meta ?? {};
    p.rateLimit = rateLimit ?? null;
    p.raw = raw ?? {};
    return p;
  }

  get total() { return this.meta?.total ?? null; }
  get page() { return this.meta?.page ?? null; }
  get pages() { return this.meta?.pages ?? null; }
}

const cleanParams = (params) => {
  const out = {};
  for (const [k, v] of Object.entries(params ?? {})) {
    if (v === null || v === undefined) continue;
    out[k] = v === true ? 'true' : v === false ? 'false' : String(v);
  }
  return out;
};

const errorFor = (status, body, headers, url) => {
  const C = { 401: Unauthenticated, 402: PaymentRequired, 404: NotFound, 429: RateLimited }[status]
    ?? ApisIoError;
  return new C(status, body, headers, url);
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/**
 * A client for apis.io.
 *
 *   const api = new Client();                      // keyless free tier
 *   const api = new Client({ apiKey: '...' });     // a plan
 *
 * Most of the catalog is free and needs no key. Anything that synthesises across it — ratings,
 * cohorts, insights — needs a plan, and you get a `PaymentRequired` naming which one.
 */
export class Transport {
  constructor({ apiKey = null, baseUrl = DEFAULT_BASE_URL, timeout = 30000, maxRetries = 2,
                userAgent = USER_AGENT, fetch: f = null } = {}) {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.timeout = timeout;
    this.maxRetries = maxRetries;
    this.userAgent = userAgent;
    this._fetch = f ?? globalThis.fetch?.bind(globalThis);
    this.lastRateLimit = null;
    if (!this._fetch) throw new Error('no fetch available — pass one, or use Node 18+');
  }

  async request(method, path, { params = null, json = null } = {}) {
    const qs = new URLSearchParams(cleanParams(params)).toString();
    const url = `${this.baseUrl}/${String(path).replace(/^\/+/, '')}${qs ? `?${qs}` : ''}`;

    const headers = { accept: 'application/json' };
    // A browser refuses to set user-agent; setting it there throws rather than being ignored.
    if (typeof window === 'undefined') headers['user-agent'] = this.userAgent;
    // Omit the header entirely for the keyless free tier — an empty or wrong key is an
    // `invalid_key` 401, which reads like a bug and is not one.
    if (this.apiKey) headers['x-api-key'] = this.apiKey;
    if (json !== null) headers['content-type'] = 'application/json';

    for (let attempt = 0; ; attempt += 1) {
      let res;
      try {
        res = await this._fetch(url, {
          method: method.toUpperCase(),
          headers,
          body: json === null ? undefined : JSON.stringify(json),
          signal: AbortSignal.timeout(this.timeout),
        });
      } catch (e) {
        // A reset connection, a DNS blip, an abort. Retried like any other transport failure and
        // surfaced as an ApisIoError, so callers only ever catch one family.
        if (attempt < this.maxRetries) { await sleep(2 ** attempt * 1000); continue; }
        throw new ApisIoError(0, { error: 'network', detail: String(e?.message ?? e) }, {}, url);
      }

      const hdrs = {};
      res.headers.forEach((v, k) => { hdrs[k.toLowerCase()] = v; });
      this.lastRateLimit = new RateLimit(hdrs);

      const text = await res.text();
      let body = null;
      if (text) { try { body = JSON.parse(text); } catch { body = { detail: text.slice(0, 500) }; } }
      if (res.ok) return body;

      const err = errorFor(res.status, body ?? {}, hdrs, url);
      // Retry only what retrying can fix. A 402 will never become a 200 by asking again.
      if (err instanceof RateLimited && attempt < this.maxRetries) {
        await sleep((err.retryAfter ?? 2 ** attempt) * 1000);
        continue;
      }
      if (res.status >= 500 && attempt < this.maxRetries) { await sleep(2 ** attempt * 1000); continue; }
      throw err;
    }
  }

  get(path, params) { return this.request('GET', path, { params }); }
  post(path, json, params) { return this.request('POST', path, { params, json }); }
  delete(path, params) { return this.request('DELETE', path, { params }); }

  /** A list endpoint, as a Page. Collection responses are `{meta, data}`. */
  async page(path, params) {
    const body = await this.get(path, params);
    if (body && typeof body === 'object' && Array.isArray(body.data)) {
      return Page.of(body.data, body.meta, this.lastRateLimit, body);
    }
    // A few endpoints answer with a bare list or a single object; do not pretend otherwise.
    return Page.of(Array.isArray(body) ? body : [body], {}, this.lastRateLimit,
                   body && typeof body === 'object' ? body : {});
  }

  /**
   * Walk every page, yielding one record at a time. Stops on the server's own `meta.pages`
   * rather than on an empty page, and an endpoint that reports no `pages` gets exactly one —
   * the honest answer rather than an unbounded crawl.
   */
  async *paginate(path, { limit = 100, maxPages = null, ...params } = {}) {
    for (let page = 1; ; page += 1) {
      const p = await this.page(path, { ...params, limit, page });
      yield* p;
      if (!p.pages || page >= p.pages) return;
      if (maxPages && page >= maxPages) return;
    }
  }
}
