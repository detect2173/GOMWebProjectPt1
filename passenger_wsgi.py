import os
import sys

# Adjust path if necessary; assumes this file sits beside manage.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GOMWebProjectPt1.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402
application = get_wsgi_application()
