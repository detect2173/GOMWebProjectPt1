import json
import logging
import urllib.request

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import LeadMagnetForm
from .models import Lead

logger = logging.getLogger(__name__)


def home(request: HttpRequest) -> HttpResponse:
    """Render homepage. If template rendering fails in production, fall back to a
    minimal inline HTML so visitors don’t see a 500 while we investigate.

    This also logs the exception with full traceback.
    """
    try:
        return render(
            request,
            "sitecore/home.html",
            {
                "calendly_url": settings.CALENDLY_URL,
            },
        )
    except Exception:
        logger.exception("Home page template render failed; serving fallback HTML")
        # Simple, dependency-free fallback to avoid hard 500s in production
        html = (
            "<html><head><meta charset='utf-8'><title>Great Owl Marketing</title>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'></head>"
            "<body style='font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;"
            "margin:40px;line-height:1.6;'>"
            "<h1>Great Owl Marketing</h1>"
            "<p>We’re experiencing a temporary issue rendering the homepage template."
            " The site is still healthy (<a href='/healthz/'>healthz</a> ok)."
            " Please try again shortly.</p>"
            "<p><a href='/pricing/'>Pricing</a> · <a href='/book/'>Book a Call</a> · "
            "<a href='/free-guide/'>Free Guide</a></p>"
            "</body></html>"
        )
        return HttpResponse(html, content_type="text/html")


def pricing(request: HttpRequest) -> HttpResponse:
    return render(request, "sitecore/pricing.html")


def book(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "sitecore/book.html",
        {
            "calendly_url": settings.CALENDLY_URL,
        },
    )


def _subscribe_to_getresponse(name: str, email: str) -> bool:
    api_key = settings.GETRESPONSE_API_KEY
    list_id = settings.GETRESPONSE_LIST_ID
    if not api_key or not list_id:
        logger.warning("GetResponse not configured; skipping API call")
        return False
    # Minimal direct API call using HTTP request. In production, use official SDK or requests.
    url = "https://api.getresponse.com/v3/contacts"
    payload = {
        "email": email,
        "name": name or "",
        "campaign": {"campaignId": list_id},
        "dayOfCycle": 0,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Auth-Token", f"api-key {api_key}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return 200 <= int(resp.status) < 300
    except Exception as e:
        logger.error("GetResponse subscription failed: %s", e)
        return False


def lead_magnet(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LeadMagnetForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            consent = form.cleaned_data["consent"]
            # Save locally
            Lead.objects.get_or_create(
                email=email, defaults={"name": name, "consent": consent}
            )
            # Attempt subscription
            subscribed = _subscribe_to_getresponse(name, email)
            if subscribed:
                messages.success(
                    request, "Check your inbox! Your free guide is on its way."
                )
            else:
                messages.info(
                    request,
                    "Thanks! We saved your email. We will send the free guide shortly.",
                )
            return redirect("free_guide_thanks")
    else:
        form = LeadMagnetForm()
    return render(request, "sitecore/lead_magnet.html", {"form": form})


def lead_thanks(request: HttpRequest) -> HttpResponse:
    return render(request, "sitecore/lead_thanks.html")


# New aliases for clarity and new canonical URLs


def free_guide(request: HttpRequest) -> HttpResponse:
    return lead_magnet(request)


def free_guide_thanks(request: HttpRequest) -> HttpResponse:
    return lead_thanks(request)


def terms(request: HttpRequest) -> HttpResponse:
    return render(request, "sitecore/terms.html")


def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, "sitecore/privacy.html")


def start(request: HttpRequest) -> HttpResponse:
    """Post-payment onboarding form embed page.
    If ONBOARDING_EMBED_URL is provided, we render an iframe; otherwise show instructions.
    """
    return render(
        request,
        "sitecore/start.html",
        {
            "embed_url": getattr(settings, "ONBOARDING_EMBED_URL", ""),
        },
    )


def gom_onboarding(request: HttpRequest) -> HttpResponse:
    """Serve the standalone onboarding form at /gom-onboarding.html (exact filename in URL)."""
    return render(request, "gom-onboarding.html")


def smartpro_agreement(request: HttpRequest) -> HttpResponse:
    """Serve the standalone agreement page at /smartpro-agreement.html (exact filename in URL).
    We'll replace its contents when the embed code is provided.
    """
    return render(request, "smartpro-agreement.html")


def healthz(request: HttpRequest) -> HttpResponse:
    """Lightweight health check endpoint for uptime monitors and debugging 500s.
    Returns 200 OK with a short body and no DB access.
    """
    return HttpResponse("ok", content_type="text/plain")
