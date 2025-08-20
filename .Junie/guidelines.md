## 9) Style & Quality Gates
- Black, isort, Ruff; adopt `.editorconfig`.
- Type hints on public functions; `mypy --strict` for domain/services.
- Pre-commit hooks are mandatory:  
  `black`, `isort`, `ruff`, `mypy`, `pytest -q`.
- Small, atomic commits with rationale.

---

## 9.1) VCS & Commit Policy (Junie)

### Branching
- All work must happen on feature branches:
  - `feat/<ticket>`, `fix/<bug>`, `chore/<topic>`.
- Never commit directly to `main`.

### Default Behavior
- Junie **must not** commit or push automatically.
- Junie should:
  1. Stage the proposed changes.
  2. Show the diff and a suggested commit message.
  3. Wait for explicit approval before committing.
- After approval:
  - Commit only the staged change.
  - Push the branch (`git push -u origin HEAD`).

### Commit Format
type(scope): concise summary [junie]

= What changed

- Why it changed

- Notes: migrations/perf/security


Examples:
- `feat(api): add idempotency middleware [junie]`
- `fix(repo): tighten .gitignore [junie]`

### Push Rules
- Push only after tests and linters pass locally.
- Do not force-push unless explicitly instructed.
- Open a PR for merge into `main`.

### Safety
- IDE settings: disable “Commit and Push” as default, and disable “Auto-update if Push Rejected.”
- Server settings: protect `main` branch (require PR and status checks).

---

## 9.2) Pre-commit Guardrails
Use `pre-commit` to block invalid commits. Required hooks: black, isort, ruff, mypy, pytest -q.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: []
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest -q
        language: system
        pass_filenames: false
        stages: [commit]
```

Install:

- pip install -U pre-commit black isort ruff mypy pytest
- pre-commit install

Notes:
- Adopt a project-wide `.editorconfig` to ensure consistent line endings, indentation, and charset.
- For mypy, prefer `--strict` in domain/services. Add a mypy config (e.g., `mypy.ini`) if needed to handle Django-specific typing.