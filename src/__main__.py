"""Command-line entry point for the constrained decoding pipeline."""

import time
from typing import Any

from .base_prompt import CreatePrompt
from .decoder import build_number_token_mask, generate_parameter
from .function_constraint_decoder import Generator
from .models import FunctionDefenition
from .parsing import (
    DEFAULT_FUNCTIONS_DEFINITION,
    DEFAULT_OUTPUT,
    DEFAULT_TEST_INPUT,
    ParsingError,
    load_function_definitions,
    load_test_prompts,
    parse_arguments,
    resolve_path,
    write_json,
)
from .tokenizer import Tokenizer


def get_request_text(test_case: dict) -> str:
    """Return the prompt text for a single test case."""
    if "prompt" in test_case:
        return str(test_case["prompt"])
    if "request" in test_case:
        return str(test_case["request"])
    return str(next(iter(test_case.values())))


def function_signature(
    name: str,
    function_obj: FunctionDefenition,
) -> str:
    """Build a simple function signature string for the prompt."""
    params = ", ".join(
        f"{k}: {v.type}" for k, v in function_obj.parameters.items()
    )
    return f"Function: {name}({params})\n"


def select_function(
    generator: Generator,
    function_prompt: str,
    request_text: str,
) -> str:
    """Ask the model which function fits the request."""
    return generator.start_model(function_prompt + request_text)


def extract_parameters(
    tokenizer: Tokenizer,
    parameter_prompt: str,
    request_text: str,
    function_name: str,
    function_obj: FunctionDefenition,
    number_mask: list[int],
) -> dict[str, Any]:
    """Generate parameter values for one chosen function."""
    header = (
        f"{function_signature(function_name, function_obj)}"
        f"Request: {request_text}\n"
        f"Answer: {{ "
    )
    prompt_ids = tokenizer.encode(parameter_prompt + header)

    params = list(function_obj.parameters.items())
    result: dict[str, Any] = {}

    for i, (key, value) in enumerate(params):
        prompt_ids.extend(tokenizer.encode(f'"{key}":'))

        generated = generate_parameter(
            tokenizer,
            prompt_ids,
            value.type,
            number_mask,
        )
        result[key] = coerce_generated_value(generated, value.type)

        is_last = i == len(params) - 1
        prompt_ids.extend(tokenizer.encode(" }" if is_last else ", "))

    return result


def coerce_generated_value(value: str, value_type: str) -> Any:
    """Convert a generated string into the expected JSON value."""
    cleaned_value = value.strip().strip('"')
    if value_type == "number":
        if cleaned_value == "":
            raise ValueError("Generated an empty numeric value")
        if any(char in cleaned_value for char in ".eE"):
            return float(cleaned_value)
        return float(cleaned_value)
    if value_type == "boolean":
        lowered_value = cleaned_value.lower()
        if lowered_value not in {"true", "false"}:
            raise ValueError(f"Invalid boolean value: {value}")
        return lowered_value == "true"
    return cleaned_value


def process_request(
    test_case: dict,
    tokenizer: Tokenizer,
    generator: Generator,
    function_prompt: str,
    parameter_prompt: str,
    usable_functions: dict[str, FunctionDefenition],
    number_mask: list[int],
) -> dict:
    """Run the full select-and-extract flow for one prompt."""
    request_text = get_request_text(test_case)
    function_name = select_function(generator, function_prompt, request_text)

    if function_name not in usable_functions:
        return {"prompt": request_text, "fn_name": "fn_no_match", "args": {}}

    function_obj = usable_functions[function_name]
    if not function_obj.parameters:
        return {"prompt": request_text, "fn_name": function_name, "args": {}}

    parameters = extract_parameters(
        tokenizer,
        parameter_prompt,
        request_text,
        function_name,
        function_obj,
        number_mask,
    )

    return {
        "prompt": request_text,
        "name": function_name,
        "parameters": parameters,
    }


def main(argv: list[str] | None = None) -> list[dict[str, Any]]:
    """Run the full prompt-processing workflow."""
    start_time = time.time()

    try:
        args = parse_arguments(argv)
        definitions_path = resolve_path(
            args.functions_definition,
            DEFAULT_FUNCTIONS_DEFINITION,
        )
        tests_path = resolve_path(args.input, DEFAULT_TEST_INPUT)
        output_path = resolve_path(args.output, DEFAULT_OUTPUT)

        try:
            usable_functions = load_function_definitions(definitions_path)
            test_cases = load_test_prompts(tests_path)
        except ParsingError as error:
            print(f"Error: {error}")
            return []

        if not test_cases:
            print("No test prompts were found.")
            return []

        tokenizer = Tokenizer()
        generator = Generator(tokenizer, usable_functions, [])
        prompt_creator = CreatePrompt(usable_functions)

        function_prompt = prompt_creator.create_main_prompt()
        parameter_prompt = prompt_creator.create_parameters_prompt()
        number_mask = build_number_token_mask(tokenizer)

        results: list[dict[str, Any]] = []
        total_prompts = len(test_cases)
        for index, test_case in enumerate(test_cases, start=1):
            result = process_request(
                test_case,
                tokenizer,
                generator,
                function_prompt,
                parameter_prompt,
                usable_functions,
                number_mask,
            )
            results.append(result)
            print(f"Finished processing prompt {index} of {total_prompts} :)")

        elapsed_min = (time.time() - start_time) / 60
        print(f"\n\nTotal time: {elapsed_min:.2f} min")
        write_json(output_path, results)
        return results
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting gracefully.")
        return []


if __name__ == "__main__":
    main()
