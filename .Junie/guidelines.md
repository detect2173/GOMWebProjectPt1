## 9) Style & Quality Gates

- Black, isort, Ruff; adopt `.editorconfig`.
- Type hints on public functions; `mypy --strict` for domain/services.
- Pre-commit hooks are mandatory:  
  `black`, `isort`, `ruff`, `mypy`, `pytest -q`.
- Small, atomic commits with rationale.

---

## 9.1) VCS & Commit Policy (Junie)

### Branching

- All work happens directly on the `master` branch.
- No feature branches are required for this workflow.

### Default Behavior

- Junie **must automatically commit and push each change**.
- For every file modification:
    1. Stage only the relevant change.
    2. Commit immediately using the change summary as the commit message.
    3. Push directly to `origin/master`.

### Commit Format

type(scope): concise summary [junie]

- What changed
- Why it changed
- Notes: migrations/perf/security

**Examples:**

- `feat(api): add idempotency middleware [junie]`
- `fix(repo): update .gitignore to exclude pyc files [junie]`
- `chore(deploy): restart Passenger after staticfiles collect [junie]`

### Push Rules

- Push immediately after every commit (no batching).
- Never skip or delay commits — every edit should be traceable.
- Do not force-push unless explicitly instructed.

### Safety

- Exclude untracked/ignored files (`db.sqlite3`, `__pycache__`, logs, IDE configs, etc.) by honoring `.gitignore`.
- Do not commit secrets, `.env`, or compiled artifacts.
- For schema or migration changes, include clear notes in the commit message.
- If a change could break deploys (e.g., settings, dependencies, schema), Junie must **pause and confirm before pushing
  **.

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
- For mypy, prefer `--strict` in domain/services. Add a mypy config (e.g., `mypy.ini`) if needed to handle
  Django-specific typing.

### Agent Runtime Hints
- Skip full repository review unless I explicitly ask for it.
- Run at most one `git status -s -b` per task.
- Prefer the IDE Git API over interactive terminals.
- If a terminal command returns no output or closes, abort that step and report the command + exit code instead of retrying.
