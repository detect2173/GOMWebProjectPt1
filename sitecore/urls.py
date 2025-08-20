from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("pricing/", views.pricing, name="pricing"),
    path("book/", views.book, name="book"),
    # New canonical routes for the Free Guide
    path("free-guide/", views.free_guide, name="free_guide"),
    path("free-guide/thanks/", views.free_guide_thanks, name="free_guide_thanks"),
    # Backward-compatible redirects from old slugs
    path(
        "lead-magnet/", RedirectView.as_view(pattern_name="free_guide", permanent=True)
    ),
    path(
        "lead-magnet/thanks/",
        RedirectView.as_view(pattern_name="free_guide_thanks", permanent=True),
    ),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
    path("start/", views.start, name="start"),
    # Standalone embedded forms (requested exact filenames)
    path("gom-onboarding.html", views.gom_onboarding, name="gom_onboarding"),
    path(
        "smartpro-agreement.html", views.smartpro_agreement, name="smartpro_agreement"
    ),
]
