"""Runs the function-calling pipeline: pick a function for each test prompt,
then extract its arguments, using constrained decoding at every step."""

import time

from schema import Schema
from function_constraint_decoder import Generator
from base_prompt import CreatePrompt
from models import FunctionDefenition
from tokenizer import Tokenizer
from decoder import build_number_token_mask, generate_parameter

DEFINITIONS_PATH = "../data/input/functions_definition.json"
TESTS_PATH = "../data/input/function_calling_tests.json"


def get_request_text(test_case: dict) -> str:
    """Pull the natural-language request out of one test-case dict."""
    if "request" in test_case:
        return str(test_case["request"])
    return str(next(iter(test_case.values())))


def function_signature(name: str, function_obj: FunctionDefenition) -> str:
    """e.g. 'Function: fn_add_numbers(a: number, b: number)\\n'"""
    params = ", ".join(f"{k}: {v.type}" for k, v in function_obj.parameters.items())
    return f"Function: {name}({params})\n"


def select_function(generator: Generator, function_prompt: str, request_text: str) -> str:
    """Ask the model which function (or 'null') fits this request."""
    return generator.start_model(function_prompt + request_text)


def extract_parameters(
    tokenizer: Tokenizer,
    parameter_prompt: str,
    request_text: str,
    function_name: str,
    function_obj: FunctionDefenition,
    number_mask: list[int],
) -> dict[str, str]:
    """Generate every parameter for the chosen function, one at a time."""
    header = (
        f"{function_signature(function_name, function_obj)}"
        f"Request: {request_text}\n"
        f"Answer: {{ "
    )
    prompt_ids = tokenizer.encode(parameter_prompt + header)

    params = list(function_obj.parameters.items())
    result: dict[str, str] = {}

    for i, (key, value) in enumerate(params):
        prompt_ids.extend(tokenizer.encode(f'"{key}":'))  # no trailing space

        generated = generate_parameter(tokenizer, prompt_ids, value.type, number_mask)
        result[key] = generated.strip()

        is_last = i == len(params) - 1
        prompt_ids.extend(tokenizer.encode(" }" if is_last else ", "))

    return result


def process_request(
    test_case: dict,
    tokenizer: Tokenizer,
    generator: Generator,
    function_prompt: str,
    parameter_prompt: str,
    usable_functions: dict[str, FunctionDefenition],
    number_mask: list[int],
) -> dict:
    """Run the full pipeline (select -> extract) for one test prompt."""
    request_text = get_request_text(test_case)
    function_name = select_function(generator, function_prompt, request_text)
    print(f"Selected function: {function_name}")

    if function_name not in usable_functions:
        print(f"  -> unknown function '{function_name}', skipping: {request_text}")
        return {"function": None, "parameters": {}}

    function_obj = usable_functions[function_name]
    if not function_obj.parameters:
        return {"function": function_name, "parameters": {}}

    parameters = extract_parameters(
        tokenizer, parameter_prompt, request_text, function_name, function_obj, number_mask
    )
    print(f"  -> parameters: {parameters}")
    return {"function": function_name, "parameters": parameters}


def main() -> dict[str, dict]:
    start_time = time.time()

    schema = Schema(DEFINITIONS_PATH, TESTS_PATH)
    usable_functions, test_cases = schema.create_schema()

    if not test_cases:
        return {}

    tokenizer = Tokenizer()
    generator = Generator(tokenizer, usable_functions, test_cases)
    prompt_creator = CreatePrompt(usable_functions)

    function_prompt = prompt_creator.create_main_prompt()
    parameter_prompt = prompt_creator.create_parameters_prompt()
    number_mask = build_number_token_mask(tokenizer)

    results: dict[str, dict] = {}
    for test_case in test_cases:
        request_text = get_request_text(test_case)
        results[request_text] = process_request(
            test_case, tokenizer, generator, function_prompt, parameter_prompt, usable_functions, number_mask
        )

    elapsed_min = (time.time() - start_time) / 60
    print(f"\n\nTotal time: {elapsed_min:.2f} min")
    return results


if __name__ == "__main__":
    main()
