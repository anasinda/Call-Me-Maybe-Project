"""Constrained decoding: generates a single parameter value (number or
string) from the model, masking logits so the output is always valid."""

from .tokenizer import Tokenizer

MAX_STEPS = 64  # safety cap so a stuck generation loop can't run forever


def argmax_index(values: list[float]) -> int:
    """Return the index of the largest value in ``values``."""

    return max(range(len(values)), key=values.__getitem__)


def build_number_token_mask(tokenizer: Tokenizer) -> list[int]:
    """Token ids allowed while generating a number: digits, sign, dot,
    and the two structural characters that end a value."""
    allowed = set()
    for ch in "0123456789-.,}":
        allowed.update(tokenizer.encode(ch))
    return list(allowed)


def generate_number(tokenizer: Tokenizer, prompt_ids: list[int], number_mask: list[int]) -> str:
    """Greedily generate a numeric value, masked to number characters only."""
    value = ""
    for _ in range(MAX_STEPS):
        logits = tokenizer.get_logits(prompt_ids)
        masked_logits = [float("-inf")] * len(logits)
        for index in number_mask:
            masked_logits[index] = logits[index]
        next_token = argmax_index(masked_logits)
        next_text = tokenizer.decode([next_token])

        if next_text in (",", "}"):
            break

        prompt_ids.append(next_token)
        value += next_text
    else:
        print("Warning: number generation hit MAX_STEPS without stopping")

    return value


def generate_string(tokenizer: Tokenizer, prompt_ids: list[int]) -> str:
    """Greedily generate a string value, stopping at the first ',' or '}'."""
    value = ""
    for _ in range(MAX_STEPS):
        logits = tokenizer.get_logits(prompt_ids)
        next_token = argmax_index(logits)
        next_text = tokenizer.decode([next_token])

        prompt_ids.append(next_token)
        value += next_text

        if "," in value:
            return value.split(",")[0]
        if "}" in value:
            return value.split("}")[0]
    else:
        print("Warning: string generation hit MAX_STEPS without stopping")

    return value


def generate_parameter(tokenizer: Tokenizer, prompt_ids: list[int], param_type: str, number_mask: list[int]) -> str:
    """Dispatch to the right generator based on the parameter's declared type."""
    if param_type == "number":
        return generate_number(tokenizer, prompt_ids, number_mask)
    return generate_string(tokenizer, prompt_ids)
