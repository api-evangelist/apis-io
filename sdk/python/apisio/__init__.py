"""apis.io — the API catalog, as a Python client.

    from apisio import Client

    api = Client()                                  # keyless free tier
    for p in api.list_providers(q="payments", limit=5):
        print(p["slug"], p["name"])

    api.get_provider("stripe")
    api.what_can_i_fix("stripe")                    # needs a plan

Most of the catalog is free and needs no key: search, providers, apis, tags, taxonomy and
artifacts. Anything that synthesises across it — ratings, cohorts, insights, stack design — needs
a plan, and refusing to serve it raises `PaymentRequired` naming which one.

The 108 operation methods are generated from the OpenAPI documents apis.io publishes, so they
cannot drift from the contract. See `generate.py`.
"""

from .client import (
    ApisIoError,
    Client as _Transport,
    NotFound,
    Page,
    PaymentRequired,
    RateLimit,
    RateLimited,
    Unauthenticated,
)
from .operations import Operations

__version__ = "0.1.0"

__all__ = [
    "Client",
    "ApisIoError",
    "Unauthenticated",
    "PaymentRequired",
    "RateLimited",
    "NotFound",
    "Page",
    "RateLimit",
    "__version__",
]


class Client(Operations, _Transport):
    """The apis.io client: transport plus one method per published operation.

    `Operations` comes first in the MRO so the generated bindings are what callers reach, and
    the transport (`request`, `get`, `page`, `paginate`) stays available underneath for anything
    the contract has not caught up with yet.
    """
