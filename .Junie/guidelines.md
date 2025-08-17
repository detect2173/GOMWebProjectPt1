# Project Guidelines for Junie

These rules are **mandatory** for any code you write or modify.  
If a rule conflicts with implicit Django “magic,” **prioritize these rules** and ask for clarification in **Ask Mode** before proceeding.

---

## 0) Modes & Scope Control
- Start tasks in **Ask Mode** to restate requirements, risks, and file plan. Switch to **Code Mode** only after confirming scope.
- If unsure about any requirement or if a change has side effects (schema, settings, dependency versions), **stop and ask**.
- Breaking changes to public APIs require an API version bump and a deprecation plan.

---

## 1) Dependency Management (No “Field” Injection)
**Principle:** Prefer **constructor injection** or explicit parameter passing over module-level singletons, service locators, or reaching into globals.

**DO**
- Pass dependencies via `__init__` or function parameters.
- Accept configuration through parameters or typed dataclasses.
- Wrap third-party clients in small adapter classes that are injected, with timeouts and retries configured.
- Inject configuration at process start; no runtime `settings` access in domain logic.

**DON’T**
- Don’t access `django.conf.settings` inside domain logic (OK in boundaries like config/adapters).
- Don’t import and use clients at module import time (no hidden singletons).
- Don’t mutate globals to share state.

**Python Example:**
```python
# ✅ Good: constructor injection
class EmailNotifier:
    def __init__(self, mailer):
        self.mailer = mailer

    def send_welcome(self, user):
        self.mailer.send(to=user.email, template="welcome.html")

# ❌ Bad: "field" injection / global access
from django.conf import settings
from myapp.mailers import global_mailer

class EmailNotifier:
    def send_welcome(self, user):
        global_mailer.send(to=user.email, template=settings.DEFAULT_TEMPLATE)
```

---

## 2) Layering & Architecture
- **Views/Controllers**: Only orchestrate. No business rules.
- **Domain/Service layer**: Business logic lives here. No HTTP, no ORM calls except via repositories.
- **Repositories**: Encapsulate ORM access. No business decisions.
  - *Example business decision (forbidden in repos)*: filtering records based on the current user’s subscription plan.
- **Adapters** (email, payments, external APIs): Small, injected, testable.

**File placement:**
```
myapp/
  domain/
    services/*.py
    models/*.py  # domain models (not Django ORM models)
  infra/
    repos/*.py   # ORM access
    adapters/*.py
  web/
    views/*.py
    serializers/*.py
```

**Import Boundaries (Enforced via import-linter):**
- `domain` → no imports from `infra` or `web`
- `infra` → may import domain interfaces only
- `web` → may import domain services and serializers; not `infra`

---

## 3) Django/DRF Conventions
- Use **DRF serializers** for I/O; never pass raw request data into domain services.
- Keep **querysets** lazy in views; use repositories for complex queries.
- Avoid `.values()`/`.values_list()` unless justified and documented.
- Pagination: Use `PageNumberPagination` with `PAGE_SIZE=50` (max 200). Return consistent envelopes:  
  `{"count", "next", "previous", "results"}`
- Idempotency for POST where applicable; use `X-Idempotency-Key` retained for 24h; replay returns same result.
- Use a custom exception handler to return:  
  `{"code": "...", "message": "...", "details": "...", "field_errors": {...}}`

---

## 4) Migrations & Models
- **Never** modify historical migrations; create a new migration.
- Model field changes must include data migrations if needed.
- Use explicit `db_index=True` on frequent filters/joins; explain in code comments.
- Risky schema changes (large rewrites, locking) must include a stepwise migration plan, downtime estimate, and rollback strategy.

---

## 5) Error Handling, Logging, and Observability
- Catch only expected exceptions; rethrow unknowns.
- Use JSON logs with keys: `ts, level, event, logger, request_id, user_id_hash, trace_id, span_id`.
- Never log PII; maintain an allowlist of safe fields. Mask or hash sensitive values.
- Wrap external calls; time them; add circuit-breaker or retries where appropriate.
- Tracing: instrument external calls and DB operations (OpenTelemetry or equivalent).

---

## 6) Security Rules (Hard Stops)
- **No** secrets in code or committed `.env` files.
- All secrets sourced from a secrets manager (AWS Secrets Manager, Azure Key Vault, Vault, etc.). Rotate at least every 90 days.
- Validate and sanitize all input; rely on DRF validation + explicit validators.
- CSRF stays **on** for state-changing views (unless API with proper token).
- Enforce permissions at the viewset and service entrypoints.
- SQL: ORM only; raw SQL requires prior approval and parameterization.
- Secret scanning runs in CI.

---

## 7) Testing Requirements
- For any new logic, include unit tests. For endpoints, add API tests.
- Use **pytest** + **pytest-django**.
- No network calls in unit tests; use fakes/mocks. Mark integration tests.
- Factories over fixtures; coverage must be ≥ 90% overall and 100% in domain/services. Enforced in CI.

**Example test:**
```python
def test_send_welcome_uses_mailer(fake_mailer, user):
    svc = EmailNotifier(mailer=fake_mailer)
    svc.send_welcome(user)
    fake_mailer.assert_called_once()
```

---

## 8) Performance, Async, and Caching
- Prefer `.select_related()` / `.prefetch_related()` for N+1 hotspots.
- Bulk operations where safe (`bulk_create`, `update`).
- Async views only if all deps are async-compatible; prohibit async calls from sync views unless safely wrapped (e.g., `run_in_executor`).
- Set default timeouts for external calls (`connect=3s`, `read=10s`).
- Define caching strategy: acceptable staleness, key patterns, invalidation rules.

---

## 9) Style & Quality Gates
- Black, isort, Ruff; adopt `.editorconfig`.
- Type hints on public functions; `mypy --strict` for domain/services.
- Pre-commit hooks are mandatory:  
  `black`, `isort`, `ruff`, `mypy`, `pytest -q`.
- Small, atomic commits with rationale.

**Commit rules:**
- Commit and push each change **individually**, using only that change’s summary as the commit message.
- Do not bundle unrelated changes in the same commit.

**Commit format:**
```
type(scope): concise summary

- What changed
- Why it changed
- Any migration/perf/security notes
```

---

## 10) What Junie Must Not Do (Without Explicit Approval)
- Change dependency versions or add packages.
- Auto-refactor unrelated files.
- Regenerate lockfiles or rewrite settings.
- Run destructive shell commands or apply migrations.
- Alter CI/CD, Dockerfiles, or deployment manifests.
- Force-push to protected branches or commit directly to `main`.

---

## 11) Task Checklist (Junie)
Before coding, produce in Ask Mode:
1. **Plan:** files to touch, function/class signatures, dependencies to inject.
2. **Risks:** migrations, settings, external calls.
3. **Tests:** list of tests you’ll add.
4. **Rollback & Observability Plan:** metrics/logs you’ll add, rollback steps.

Only after approval → implement exactly that plan.

---

## 12) Enforcement
- **Static checks:** Ruff, mypy strict, import-linter.
- **CI gates:** enforce test coverage thresholds; fail on secrets; block migrations without tests/plans.
- **Pre-commit:** required before merge; run locally and in CI.



---

## 13) Supported Versions & Tooling Matrix
- Python: 3.11 (min), 3.12 (target)
- Django: 4.2 LTS
- Django REST Framework: 3.14
- PostgreSQL: 14+
- Tooling: black 24.x, isort 5.13.x, ruff 0.5.x, mypy 1.10+, import-linter 2.x, pytest 8.x, pytest-django 4.x

These versions align local development, CI images, and config files. Deviations require approval in Ask Mode.

---

## 14) Configuration & Dependency Wiring
- Config source: 12‑factor via environment variables.
- Loader: infra/config adapter (e.g., django-environ or pydantic-settings) reads at process start and produces typed objects.
- Wiring: a bootstrap/providers module constructs adapters and injects them into services via constructors.
- Rule: No dynamic settings reads in domain logic; inject typed config objects.

Copy‑paste policy:
- “Config must be read at process start, transformed into typed objects, and injected into services/adapters. No runtime settings access in domain logic.”

---

## 15) API Auth, Permissions & CSRF
- Default DRF permission: IsAuthenticated; adjust per endpoint explicitly.
- Auth methods: Prefer stateless token/JWT for public APIs; session auth only for internal apps.
- CSRF: Keep enabled for session‑based state‑changing views; for token/JWT endpoints, require Authorization header and configure CSRF accordingly.
- Enforce permissions at both web viewsets and service entrypoints.

---

## 16) DRF Exception Handler (Standard Error Envelope)
Add this handler and set it via REST_FRAMEWORK["EXCEPTION_HANDLER"].

```python
# web/exceptions.py
from rest_framework.views import exception_handler
from rest_framework import exceptions


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    code = getattr(exc, "default_code", None) or "error"
    message = None
    field_errors = {}

    data = response.data
    if isinstance(exc, exceptions.ValidationError):
        message = "Invalid input."
        if isinstance(data, dict):
            field_errors = {k: v for k, v in data.items() if isinstance(v, list)}
    else:
        message = data.get("detail") if isinstance(data, dict) else str(exc) or "Error"

    response.data = {
        "code": str(code),
        "message": message,
        "details": None,
        "field_errors": field_errors,
    }
    return response
```

Settings wiring:
- `REST_FRAMEWORK["EXCEPTION_HANDLER"] = "myapp.web.exceptions.custom_exception_handler"`

---

## 17) Import‑Linter Config Example
Place as .importlinter.ini at the repo root:

```
[importlinter]
root_package = myapp

[contract:no_domain_to_infra_web]
name = Domain must not import infra or web
type = forbidden
source_modules = myapp.domain
forbidden_modules = myapp.infra myapp.web

[contract:web_not_import_infra]
name = Web must not import infra
type = forbidden
source_modules = myapp.web
forbidden_modules = myapp.infra
```

---

## 18) Caching Defaults
- Backend: Redis recommended (namespaced per environment, e.g., `dev:`, `stg:`, `prod:` prefix).
- Key patterns: `app:resource:{id}` and `app:query:{hash}`; include env prefix.
- TTL: default 300 seconds unless otherwise documented.
- Invalidation: write‑through on object updates; explicit cache bust on mutating events.
- Do not cache user‑specific responses without scoping keys to user identity and permissions.

---

## 19) Idempotency Implementation Details
- Storage: Redis with 24h TTL for `X-Idempotency-Key` records.
- Scope keys to (endpoint, authenticated user).
- Persist status code, response body hash, and created_at. On replay, return the same status/body.

---

## 20) Query Budgets & N+1 Enforcement
- Budgets: list endpoints ≤ 30 queries; detail endpoints ≤ 10, unless justified in code comments.
- Tests should assert query counts.

Example with Django’s query capture:
```python
from django.test.utils import CaptureQueriesContext
from django.db import connection

def test_list_query_budget(client):
    with CaptureQueriesContext(connection) as ctx:
        resp = client.get("/api/v1/widgets/")
        assert resp.status_code == 200
    assert len(ctx) <= 30
```

---

## 21) Observability Defaults
- Tracing: OpenTelemetry SDK + OTLP exporter to collector; instrument DB and external calls; include trace/span IDs in logs.
- Logging: JSON to stdout with keys already defined; levels policy: INFO default; DEBUG only in dev; WARN for 4xx; ERROR for 5xx.
- Metrics: HTTP request count, latency p50/p95/p99, error rate; external call timing and error tags.
- Policy: Every external call must record duration, status, and error outcome with trace correlation.

---

## 22) Async and ORM Boundary Clarification
- Django ORM is synchronous; do not call ORM in async views without `database_sync_to_async`.
- Prefer keeping views synchronous unless all dependencies are async‑ready end‑to‑end.

---

## 23) Migration Review & Operational Safety
- All migrations require peer review; risky operations require DBA review.
- Use `CREATE INDEX CONCURRENTLY` where applicable; schedule off‑peak; include rollback migration.
- For large rewrites/backfills, use stepwise migrations (backfill in batches, then swap columns); document expected lock times.

---

## 24) Testing Policy Enhancements
- Ban `sleep()` in tests; for time control use `freezegun` (or equivalent) and deterministic clocks.
- Prefer `factory_boy` with Faker; seed deterministically in CI.
- Mark integration tests explicitly; unit tests must not touch network or disk.
- When using `.values()`/`.values_list()`, include a code comment explaining why, ideally with measured performance benefit.

---

## 25) Delivery & Branching
- Strategy: trunk‑based with short‑lived feature branches.
- All changes via PR; ≥1 reviewer required.
- CI must pass: lint (ruff), type (mypy), tests, coverage thresholds, import‑linter, and secret scanning.
- No force‑push to protected branches and no direct commits to `main` (already stated).

---

## 26) Compliance, i18n, Accessibility (If Applicable)
- PII classification, retention/deletion policies, and audit logging for sensitive actions.
- i18n: use gettext for translatable strings; avoid hard‑coded user‑facing text; handle locale files.
- Accessibility: follow WCAG 2.1 AA for web UIs; run automated accessibility checks (e.g., axe) in CI.

---

## 27) Minor Wording Preferences
- Logging levels: “INFO default; DEBUG only in dev; WARN for 4xx; ERROR for 5xx; avoid TRACE in prod.”
- HTTP client timeouts: “Always set connect/read timeouts in adapters; prohibit infinite timeouts.”
