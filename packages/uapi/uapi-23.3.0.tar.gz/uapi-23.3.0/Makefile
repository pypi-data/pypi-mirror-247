.PHONY: test lint

test:
	pdm run pytest tests -x --ff --mypy-only-local-stub

lint:
	pdm run mypy src/ tests/ && pdm run ruff src/ tests/ && pdm run black --check -q src/ tests/
