.PHONY: help test clean fix-linting

help:
	@echo "Available commands:"
	@echo "  make test            - Run all tests using uv"
	@echo "  make fix-linting     - Fix linting issues using scripts/fix-linting-command.sh"
	@echo "  make clean           - Remove build artifacts and cache directories"

test:
	uv run pytest -s $(filter-out $@,$(MAKECMDGOALS))

fix-linting:
	./scripts/fix-linting-command.sh

check-types:
	./scripts/check-types-command.sh

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# This target catches all non-defined targets to allow passing arguments
%:
	@: