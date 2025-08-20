import os

import django
from django.test import Client

# Ensure Django is set up for pytest without pytest-django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GOMWebProjectPt1.settings")
django.setup()


def test_core_pages_get_200():
    client = Client()
    for path in [
        "/",
        "/pricing/",
        "/book/",
        "/free-guide/",
        "/free-guide/thanks/",
        "/terms/",
        "/privacy/",
        "/start/",
        "/gom-onboarding.html",
        "/smartpro-agreement.html",
    ]:
        resp = client.get(path)
        assert resp.status_code == 200, f"{path} returned {resp.status_code}"


def test_legacy_redirects_permanent():
    client = Client()
    for path in ["/lead-magnet/", "/lead-magnet/thanks/"]:
        resp = client.get(path)
        assert resp.status_code in {301, 308}
