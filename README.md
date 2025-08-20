Great Owl Marketing — Web Project

This Django project provides a simple marketing site for Great Owl Marketing to showcase chatbot services, capture leads via GetResponse, and book calls via Calendly.

Key Pages
- Home: overview, CTA to Free Guide and booking
- Pricing: transparent pricing for Build & Handoff vs Managed Subscription
- Free Guide: form to collect email/name and consent
- Book: embedded Calendly scheduler

Configuration
Set these environment variables before running in production:
- DJANGO_DEBUG (True/False)
- DJANGO_ALLOWED_HOSTS (comma-separated; e.g., example.com,www.example.com)
- DJANGO_CSRF_TRUSTED_ORIGINS (comma-separated full origins; e.g., https://example.com,https://www.example.com)
- GETRESPONSE_API_KEY
- GETRESPONSE_LIST_ID
- CALENDLY_URL (e.g., https://calendly.com/your-link)
- ONBOARDING_EMBED_URL (URL of your post-payment intake form to embed at /start/)
- LOGO_URL (optional; defaults to /static/img/logo.png). Place your logo at static/img/logo.png or set LOGO_URL to another static path or full URL.

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


Do I need API keys?
Yes, for full functionality in production you should configure these environment variables:

Required for live lead delivery and scheduling
- GETRESPONSE_API_KEY: Your GetResponse API key (used to create contacts)
- GETRESPONSE_LIST_ID: The campaign/list ID where contacts should be added
- CALENDLY_URL: Your public Calendly scheduling link (used to embed the widget)

What happens if I don’t set them?
- If GETRESPONSE_API_KEY or GETRESPONSE_LIST_ID are missing, the app will still accept the form and store the lead locally in the database, but it will skip the external GetResponse API call. A log warning is emitted.
- If CALENDLY_URL is not set, a placeholder Calendly URL will be used and the widget may not display your actual calendar.

Recommended/optional production settings
- DJANGO_DEBUG: False in production
- DJANGO_ALLOWED_HOSTS: Comma-separated hostnames (example.com,www.example.com)
- DJANGO_CSRF_TRUSTED_ORIGINS: Comma-separated full origins (https://example.com,https://www.example.com)

How to set variables
- Local (Windows PowerShell):
  $env:GETRESPONSE_API_KEY = "your_key"
  $env:GETRESPONSE_LIST_ID = "your_list_id"
  $env:CALENDLY_URL = "https://calendly.com/your-link"
  $env:DJANGO_DEBUG = "True"  # or "False"
  # Optional, only if you are not placing the file at static/img/logo.png
  $env:LOGO_URL = "/static/img/logo.png"

- Namecheap cPanel (Setup Python App):
  1) Open your application
  2) Add Environment variables for the keys above
  3) Click "Save" then "Restart" the application

Where these are used in code
- sitecore/views.py: the Free Guide POST will try to subscribe via GetResponse using GETRESPONSE_API_KEY and GETRESPONSE_LIST_ID; if unset, it logs a warning and continues gracefully.
- GOMWebProjectPt1/settings.py: reads CALENDLY_URL and passes it to templates for the embedded widget.

Local setup via .env (recommended)
- Copy .env.example to .env and fill in your values. Do NOT commit .env (it’s in .gitignore).
- Example:
  GETRESPONSE_API_KEY=your_real_key
  GETRESPONSE_LIST_ID=your_list_id
  CALENDLY_URL=https://calendly.com/phineasjholdings-info/30min

Namecheap cPanel setup
- In Setup Python App > Environment variables, add your real values for GETRESPONSE_API_KEY and GETRESPONSE_LIST_ID.
- Keep your keys private; never commit them to the repository.
