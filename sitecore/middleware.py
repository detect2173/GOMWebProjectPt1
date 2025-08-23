from collections.abc import Callable

from django.http import HttpRequest, HttpResponse


class PermissionsPolicyMiddleware:
    """
    Sets explicit Permissions-Policy to avoid noisy console warnings from embeds/extensions
    attempting to access features like the Payment Request API. This does not change any
    app functionality; it simply declares that 'payment' is allowed, which prevents
    Chrome's "Potential permissions policy violation" messages when third-party content
    or extensions probe the API.

    Note: The modern header name is "Permissions-Policy" (previously "Feature-Policy").
    Grammar allows values like (self), (*), ("https://origin.example"). We use (*) to
    allow use from any context inside this document, which is acceptable for a marketing
    site and avoids warnings from embeds such as Calendly.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        # Add headers defensively; never let a header formatting issue break the response.
        try:
            # Allow payment feature to avoid console warnings on pages with embeds/extensions.
            # Send both modern and legacy headers with broadly compatible syntax.
            # Newer syntax (Permissions-Policy): allow all origins
            response["Permissions-Policy"] = "payment=*"
            # Legacy header (Feature-Policy): broad allow for compatibility with older Chromium
            response["Feature-Policy"] = "payment *"
        except Exception:
            # Silently ignore header set failures; functional content must still be served.
            pass
        return response
