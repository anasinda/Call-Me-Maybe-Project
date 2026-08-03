from tokenizer import Tokenizer
import numpy as np
from typing import Any



class Generator():
    def __init__(self, usable_funcs: list[str], usable_prompts: list[str], main_prompt: str):
        self.tokenizer: Tokenizer = Tokenizer()
        self.usable_funcs: list[dict[str, Any]] = usable_funcs
        self.usable_prompts: list[dict[str, str]] = usable_prompts
        self.main_prompt: str = main_prompt
        self.input_ids: list[int] = []
        self.generated_result: list[int] = []
        self.next_tokens: list[int] = []
        self.remaining_tokens: list[int] = []
        self.ids_to_str: str = ""

    def start_model(self):
        self.input_ids = self.tokenizer.encode(self.main_prompt)
        logits = np.array(self.tokenizer.get_logits(self.input_ids))
        mask = np.full(len(logits), -np.inf)
        end: int = 0

        while True:
            for token in self.input_ids:
                if end < len(token):
                    mask[token[end]] = 0
                else:
                    break
            end += 1
            best_token = np.argmax(logits)
            self.next_tokens.append(best_token)
            for token in self.input_ids:
                if self.next_tokens in token:
                    self.remaining_tokens.append(token)




