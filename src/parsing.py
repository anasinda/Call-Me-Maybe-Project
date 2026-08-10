"""Command-line and JSON parsing helpers for the project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from .models import FunctionDefenition


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FUNCTIONS_DEFINITION = PROJECT_ROOT / "data" / "input" / "functions_definition.json"
DEFAULT_TEST_INPUT = PROJECT_ROOT / "data" / "input" / "function_calling_tests.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "output" / "function_calling_results.json"


class ParsingError(RuntimeError):
    """Raised when an input file or CLI argument cannot be parsed."""


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser used by ``python -m src``."""

    parser = argparse.ArgumentParser(prog="python -m src")
    parser.add_argument("--functions_definition", type=Path, default=None)
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the project."""

    return build_parser().parse_args(argv)


def resolve_path(value: Path | None, default_path: Path) -> Path:
    """Return a user-supplied path or the project default."""

    if value is None:
        return default_path
    return value.expanduser()


def load_json_list(path: Path) -> list[dict[str, Any]]:
    """Load and validate a JSON array from ``path``."""

    try:
        with path.open("r", encoding="utf-8") as file_handle:
            payload = json.load(file_handle)
    except FileNotFoundError as error:
        raise ParsingError(f"Missing input file: {path}") from error
    except json.JSONDecodeError as error:
        raise ParsingError(f"Invalid JSON in {path}: {error.msg}") from error

    if not isinstance(payload, list):
        raise ParsingError(f"Expected a JSON array in {path}")

    parsed_items: list[dict[str, Any]] = []
    for item in payload:
        if not isinstance(item, dict):
            raise ParsingError(f"Expected every item in {path} to be a JSON object")
        parsed_items.append(item)

    return parsed_items


def load_function_definitions(path: Path) -> dict[str, FunctionDefenition]:
    """Load function definitions into a lookup dictionary."""

    parsed_items = load_json_list(path)
    functions: dict[str, FunctionDefenition] = {}
    for item in parsed_items:
        function_def = FunctionDefenition.model_validate(item)
        functions[function_def.name] = function_def
    return functions


def load_test_prompts(path: Path) -> list[dict[str, Any]]:
    """Load prompt records used to drive the function-calling pipeline."""

    return load_json_list(path)


def ensure_output_parent(path: Path) -> None:
    """Create the output directory if it does not already exist."""

    path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: Any) -> None:
    """Write JSON payload to ``path`` using a stable, readable format."""

    ensure_output_parent(path)
    with path.open("w", encoding="utf-8") as file_handle:
        json.dump(payload, file_handle, indent=2, ensure_ascii=False)
        file_handle.write("\n")
