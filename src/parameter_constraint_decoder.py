from tokenizer import Tokenizer
from models import FunctionDefenition, Parameter
import numpy as np

class ParameterDecoder():
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer: Tokenizer = tokenizer
        self.input_ids: list[int] = []
        # self.parameters_tokens: list[list[int]] = []
        # self.get_parameters: dict[str, Parameter]
        # self.possible_num_tokens: str = "0123456789-.,}"
        # self.stopping_num_tokens: list[str] = [',', '}']
        self.generate_result: str = ""


    def generate_parameters(self, user_prompt: str, parameters_prompt: str, selected_input_ids: list[int], function_obj: FunctionDefenition):

        parameter_ids = self.tokenizer.encode(parameters_prompt)
        for name, parameter in function_obj.parameters.items():
            if parameter.type == "number":
                possible = []
                stop_tokens = [",", "}", "\n"]
                for charachter in "0123456789-.,}":
                    possible.append(self.tokenizer.encode(charachter))
                # for stop_char in ",}\n":
                #     possible.extend(self.tokenizer.encode(stop_char))
            elif parameter.type == "string":
                possible = []
                for token in user_prompt.split():
                    possible.append(self.tokenizer.encode(token))
                stop_tokens = ['"', "\n", "}", ","]

            while True:
                logits = self.tokenizer.get_logits(parameter_ids)
                # if parameter.type == "number":
                mask = np.full(len(logits), -np.inf)
                for token in possible:
                    mask[token] = 0
                masked_logits = logits + mask
                # elif parameter.type == "string":
                    # masked_logits = logits
                best_token = np.argmax(masked_logits)
                parameter_ids.append(best_token)
                decode_token = self.tokenizer.decode([best_token])
                if decode_token in stop_tokens:
                    break
                self.generate_result += decode_token
            parameters_prompt += f"\nParameter {name}: {self.generate_result} Found\n"
            parameters_prompt += f"Searching for next parameter\n"
            print("THis is generated result:", self.generate_result)
            self.generate_result = ""
