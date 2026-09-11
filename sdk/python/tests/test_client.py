"""Tests for the apis.io Python client.

Offline by default — the transport is stubbed, so these run in CI with no network and no key.
Set `APISIO_LIVE=1` to additionally run the handful of tests that call the real API.

They assert BEHAVIOUR that callers depend on, not response content: the catalog moves nightly and
a test pinned to Stripe's composite fails for the wrong reason.
"""

from __future__ import annotations

import io
import json
import os
import sys
import unittest
import urllib.error
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apisio import Client, NotFound, PaymentRequired, Unauthenticated  # noqa: E402
from apisio.client import ApisIoError, Page, RateLimited  # noqa: E402


def _http_error(status, body, headers=None):
    return urllib.error.HTTPError(
        "https://apis.io/api/v1/x", status, "err", headers or {},
        io.BytesIO(json.dumps(body).encode()))


def _ok(body, headers=None):
    resp = mock.MagicMock()
    resp.read.return_value = json.dumps(body).encode()
    resp.headers = headers or {}
    resp.__enter__ = lambda s: s
    resp.__exit__ = lambda s, *a: False
    return resp


class TestEnvelope(unittest.TestCase):
    def test_collection_is_a_list_you_can_iterate(self):
        """The common case is iterating results. Making callers reach for `.data` is friction."""
        body = {"meta": {"total": 2, "page": 1, "pages": 1}, "data": [{"slug": "a"}, {"slug": "b"}]}
        with mock.patch("urllib.request.urlopen", return_value=_ok(body)):
            p = Client().page("/providers")
        self.assertIsInstance(p, Page)
        self.assertEqual([r["slug"] for r in p], ["a", "b"])
        self.assertEqual(p.total, 2)
        self.assertEqual(len(p), 2)

    def test_rate_limit_is_read_from_headers_not_the_body(self):
        hdrs = {"x-ratelimit-tier": "pro", "x-ratelimit-limit": "5000",
                "x-ratelimit-window": "86400"}
        with mock.patch("urllib.request.urlopen", return_value=_ok({"data": [], "meta": {}}, hdrs)):
            c = Client()
            c.page("/providers")
        self.assertEqual(c.last_rate_limit.tier, "pro")
        self.assertEqual(c.last_rate_limit.limit, 5000)

    def test_paginate_stops_on_the_servers_own_page_count(self):
        """An endpoint that does not report `pages` gets exactly one page, not an endless crawl."""
        pages = [
            {"meta": {"pages": 2, "page": 1}, "data": [{"i": 1}]},
            {"meta": {"pages": 2, "page": 2}, "data": [{"i": 2}]},
        ]
        with mock.patch("urllib.request.urlopen", side_effect=[_ok(p) for p in pages]):
            got = list(Client().paginate("/tags", limit=1))
        self.assertEqual([r["i"] for r in got], [1, 2])

        with mock.patch("urllib.request.urlopen", return_value=_ok({"data": [{"i": 1}]})):
            got = list(Client().paginate("/weird"))
        self.assertEqual(len(got), 1, "no `pages` in meta must not become an unbounded crawl")


class TestErrors(unittest.TestCase):
    """401 and 402 are DIFFERENT ANSWERS and the client must not collapse them.

    A 401 says "you have not authenticated" and carries the bootstrap challenge; a 402 says "you
    are authenticated and this costs more". An agent that cannot tell them apart either never
    registers or tries to pay for something it has no identity to buy with.
    """

    def test_401_is_unauthenticated_and_exposes_the_challenge(self):
        hdrs = {"x-auth-challenge":
                'Bearer resource_metadata="https://apis.io/.well-known/oauth-protected-resource/api/v1", scope="apis:pro"'}
        err = _http_error(401, {"error": "unauthorized", "detail": "no credential"}, hdrs)
        with mock.patch("urllib.request.urlopen", side_effect=err):
            with self.assertRaises(Unauthenticated) as ctx:
                Client().get("/ratings")
        self.assertEqual(
            ctx.exception.resource_metadata,
            "https://apis.io/.well-known/oauth-protected-resource/api/v1")
        self.assertEqual(ctx.exception.scope, "apis:pro")

    def test_the_challenge_is_read_from_whichever_header_survived(self):
        """API Gateway renames `www-authenticate`; the value arrives as `x-auth-challenge` or
        `x-amzn-remapped-www-authenticate`. Callers should never have to know that."""
        for name in ("www-authenticate", "x-auth-challenge",
                     "x-amzn-remapped-www-authenticate"):
            err = _http_error(401, {"error": "unauthorized"},
                              {name: 'Bearer resource_metadata="https://x/y"'})
            with mock.patch("urllib.request.urlopen", side_effect=err):
                with self.assertRaises(Unauthenticated) as ctx:
                    Client().get("/ratings")
            self.assertEqual(ctx.exception.resource_metadata, "https://x/y",
                             f"challenge not read from {name}")

    def test_402_names_the_plan_that_would_unlock_it(self):
        err = _http_error(402, {"error": "upgrade_required", "tier": "business",
                                "detail": "The checks endpoint requires the Influence plan.",
                                "plans": "https://apis.io/developer/plans/"})
        with mock.patch("urllib.request.urlopen", side_effect=err):
            with self.assertRaises(PaymentRequired) as ctx:
                Client(api_key="k").post("/checks")
        self.assertEqual(ctx.exception.tier, "business")
        self.assertIn("developer/plans", ctx.exception.plans_url)

    def test_404_is_its_own_type(self):
        err = _http_error(404, {"error": "not_found", "detail": "provider nope"})
        with mock.patch("urllib.request.urlopen", side_effect=err):
            with self.assertRaises(NotFound):
                Client().get("/providers/nope")

    def test_a_402_is_never_retried(self):
        """Retrying a paywall is pure waste — it will never become a 200 by asking again."""
        err = _http_error(402, {"error": "upgrade_required"})
        with mock.patch("urllib.request.urlopen", side_effect=err) as m:
            with self.assertRaises(PaymentRequired):
                Client(api_key="k", max_retries=3).get("/ratings")
        self.assertEqual(m.call_count, 1)

    def test_a_429_is_retried_and_carries_retry_after(self):
        err = _http_error(429, {"error": "rate_limited"}, {"retry-after": "0"})
        with mock.patch("urllib.request.urlopen", side_effect=err) as m:
            with self.assertRaises(RateLimited):
                Client(max_retries=2).get("/providers")
        self.assertEqual(m.call_count, 3, "429 should be retried up to max_retries")

    def test_every_error_keeps_the_parsed_body(self):
        err = _http_error(400, {"error": "bad_request", "detail": "why"})
        with mock.patch("urllib.request.urlopen", side_effect=err):
            with self.assertRaises(ApisIoError) as ctx:
                Client().get("/x")
        self.assertEqual(ctx.exception.body["detail"], "why")


class TestRequestShaping(unittest.TestCase):
    def test_no_key_means_NO_HEADER_not_an_empty_one(self):
        """An empty or wrong key is an `invalid_key` 401, which reads like a bug and is not one.
        The free tier is keyless — the header must be omitted entirely."""
        captured = {}

        def fake(req, **kw):
            captured["headers"] = dict(req.header_items())
            return _ok({"data": [], "meta": {}})

        with mock.patch("urllib.request.urlopen", side_effect=fake):
            Client().get("/providers")
        self.assertNotIn("X-api-key", captured["headers"])
        self.assertNotIn("x-api-key", {k.lower(): v for k, v in captured["headers"].items()})

    def test_none_params_are_dropped_and_bools_are_rendered(self):
        captured = {}

        def fake(req, **kw):
            captured["url"] = req.full_url
            return _ok({"data": [], "meta": {}})

        with mock.patch("urllib.request.urlopen", side_effect=fake):
            Client().page("/providers", q="x", tags=None, verified=True, stale=False)
        self.assertIn("q=x", captured["url"])
        self.assertNotIn("tags=", captured["url"], "a None filter must not be sent as empty")
        self.assertIn("verified=true", captured["url"])
        self.assertIn("stale=false", captured["url"])


class TestGeneratedBindings(unittest.TestCase):
    def test_path_parameters_are_real_arguments(self):
        """The generator derives these from the path TEMPLATE, because every declaration in these
        documents is a $ref the first version could not see — and produced 108 methods, not one of
        them taking a slug."""
        captured = {}

        def fake(req, **kw):
            captured["url"] = req.full_url
            return _ok({"slug": "stripe"})

        with mock.patch("urllib.request.urlopen", side_effect=fake):
            Client().get_provider_rating("stripe")
        self.assertIn("/providers/stripe/rating", captured["url"])

        with mock.patch("urllib.request.urlopen", side_effect=fake):
            Client().get_cohort("industry", "payments")
        self.assertIn("/cohorts/industry/payments", captured["url"])

    def test_the_surface_is_bound_and_named_in_snake_case(self):
        for name in ("list_providers", "get_provider", "search", "get_provider_rating",
                     "what_can_i_fix", "readiness_gates", "claim_listing", "submit_artifact",
                     "list_tags", "get_rating_rubric"):
            self.assertTrue(callable(getattr(Client, name, None)), f"{name} is not bound")

    def test_collections_return_a_page_and_singles_do_not(self):
        with mock.patch("urllib.request.urlopen",
                        return_value=_ok({"meta": {"total": 1}, "data": [{"slug": "a"}]})):
            self.assertIsInstance(Client().list_providers(), Page)
        with mock.patch("urllib.request.urlopen", return_value=_ok({"slug": "stripe"})):
            self.assertIsInstance(Client().get_provider("stripe"), dict)


@unittest.skipUnless(os.environ.get("APISIO_LIVE"), "set APISIO_LIVE=1 to call the real API")
class TestLive(unittest.TestCase):
    def test_the_free_tier_works_with_no_key(self):
        p = Client().list_providers(limit=2)
        self.assertTrue(len(p) > 0)
        self.assertIsNotNone(p.total)

    def test_a_gated_resource_refuses_in_a_way_the_caller_can_act_on(self):
        with self.assertRaises((PaymentRequired, Unauthenticated)) as ctx:
            Client().what_can_i_fix("stripe")
        e = ctx.exception
        actionable = getattr(e, "plans_url", None) or getattr(e, "resource_metadata", None)
        self.assertTrue(actionable, "a refusal with no way forward is not an answer")

    def test_search_answers_in_sections(self):
        """roadmap#308: /search is sectioned, not a {meta,data} collection."""
        r = Client().search(q="payments", limit=2)
        self.assertIn("providers", r)
        self.assertIn("total", r["providers"])


if __name__ == "__main__":
    unittest.main()
