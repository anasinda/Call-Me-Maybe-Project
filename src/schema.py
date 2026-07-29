import json
from typing import Any
from models import FunctionDefenition, Parameter
from grammar import Grammar, State

with open("../data/input/functions_definition.json", 'r') as file:
    llm_usable_functions: dict[str, FunctionDefenition] = {}
    parsed_json: list[dict[str, Any]] = json.load(file)

    for data in parsed_json:
        func_obj: FunctionDefenition = FunctionDefenition.model_validate(data)
        llm_usable_functions[func_obj.name] = func_obj
