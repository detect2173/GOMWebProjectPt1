# Default goal: show help when you just type `make`
.DEFAULT_GOAL := help

# Treat these names as phony targets (always run, even if files exist)
.PHONY: help install migrate makemigrations run shell lint format test coverage \
        clean clean-preview clean-ignored clean-pyc clean-all

# ------------------
# Help (pretty)
# ------------------
help: ## Show all make targets with descriptions
	@echo ""
	@echo "Available commands:"
	@echo "-------------------"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Safety tips:"
	@echo "  - \033[36mmake clean\033[0m          : Safe preview (shows what would be deleted)"
	@echo "  - \033[36mmake clean-ignored\033[0m : Deletes ignored files (safe-ish)"
	@echo "  - \033[36mmake clean-all CONFIRM=YES\033[0m : Deletes ALL untracked+ignored files (nuclear)"
	@echo ""

# ------------------
# Dev environment
# ------------------
install: ## Install dependencies
	pip install -r requirements.txt

migrate: ## Run Django migrations
	python manage.py migrate

makemigrations: ## Create new migrations
	python manage.py makemigrations

run: ## Run Django development server
	python manage.py runserver 0.0.0.0:8000

shell: ## Open Django shell
	python manage.py shell

# ------------------
# Quality / Testing
# ------------------
lint: ## Run Ruff linter
	ruff check .

format: ## Auto-format with Black & isort
	black .
	isort .

test: ## Run pytest
	pytest -q --disable-warnings

coverage: ## Run tests with coverage
	pytest --cov=. --cov-report=term-missing

# ------------------
# Cleanup (graduated safety)
# ------------------
clean: clean-preview ## (Safe) Alias: show what would be deleted

clean-preview: ## Show ignored files that would be deleted
	git clean -ndX

clean-ignored: ## Delete ignored files only (from .gitignore)
	git clean -fdX

clean-pyc: ## Remove Python bytecode and __pycache__ folders
	# Works on Git Bash / macOS / Linux
	find . -name '*.pyc' -delete || true
	find . -name '*.pyo' -delete || true
	find . -name '__pycache__' -type d -exec rm -rf {} + || true

# Nuclear option: requires explicit CONFIRM=YES
clean-all: ## Delete ALL untracked + ignored files (DANGER: keeps only what Git tracks)
	@if [ "$(CONFIRM)" != "YES" ]; then \
		echo "Refusing to run. This will delete ALL untracked + ignored files."; \
		echo "If you really want this, re-run as:"; \
		echo "  make clean-all CONFIRM=YES"; \
		exit 1; \
	fi
	git clean -fdx
