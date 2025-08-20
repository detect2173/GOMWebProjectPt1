from django.test import RequestFactory
from django.http import HttpResponse

from sitecore.middleware import PermissionsPolicyMiddleware


def _dummy_view(_):
    return HttpResponse("ok")


def test_permissions_policy_headers_present():
    rf = RequestFactory()
    request = rf.get("/")
    middleware = PermissionsPolicyMiddleware(_dummy_view)
    response = middleware(request)
    assert response["Permissions-Policy"] == "payment=*"
    assert response["Feature-Policy"] == "payment *"
