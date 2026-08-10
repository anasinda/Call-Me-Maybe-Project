"""Simple model driver used to select a function from the prompt."""

from .models import FunctionDefenition
from .tokenizer import Tokenizer


class Generator:
    def __init__(
        self,
        tokenizer: Tokenizer,
        usable_funcs: dict[str, FunctionDefenition],
        usable_prompts: list[dict[str, str]],
    ):
        self.tokenizer: Tokenizer = tokenizer
        self.usable_funcs: dict[str, FunctionDefenition] = usable_funcs
        self.usable_prompts: list[dict[str, str]] = usable_prompts
        self.input_ids: list[int] = []
        self.next_tokens: list[int] = []
        self.function_tokens: list[list[int]] = []
        self.remaining_tokens: list[list[int]] = []

    def start_model(self, main_prompt: str) -> str:
        index: int = 0
        self.input_ids = self.tokenizer.encode(main_prompt)
        while True:
            if len(self.function_tokens) == 1:
                last_token = self.function_tokens[0][len(self.next_tokens):]
                self.next_tokens.extend(last_token)
                self.input_ids.extend(last_token)
                break

            logits = self.tokenizer.get_logits(self.input_ids)
            mask = [float("-inf")] * len(logits)

            if not self.function_tokens:
                function_names: list[str] = list(self.usable_funcs.keys())
                function_names.append("fn_no_match")
                for function in function_names:
                    print(
                        "Looping threw functions --- now on: ",
                        function,
                    )
                    encoded_function = self.tokenizer.encode(function)
                    self.function_tokens.append(encoded_function)

            for function_token in self.function_tokens:
                if index < len(function_token):
                    mask[function_token[index]] = 0.0

            masked_logits = [
                logit + mask_value
                for logit, mask_value in zip(logits, mask)
            ]
            best_token = max(
                range(len(masked_logits)),
                key=masked_logits.__getitem__,
            )
            self.input_ids.append(best_token)
            self.next_tokens.append(best_token)

            for match_token in self.function_tokens:
                if match_token[:len(self.next_tokens)] == self.next_tokens:
                    self.remaining_tokens.append(match_token)
            if not self.remaining_tokens:
                raise RuntimeError("No function matches generated prefix...")

            self.function_tokens = self.remaining_tokens.copy()
            self.remaining_tokens.clear()
            index += 1

        result = self.tokenizer.decode(self.next_tokens)
        print("THis is function processed: ", result)

        self.next_tokens.clear()
        self.function_tokens.clear()
        self.input_ids.clear()
        return result
