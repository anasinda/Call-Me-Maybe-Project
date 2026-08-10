import json
from pathlib import Path
from typing import Any

from .models import FunctionDefenition


class Schema:
    def __init__(self, file_path_definitions: str | Path, file_path_test_prompts: str | Path):
        self.file_path_definitions = Path(file_path_definitions)
        self.file_path_test_prompts = Path(file_path_test_prompts)
        self.parsed_json_definitions: list[dict[str, Any]] = [{}]
        self.parsed_json_test_prompts: list[dict[str, Any]] = [{}]
        self.llm_usable_functions: dict[str, FunctionDefenition] = {}
        self.llm_given_prompts: dict[str, FunctionDefenition] = {}

    def create_schema(
        self,
    ) -> tuple[dict[str, FunctionDefenition], list[dict[str, Any]]]:
        try:
            with open(self.file_path_definitions, 'r') as file_func_def, open(self.file_path_test_prompts, "r") as file_prompt_test:
                self.parsed_json_definitions = json.load(file_func_def)
                self.parsed_json_test_prompts = json.load(file_prompt_test)

                # print("Loaded json functions defs", self.parsed_json_definitions)
                # print("Loaded json prompts tests", self.parsed_json_test_prompts)
                for data in self.parsed_json_definitions:
                    func_def_obj: FunctionDefenition = FunctionDefenition.model_validate(data)
                    self.llm_usable_functions[func_def_obj.name] = func_def_obj

                # for index, data in enumerate(self.parsed_json_test_prompts):
                #     prompt_test_obj: PromptGetter = PromptGetter.model_validate(data)
                #     self.llm_given_prompts[f"prompt-{index}"] = prompt_test_obj
        except FileNotFoundError as no_file_error:
            print(f"Couldn't open file: {no_file_error.filename}")

        return self.llm_usable_functions, self.parsed_json_test_prompts
