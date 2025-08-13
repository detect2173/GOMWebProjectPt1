Great Owl Marketing — Web Project

This Django project provides a simple marketing site for Great Owl Marketing to showcase chatbot services, capture leads via GetResponse, and book calls via Calendly.

Key Pages
- Home: overview, CTA to lead magnet and booking
- Pricing: transparent pricing for Build & Handoff vs Managed Subscription
- Lead Magnet: form to collect email/name and consent
- Book: embedded Calendly scheduler

Configuration
Set these environment variables before running in production:
- DJANGO_DEBUG (True/False)
- DJANGO_ALLOWED_HOSTS (comma-separated; e.g., example.com,www.example.com)
- DJANGO_CSRF_TRUSTED_ORIGINS (comma-separated full origins; e.g., https://example.com,https://www.example.com)
- GETRESPONSE_API_KEY
- GETRESPONSE_LIST_ID
- CALENDLY_URL (e.g., https://calendly.com/your-link)

Running locally
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver

Deployment
- See DEPLOYMENT.md for a step-by-step Namecheap (cPanel) guide using Passenger (Setup Python App).

Notes
- GetResponse integration is implemented with a minimal HTTP call in sitecore/views.py. If no API key/list is set, it will skip the external call gracefully while storing the lead locally.
- Static files are served via WhiteNoise in production; run collectstatic.
- Replace pricing copy in templates/sitecore/pricing.html as needed.
