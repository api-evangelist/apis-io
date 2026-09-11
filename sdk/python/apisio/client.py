"""apis.io Python client — the core transport.

Deliberately small. The 110 operation methods in `operations.py` are GENERATED from the OpenAPI
documents apis.io publishes, so the client cannot drift from the contract; everything that needs a
human decision lives here.

Three things this handles that a raw `requests` call does not, and they are the reason a client
library is worth having for this API rather than just a wrapper:

1. **401 and 402 mean different things.** A 401 says "you have not authenticated" and carries an
   RFC 9728 challenge naming the resource-metadata document you bootstrap from. A 402 says "you
   are authenticated and this costs more" and names the plan. Collapsing them — which is what a
   bare `raise_for_status()` does — is the single most common way an agent gets stuck here.
2. **The challenge does not arrive under its standard name.** API Gateway reserves
   `WWW-Authenticate` and renames it; the value arrives as `x-auth-challenge` (and
   `x-amzn-remapped-www-authenticate`). `Unauthenticated.resource_metadata` reads all three, so
   callers never have to know that.
3. **Rate-limit state is in response headers**, not in the body, and is what you back off on.

No dependencies beyond the standard library.
"""

from __future__ import annotations

import http.client
import json as _json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Iterator, Mapping

__all__ = [
    "Client",
    "ApisIoError",
    "Unauthenticated",
    "PaymentRequired",
    "RateLimited",
    "NotFound",
    "Page",
    "RateLimit",
]

DEFAULT_BASE_URL = "https://apis.io/api/v1"
USER_AGENT = "apisio-python/0.1.0 (+https://apis.io)"


class ApisIoError(Exception):
    """Any non-2xx answer. Carries the parsed body, because this API always explains itself."""

    def __init__(self, status: int, body: Any, headers: Mapping[str, str], url: str):
        self.status = status
        self.body = body if isinstance(body, dict) else {"detail": body}
        self.headers = {k.lower(): v for k, v in dict(headers or {}).items()}
        self.url = url
        detail = self.body.get("detail") or self.body.get("error") or str(body)[:200]
        super().__init__(f"{status} {self.body.get('error', 'error')}: {detail}")

    @property
    def error(self) -> str | None:
        return self.body.get("error")


class Unauthenticated(ApisIoError):
    """401 — you have no credential. The challenge tells you how to get one.

    This is NOT a paywall. An agent that has never authenticated should read
    `resource_metadata`, fetch that document, and register. See RFC 9728.
    """

    @property
    def resource_metadata(self) -> str | None:
        """The RFC 9728 metadata URL, from whichever header actually survived the hop.

        `www-authenticate` is reserved by API Gateway and renamed on the way out, and the
        CloudFront function that would rename it back is not invoked on error responses. The
        origin therefore also emits `x-auth-challenge`, which is the one that reliably arrives.
        """
        for name in ("www-authenticate", "x-auth-challenge",
                     "x-amzn-remapped-www-authenticate"):
            raw = self.headers.get(name)
            if not raw:
                continue
            m = re.search(r'resource_metadata="([^"]+)"', raw)
            if m:
                return m.group(1)
        return None

    @property
    def scope(self) -> str | None:
        for name in ("www-authenticate", "x-auth-challenge",
                     "x-amzn-remapped-www-authenticate"):
            raw = self.headers.get(name)
            if raw:
                m = re.search(r'scope="([^"]+)"', raw)
                if m:
                    return m.group(1)
        return None


class PaymentRequired(ApisIoError):
    """402 — you are authenticated and this resource needs a higher plan."""

    @property
    def tier(self) -> str | None:
        return self.body.get("tier")

    @property
    def plans_url(self) -> str | None:
        return self.body.get("plans")


class RateLimited(ApisIoError):
    """429 — slow down. `retry_after` is seconds, when the server said."""

    @property
    def retry_after(self) -> float | None:
        v = self.headers.get("retry-after")
        try:
            return float(v) if v is not None else None
        except ValueError:
            return None


class NotFound(ApisIoError):
    """404 — no such provider, api, tag or dataset."""


class RateLimit:
    """What the response headers said about your remaining budget."""

    __slots__ = ("tier", "limit", "window", "policy")

    def __init__(self, headers: Mapping[str, str]):
        h = {k.lower(): v for k, v in dict(headers or {}).items()}
        self.tier = h.get("x-ratelimit-tier")
        self.window = _int_or_none(h.get("x-ratelimit-window"))
        self.limit = _int_or_none(h.get("x-ratelimit-limit"))
        self.policy = h.get("ratelimit-policy")

    def __repr__(self) -> str:
        return f"RateLimit(tier={self.tier!r}, limit={self.limit}, window={self.window})"


def _int_or_none(v: str | None) -> int | None:
    try:
        return int(v) if v is not None else None
    except (TypeError, ValueError):
        return None


class Page(list):
    """A page of results: a real list, plus the `meta` block that says where you are.

    Subclassing list is deliberate — the common case is iterating results, and making callers
    reach for `.data` to do that is friction with no payoff. `meta`, `total` and `rate_limit`
    ride alongside for when you need them.
    """

    def __init__(self, data: list, meta: dict | None = None,
                 rate_limit: RateLimit | None = None, raw: dict | None = None):
        super().__init__(data or [])
        self.meta = meta or {}
        self.rate_limit = rate_limit
        self.raw = raw or {}

    @property
    def total(self) -> int | None:
        return self.meta.get("total")

    @property
    def page(self) -> int | None:
        return self.meta.get("page")

    @property
    def pages(self) -> int | None:
        return self.meta.get("pages")

    def __repr__(self) -> str:
        return f"<Page {len(self)} of {self.total} (page {self.page}/{self.pages})>"


class Client:
    """A client for apis.io.

        from apisio import Client
        api = Client()                       # keyless free tier
        api = Client(api_key="...")          # a plan

    Most of the catalog is free and needs no key: search, providers, apis, tags, taxonomy and
    artifacts. Anything that synthesises across it — ratings, cohorts, insights — needs a plan,
    and you will get a `PaymentRequired` naming which one.
    """

    def __init__(self, api_key: str | None = None, base_url: str = DEFAULT_BASE_URL,
                 timeout: float = 30.0, max_retries: int = 2,
                 user_agent: str = USER_AGENT):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.user_agent = user_agent
        self.last_rate_limit: RateLimit | None = None

    # -- transport ------------------------------------------------------------------------
    def request(self, method: str, path: str, *, params: Mapping[str, Any] | None = None,
                json: Any = None) -> Any:
        """One HTTP call. Returns the parsed body; raises a typed error on non-2xx."""
        url = self.base_url + "/" + path.lstrip("/")
        query = _clean_params(params)
        if query:
            url += "?" + urllib.parse.urlencode(query, doseq=True)

        body = None
        headers = {"accept": "application/json", "user-agent": self.user_agent}
        if json is not None:
            body = _json.dumps(json).encode()
            headers["content-type"] = "application/json"
        # Omit the header entirely for the keyless free tier — sending an empty or wrong key is
        # an `invalid_key` 401, which reads like a bug and is not one.
        if self.api_key:
            headers["x-api-key"] = self.api_key

        attempt = 0
        while True:
            req = urllib.request.Request(url, data=body, headers=headers, method=method.upper())
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    self.last_rate_limit = RateLimit(resp.headers)
                    raw = resp.read()
                    return _json.loads(raw) if raw else None
            except urllib.error.HTTPError as e:
                raw = e.read()
                try:
                    parsed = _json.loads(raw) if raw else {}
                except ValueError:
                    parsed = {"detail": raw.decode("utf-8", "replace")[:500]}
                self.last_rate_limit = RateLimit(e.headers)
                err = _error_for(e.code, parsed, e.headers, url)
                # Retry only what retrying can fix. A 402 will never become a 200 by asking again.
                if isinstance(err, RateLimited) and attempt < self.max_retries:
                    time.sleep(err.retry_after or (2 ** attempt))
                    attempt += 1
                    continue
                if e.code >= 500 and attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    attempt += 1
                    continue
                raise err from None
            except urllib.error.URLError as e:
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    attempt += 1
                    continue
                raise ApisIoError(0, {"error": "network", "detail": str(e.reason)}, {}, url) from None
            except (http.client.HTTPException, OSError) as e:
                # A reset connection, a half-closed keep-alive, a DNS blip. urllib raises these
                # RAW rather than wrapping them in URLError, so catching only URLError lets a
                # transient network fault escape as an unrelated traceback — which is exactly
                # what it did on the 40th call of a 93-call run. Retried like any other
                # transport failure, and surfaced as an ApisIoError if it persists, so callers
                # only ever have to catch one family.
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    attempt += 1
                    continue
                raise ApisIoError(0, {"error": "network", "detail": f"{type(e).__name__}: {e}"},
                                  {}, url) from None

    def get(self, path: str, **params: Any) -> Any:
        return self.request("GET", path, params=params)

    def post(self, path: str, json: Any = None, **params: Any) -> Any:
        return self.request("POST", path, params=params, json=json)

    def delete(self, path: str, **params: Any) -> Any:
        return self.request("DELETE", path, params=params)

    # -- envelope -------------------------------------------------------------------------
    def page(self, path: str, **params: Any) -> Page:
        """A list endpoint, as a Page. Collection responses are `{meta, data}`."""
        body = self.get(path, **params)
        if isinstance(body, dict) and isinstance(body.get("data"), list):
            return Page(body["data"], body.get("meta"), self.last_rate_limit, body)
        # A few endpoints answer with a bare list or a single object; do not pretend otherwise.
        return Page(body if isinstance(body, list) else [body], {}, self.last_rate_limit,
                    body if isinstance(body, dict) else {})

    def paginate(self, path: str, *, limit: int = 100, max_pages: int | None = None,
                 **params: Any) -> Iterator[dict]:
        """Walk every page, yielding one record at a time.

        Stops on the server's own `meta.pages` rather than on an empty page, and refuses to loop
        forever if `meta` is missing — an endpoint that does not report `pages` gets exactly one
        page, which is the honest answer rather than an unbounded crawl.
        """
        page_no = 1
        while True:
            p = self.page(path, limit=limit, page=page_no, **params)
            yield from p
            pages = p.pages
            if not pages or page_no >= pages:
                return
            if max_pages and page_no >= max_pages:
                return
            page_no += 1


def _clean_params(params: Mapping[str, Any] | None) -> dict:
    """Drop None, and render booleans the way the API reads them."""
    out: dict[str, Any] = {}
    for k, v in (params or {}).items():
        if v is None:
            continue
        out[k] = "true" if v is True else "false" if v is False else v
    return out


def _error_for(status: int, body: Any, headers: Mapping[str, str], url: str) -> ApisIoError:
    cls = {401: Unauthenticated, 402: PaymentRequired, 404: NotFound,
           429: RateLimited}.get(status, ApisIoError)
    return cls(status, body, headers, url)
