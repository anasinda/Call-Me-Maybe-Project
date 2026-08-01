import json
from typing import Any
from src.models import FunctionDefenition, Parameter
from src.grammar import Grammar, State

class Schema():
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.parsed_json: list[dict[str, Any]] = [{}]

    def create_schema(self):
        with open(self.file_path, 'r') as file:
            llm_usable_functions: dict[str, FunctionDefenition] = {}
            parsed_json: list[dict[str, Any]] = json.load(file)

            for data in parsed_json:
                func_obj: FunctionDefenition = FunctionDefenition.model_validate(data)
                llm_usable_functions[func_obj.name] = func_obj

            return llm_usable_functions
