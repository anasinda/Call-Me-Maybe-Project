from src.tokenizer import Tokenizer
from src.grammar import Grammar
# from src.utils import State
from src.models import FunctionDefenition, Parameter
import numpy as np

class ParameterDecoder():
    def __init__(self):
        self.tokenizer: Tokenizer = Tokenizer()
        self.input_ids: list[int] = []
        self.parameters_tokens: list[list[int]] = []
        self.remaining_tokens: list[list[int]] = []
        self.next_tokens: list[int] = []
        self.get_parameters: dict[str, Parameter]
        self.possible_num_tokens: list[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"]
        self.stopping_num_tokens: list[str] = [",", "}"]


    def generate_parameters(self, parameters_prompt: str, function_name: str, function_obj: FunctionDefenition):
        index: int = 0
        while True:
            if not self.generate_parameters:
                last_token = self.parameters_tokens[0][len(self.next_tokens):]
                self.next_tokens.extend(last_token)
                self.input_ids.extend(last_token)
                break

            logits = np.array(self.tokenizer.get_logits(self.input_ids))
            mask = np.full(len(logits), -np.inf)

            if not self.parameters_tokens:
                parameters_names: list[str] = list(function_obj.parameters.keys())
                for parameter in parameters_names:
                    if function_obj.parameters[parameter] == "number":
                        self.parameters_tokens = self.generate_numbers(parameters_prompt)
                    self.function_tokens.append(self.tokenizer.encode(function))

            for function_token in self.function_tokens:
                if index < len(function_token):
                    mask[function_token[index]] = 0

            masked_logits = logits + mask
            best_token = np.argmax(masked_logits)
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
        self.next_tokens.clear()
        self.function_tokens.clear()
        self.input_ids.clear()
        print(f"This is prompt: {user_prompt}, this is result {result}")
        return result

    def generate_numbers(self, parameters_prompt: str):
        allowed_prompt_token: str = "List of tokens to choose from:\n"
        allowed_prompt_token: str = "Stop generating at these tokens:\n"

        for token in self.possible_num_tokens:
            edit_prompt += edit_prompt + f"token\n"

