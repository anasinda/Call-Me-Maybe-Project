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
        self.current_generated: list[int] = []
        self.ids_to_str: str = ""

    def start_model(self):
        for index, prompt in enumerate(self.usable_prompts):

            for  _ in range(3):
                prompt_value = next(iter(prompt.values()))
                # print(f"Prompt-{index} name:", prompt_value)
                self.input_ids = self.tokenizer.encode(self.main_prompt + prompt_value)
                prompt_logit = self.tokenizer.encode(prompt_value)
                prompt_logit_str = self.tokenizer.decode(prompt_logit)
                # print("input ids", self.input_ids)
                # print("prompt ids", prompt_logit)
                # print("prompt str", prompt_logit_str)
                logits = np.array(self.tokenizer.get_logits(self.input_ids))
                best_logit = np.argmax(logits)
                self.input_ids.append(best_logit)
                self.generated_result.append(best_logit)
                self.ids_to_str += self.tokenizer.decode(self.generated_result)
                print("ud_str", self.ids_to_str)
                # print(f"These are generated id's:", self.generated_result)
                # print(f"This is generated string", self.tokenizer.decode(self.generated_result))

