install:
	uv sync

run:
	uv run python -m src

debug:
	uv run python -m pdb -m src.main

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache .ruff_cache src/__pycache__ llm_sdk/llm_sdk/__pycache__

lint:
	uv run flake8 src
	uv run mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
