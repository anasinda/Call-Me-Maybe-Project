from schema import Schema
from function_constraint_decoder import Generator
from base_prompt import CreatePrompt
from models import FunctionDefenition
from tokenizer import Tokenizer
import numpy as np

MAX_STEPS = 64  # safety cap so a stuck generation can't loop forever


def build_request_text(dic: dict) -> str:
    """Pull the raw user request string out of a test-case dict.

    Prefer an explicit 'request' key; fall back to the first value.
    (str(dic.values()) previously leaked 'dict_values([...])' into prompts.)
    """
    if "request" in dic:
        return str(dic["request"])
    return str(next(iter(dic.values())))


def format_function_signature(name: str, function_obj: FunctionDefenition) -> str:
    params_str = ", ".join(f"{k}: {v.type}" for k, v in function_obj.parameters.items())
    return f"Function: {name}({params_str})\n"


def generate_number_param(tokenizer: Tokenizer, encoded_prompt: list[int]) -> tuple[str, list[int]]:
    """Greedy-decode a numeric value, masking logits to digit-only characters."""
    allowed_chars = "0123456789-.,}"
    allowed_tokens = set()
    for ch in allowed_chars:
        allowed_tokens.update(tokenizer.encode(ch))
    allowed_tokens = list(allowed_tokens)

    result = ""
    for _ in range(MAX_STEPS):
        logits = tokenizer.get_logits(encoded_prompt)
        mask = np.full(len(logits), -np.inf)
        mask[allowed_tokens] = 0
        best_token = int(np.argmax(logits + mask))
        decoded_token = tokenizer.decode([best_token])

        if decoded_token in (",", "}"):
            break

        encoded_prompt.append(best_token)  # was [best_token] -> caused the TypeError
        result += decoded_token
    else:
        print("Warning: number generation hit MAX_STEPS without stopping")

    return result, encoded_prompt


def generate_string_param(tokenizer: Tokenizer, encoded_prompt: list[int]) -> tuple[str, list[int]]:
    """Greedy-decode a string value, stopping at the first structural ',' or '}'."""
    result = ""
    for _ in range(MAX_STEPS):
        logits = tokenizer.get_logits(encoded_prompt)
        best_token = int(np.argmax(logits))
        decoded_token = tokenizer.decode([best_token])

        encoded_prompt.append(best_token)
        result += decoded_token

        if "," in result:
            result = result.split(",")[0]
            break
        if "}" in result:
            result = result.split("}")[0]
            break
    else:
        print("Warning: string generation hit MAX_STEPS without stopping")

    return result, encoded_prompt


def main():
    import time

    t = time.time()
    schema = Schema(
        "../data/input/functions_definition.json",
        "../data/input/function_calling_tests.json",
    )
    tokenizer = Tokenizer()
    use_given_functions: dict[str, FunctionDefenition]
    use_given_prompts: list[dict]
    use_given_functions, use_given_prompts = schema.create_schema()

    if not use_given_prompts:
        return {}

    prompt_creator = CreatePrompt(use_given_functions)
    generator = Generator(tokenizer, use_given_functions, use_given_prompts)
    function_prompt = prompt_creator.create_main_prompt()
    parameter_prompt = prompt_creator.create_parameters_prompt()

    results: dict[str, dict] = {}

    for dic in use_given_prompts:
        request_text = build_request_text(dic)

        found_function_name = generator.start_model(function_prompt + request_text)
        print(f"Selected function: {found_function_name}")

        if found_function_name not in use_given_functions:
            print(f"  -> unknown function '{found_function_name}', skipping: {request_text}")
            results[request_text] = {"function": None, "parameters": {}}
            continue

        function_obj = use_given_functions[found_function_name]

        if not function_obj.parameters:
            results[request_text] = {"function": found_function_name, "parameters": {}}
            continue

        header = (
            f"{format_function_signature(found_function_name, function_obj)}"
            f"Request: {request_text}\n"
            f"Answer: {{ "
        )
        encoded_prompt = tokenizer.encode(parameter_prompt + header)

        generated_params: dict[str, str] = {}
        param_items = list(function_obj.parameters.items())

        for i, (key, value) in enumerate(param_items):
            encoded_prompt.extend(tokenizer.encode(f'"{key}": '))

            if value.type == "number":
                generated, encoded_prompt = generate_number_param(tokenizer, encoded_prompt)
            else:
                generated, encoded_prompt = generate_string_param(tokenizer, encoded_prompt)

            generated_params[key] = generated.strip()

            is_last = i == len(param_items) - 1
            separator = " }" if is_last else ", "
            encoded_prompt.extend(tokenizer.encode(separator))

        print(f"  -> parameters: {generated_params}")
        results[request_text] = {"function": found_function_name, "parameters": generated_params}
    print(f"\n\n this the current time {((time.time() -t )/60)} min")
    return results


if __name__ == "__main__":
    main()

