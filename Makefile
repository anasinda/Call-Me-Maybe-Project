PYTHON = python3

install:
	pip install uv

run:
	uv pip install -e ./llm_sdk
	uv sync

venv:
	$(PYTHON) -m venv .venv
