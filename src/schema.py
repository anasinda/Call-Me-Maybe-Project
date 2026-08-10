"""Compatibility helpers for loading schemas and prompt data."""

from pathlib import Path

from .models import FunctionDefenition
from .parsing import (
    ParsingError,
    load_function_definitions,
    load_test_prompts,
)


class Schema:
    def __init__(
        self,
        file_path_definitions: str | Path,
        file_path_test_prompts: str | Path,
    ):
        self.file_path_definitions = Path(file_path_definitions)
        self.file_path_test_prompts = Path(file_path_test_prompts)
        self.llm_usable_functions: dict[str, FunctionDefenition] = {}

    def create_schema(
        self,
    ) -> tuple[dict[str, FunctionDefenition], list[dict[str, object]]]:
        try:
            self.llm_usable_functions = load_function_definitions(
                self.file_path_definitions,
            )
            test_prompts = load_test_prompts(self.file_path_test_prompts)
        except ParsingError as error:
            print(f"Couldn't open file: {error}")
            return {}, []

        return self.llm_usable_functions, test_prompts
