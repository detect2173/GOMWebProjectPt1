Namecheap (cPanel) Deployment Guide — Great Owl Marketing

This project is a Django app ready for shared hosting on Namecheap using the cPanel “Setup Python App” feature (Passenger).

Prerequisites
- A Namecheap Shared Hosting plan with cPanel access
- A domain or subdomain you can point to the app
- Your GetResponse API key + list ID, and your Calendly scheduling URL

What we’ll set up
- A Python application in cPanel (Passenger WSGI)
- Virtual environment with project dependencies
- Environment variables for production
- Database migrations and static files

Repository files that help deployment
- requirements.txt — Python dependencies (Django + WhiteNoise)
- passenger_wsgi.py — WSGI entry point used by Passenger
- GOMWebProjectPt1/settings.py — production-friendly settings via environment variables

1) Create the Python App in cPanel
1. Log in to cPanel.
2. Open “Setup Python App”.
3. Click “Create Application”.
   - Python version: choose the latest available (3.11+ preferred).
   - Application root: e.g., apps/great-owl (this is the folder where the app will live).
   - Application URL: choose your domain or subdomain path.
   - Application startup file: passenger_wsgi.py
   - Application entry point: application
   - Click “Create”.

This creates a virtual environment and a basic app structure under your chosen application root.

2) Upload the project files
You have two options:
- Git deploy: push this repository to a remote (e.g., GitHub) and pull it into your application root via cPanel’s Git Version Control, or
- File Manager/FTP: upload the entire project into the Application root you set in step 1.

Ensure that at the application root you have manage.py and passenger_wsgi.py (as in this repo). Your Django project folder GOMWebProjectPt1 and the sitecore app and templates should sit alongside manage.py.

3) Install dependencies
1. In cPanel > Setup Python App, click your app, then click “Enter to the virtual environment” instructions; you can use cPanel Terminal or SSH.
2. Run:
   pip install -r requirements.txt

4) Configure environment variables
In cPanel > Setup Python App > your app, add the following Environment variables:
- DJANGO_DEBUG = False
- DJANGO_ALLOWED_HOSTS = yourdomain.com,www.yourdomain.com
- DJANGO_CSRF_TRUSTED_ORIGINS = https://yourdomain.com,https://www.yourdomain.com
- GETRESPONSE_API_KEY = your_real_key
- GETRESPONSE_LIST_ID = your_list_id
- CALENDLY_URL = https://calendly.com/your-scheduling-link

Tip: Keep your API keys private. Do not commit them to git. This project supports a .env file locally (via python-dotenv); on the server use cPanel Environment variables.

5) Collect static files and run migrations
From the app’s virtual environment (via Terminal/SSH):
- python manage.py migrate
- python manage.py collectstatic --noinput

Notes:
- STATIC_ROOT is configured to a server path and WhiteNoise is enabled to serve them efficiently via the app itself. No extra web server config is required.
- You can control the static path with either STATIC_ROOT (preferred) or STATIC_MODE (alias). For media uploads, use MEDIA_ROOT (preferred) or MEDIA_MODE (alias).
- If you prefer serving static via a separate domain or folder, you can adjust STATIC_URL and cPanel mappings.

6) Restart the app
In cPanel > Setup Python App, click “Restart” for your application. Visit your domain/subdomain to verify the site is up.

7) Admin (optional)
If you want to use Django admin:
- Create a superuser: python manage.py createsuperuser
- Access at /admin/

Database choice
- This project uses SQLite by default. For small marketing sites and forms, it’s fine. If you need MySQL (MariaDB) on Namecheap, create a DB in cPanel, then update DATABASES in settings.py accordingly via environment variables or a local settings override.

Troubleshooting
- 500 error after deploy: check the app error log in cPanel, verify environment variables and that passenger_wsgi.py is in the application root with entry point named application.
- Static files missing: ensure you ran collectstatic and then restarted the app.
- GetResponse not working: verify GETRESPONSE_API_KEY and GETRESPONSE_LIST_ID; the app will still save leads locally but logs a warning if not configured.

Security checklist
- Set DJANGO_DEBUG=False in production.
- Set DJANGO_ALLOWED_HOSTS and DJANGO_CSRF_TRUSTED_ORIGINS properly.
- Rotate SECRET_KEY before going live (move to an environment variable for production if possible).

That’s it! After these steps, your Django app should run on Namecheap’s shared hosting under cPanel with Passenger.


Staging workflow (separate branch and app)

Goal: Keep master (production) stable while you develop on a separate branch deployed to its own cPanel Python App.

A) Create the staging branch
1. git checkout master && git pull
2. git checkout -b stage/next
3. git push -u origin HEAD

B) Prepare .cpanel.yml for staging
- Option 1 (recommended): Keep different .cpanel.yml per branch.
  On stage/next only, set these paths (example):
  APPDIR=/home/greagfup/apps/great-owl-stage
  VENV=/home/greagfup/virtualenv/apps/great-owl-stage/3.12
- Keep master’s .cpanel.yml pointing at the production app paths:
  APPDIR=/home/greagfup/apps/great-owl
  VENV=/home/greagfup/virtualenv/apps/great-owl/3.12

C) Create a new cPanel Git working copy for staging
1. cPanel → Git Version Control → Create
   - Clone URL: your GitHub repo URL
   - Repository Path: /home/greagfup/apps/great-owl-stage
   - Branch: stage/next
   - Create

D) Create the staging Python App
1. cPanel → Setup Python App → Create Application
   - Python version: 3.12 (same as production)
   - Application root: /home/greagfup/apps/great-owl-stage
   - Startup file: passenger_wsgi.py
   - Entry point: application
   - (Optional) Application URL: staging.greatowlmarketing.com (create a subdomain in cPanel → Domains first)
   - Create
   - Copy the exact virtualenv path shown at the top (e.g., /home/greagfup/virtualenv/apps/great-owl-stage/3.12) and ensure .cpanel.yml on stage/next uses this path.

E) Configure staging environment variables
- DJANGO_DEBUG=False
- DJANGO_ALLOWED_HOSTS=staging.greatowlmarketing.com
- DJANGO_CSRF_TRUSTED_ORIGINS=https://staging.greatowlmarketing.com
- DJANGO_SECRET_KEY=generate-a-unique-secret
- CALENDLY_URL=your real link
- GETRESPONSE_API_KEY=… (optional for staging)
- GETRESPONSE_LIST_ID=… (optional for staging)
- LOGO_URL=/static/img/logo.png
- STATIC_VERSION=YYYYMMDD-HHMM (set a fresh value to bust caches)

F) Deploy staging via cPanel Git
- cPanel → Git Version Control → repository at apps/great-owl-stage → Deploy
- This runs .cpanel.yml for stage/next with the staging APPDIR/VENV paths:
  1) $VENV/bin/pip install -r $APPDIR/requirements.txt
  2) cd $APPDIR && $VENV/bin/python manage.py migrate --noinput
  3) cd $APPDIR && $VENV/bin/python manage.py collectstatic --noinput
  4) touch $APPDIR/passenger_wsgi.py (reload)

G) Verify staging
- Open https://staging.greatowlmarketing.com/static/css/site.css → HTTP 200, Content-Type: text/css
- Visit staging home page. Hard refresh (Ctrl+F5). The templates append ?v={{ STATIC_VERSION }} to the stylesheet to avoid stale caches.

H) Day-to-day
- Commit to stage/next and deploy the staging repo to test changes.
- When ready, merge stage/next → master, then cPanel Git → Deploy production.

Notes on virtualenv alignment
- Your cPanel Python App banner shows the exact venv path. Ensure the .cpanel.yml VENV matches it per environment (prod vs staging). If you change Python versions in the app, update .cpanel.yml accordingly.

Troubleshooting for staging
- If Deploy fails: open the deploy log in cPanel Git and copy the error. Common issues: wrong VENV path, missing migrate/collectstatic, missing env vars.
- If CSS doesn’t load: ensure STATIC_URL is "/static/", run collectstatic, restart; verify /static/css/site.css returns 200.


Practical values for greatowlmarketing.com
- DJANGO_ALLOWED_HOSTS = greatowlmarketing.com,www.greatowlmarketing.com
- DJANGO_CSRF_TRUSTED_ORIGINS = https://greatowlmarketing.com,https://www.greatowlmarketing.com
- STATIC_ROOT = /home/greagfup/static-collect/great-owl   (or set STATIC_MODE to the same path)
- MEDIA_ROOT  = /home/greagfup/media/great-owl           (or set MEDIA_MODE to the same path)

Note: Keep localhost and 127.0.0.1 in your local .env only; on the server, set only real domains.
