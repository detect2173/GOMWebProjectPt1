## 9) Style & Quality Gates
- Black, isort, Ruff; adopt `.editorconfig`.
- Type hints on public functions; `mypy --strict` for domain/services.
- Pre-commit hooks are mandatory:  
  `black`, `isort`, `ruff`, `mypy`, `pytest -q`.
- Small, atomic commits with rationale.

---

## 9.1) VCS & Commit Policy (Junie)

### Branching
- Primary branch: master.
- If working on another branch, commit and push to the **current branch** (HEAD) unless I explicitly ask to switch.

### Default Behavior (Automatic)
Junie must automatically commit and push every change **without waiting for approval**, using the change summary as the commit message.

For each edit:
1. Stage only relevant changes (respect `.gitignore`).
2. Build the commit message from the task/change summary using this format: `type(scope): concise summary [junie]`
   - If type(scope) isn’t specified by me, infer a sensible type: `feat|fix|chore|docs|test|refactor`.
3. Run:
   - `git add -A`
   - `git commit -m "<message>"`
   - `git push origin HEAD`

### Commit Message Examples
- `feat(api): add idempotency middleware [junie]`
- `fix(repo): tighten .gitignore [junie]`
- `chore(deploy): touch passenger restart [junie]`

### Push Rules
- Push **immediately** after each commit (no batching).
- Never force-push unless I explicitly say `force-push: yes`.
- If the push is rejected due to remote updates, run `git pull --rebase` and **retry once**; if it still fails, stop and report.

### Safety
- Never commit secrets or local artifacts: `.env*`, `db.sqlite3`, `__pycache__/`, `*.pyc`, `*.log`, `.idea/`, `.vscode/`, `dist/`, `build/`, `*.egg-info/`.
- Honor `.gitignore` at all times.
- If the change includes **migrations** or **requirements** updates, include a note at the end of the commit body:
  - `Notes: migrations` / `Notes: deps`
- If a commit would include any of the banned files above, exclude them and proceed; then report what was skipped.

### Rollback
- If the last commit needs to be undone on request:
  - `git revert HEAD` (preferred) → push.
- Only use history-editing commands (`reset`, `rebase`, `push --force`) if I explicitly ask.

### Action Allowlist
In **Settings → Tools → Junie → Action Allowlist**, add a **Terminal Rule** with this regex to allow the exact Git commands Junie needs:

`^git (status|branch|rev-parse|log|describe|add|commit|pull|push)(\b.*)?$`

(Or split into two rules for stricter control:)
- Read-only: `^git (status|branch|rev-parse|log|describe)(\b.*)?$`
- Write actions: `^git (add|commit|pull|push)(\b.*)?$`

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

### Agent Runtime Hints
- Prefer the IDE’s Git API to get branch name and status. Avoid opening the terminal for simple queries.
- If terminal is required, you may run read-only git commands (status, branch, rev-parse, log, describe).
