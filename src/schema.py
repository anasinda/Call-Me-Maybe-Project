import json
from models import FunctionDefenition, Parameter
from sys import argv


with open("../data/input/functions_definition.json", 'r') as file:
    llm_usable_functions: dict[str, FunctionDefenition] = {}
    parsed_json: list[dict[str, str]] = json.load(file)

    for data in parsed_json:
        func_obj: FunctionDefenition = FunctionDefenition.model_validate(data)
        llm_usable_functions[func_obj.name] = func_obj

    for key, value in llm_usable_functions.items():
        print("THis is key", key)
        print("THis is name in obj", value.description)

