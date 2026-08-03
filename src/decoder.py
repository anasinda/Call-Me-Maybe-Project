from src.tokenizer import Tokenizer
from src.grammar import Grammar
# from src.utils import State
from src.models import FunctionDefenition
import numpy as np

class Decoder():
    def __init__(self, grammar: Grammar, tokenizer: Tokenizer, functions: dict[str, FunctionDefenition]):
        self.grammar = grammar
        self.tokenizer = tokenizer
        self.functions = functions


    def generate_first_json(self, main_prompt: str, user_prompt: str):
        json_start = ["{", "name:"]
        generated_response = []

        token_ids = []
        for element in json_start:
            token_ids = self.tokenizer.encode(element)
            logits = np.array(self.tokenizer.get_logits(token_ids))
            mask = np.full(len(logits), -np.inf)
            for id in token_ids:
                mask[id] = 0
                masked_logits = logits + mask
                best_id = np.argmax(masked_logits)
                token_ids.append(best_id)
                generated_response.append(best_id)

        # token_ids.clear()
        # functions_list = list(self.functions.keys())
        # new_functions_id = {}

        # for index, function in enumerate(functions_list):
        #     new_functions_id[f"id{index}"] = function

        # function_id_prompt = f"""Here is the functions names {functions_list}.
        # We are going to give each one an id so as to point to the function name.
        # This is for speed, you can get these from {new_functions_id} as a
        # key and value pair.
        # Example:
        # Key: id0 == Value: {new_functions_id["id0"]}
        # Proccess these and store the id's and their corresponding function name
        # when receiving an id, think of it as a function name, but instead of generating
        # multiple token id's, generate a simple id from 0 to {len(new_functions_id.keys())}
        # but that token id will be used for getting logits for them
        # """
        # token_ids = self.tokenizer.encode(main_prompt + user_prompt + function_id_prompt)
        # logits = np.array(self.tokenizer.get_logits(token_ids))
        # mask = np.full(len(logits), -np.inf)
        # check_if_gen = ""
        # for id in token_ids:
        #     mask[id] = 0
        #     masked_logits = logits + mask
        #     best_id = np.argmax(masked_logits)
        #     check_if_gen = self.tokenizer.decode(best_id)
        #     token_ids.append(best_id)
        #     generated_response.append(best_id)
        # if check_if_gen in new_functions_id.keys:
        #     generated_response.append(",")

        return generated_response




#     def initiliaze_decoder(self, prompt: str):

#         input_ids: list[int] = self.tokenizer.encode(prompt)
#         generated: list[int] = []
#         remaining_candidates: list[list[int]] = []

#         while self.grammar.current_state != State.END:
#             logits = np.array(self.tokenizer.get_logits(input_ids))
#             mask = np.full(len(logits), -np.inf)
#             next_tokens: set[int] = set()

#             if self.grammar.current_state == State.EXPECT_PARAMETERS_VALUE:
#                 allowed_tokens = self.grammar.get_allowed_tokens()
#                 if allowed_tokens.value_type == "number":
#                     gen_num = self.generate_numbers(logits, mask, input_ids)
#                     self.grammar.consume(gen_num)
#                     continue

#                 if allowed_tokens.value_type == "string":
#                     gen_string = self.generate_string(logits, mask, input_ids)
#                     self.grammar.consume(gen_string)
#                     continue

#             if not remaining_candidates:
#                 allowed_tokens = self.grammar.get_allowed_tokens()

#                 for token in allowed_tokens.check_value_type():
#                     remaining_candidates.append(self.tokenizer.encode(token))

#             for token in remaining_candidates:
#                 if len(generated) < len(token):
#                     next_tokens.add(token[len(generated)])

#             mask[list(next_tokens)] = 0
#             masked_logits = logits + mask
#             best_token_id = np.argmax(masked_logits)
#             input_ids.append(best_token_id)
#             generated.append(best_token_id)

#             new_remaining_canidates: list[list[int]] = []
#             for token in remaining_candidates:
#                 if token[:len(generated)] == generated:
#                     new_remaining_canidates.append(token)
#             remaining_candidates = new_remaining_canidates

#             if len(remaining_candidates) == 1:
#                 if remaining_candidates[0] == generated:
#                     decode_remaining_canididate = self.tokenizer.decode(generated)
#                     self.grammar.consume(decode_remaining_canididate)
#                     generated.clear()
#                     remaining_candidates.clear()

#         return input_ids, generated, remaining_candidates


#     def generate_numbers(self, logits, mask, input_ids: list[int]):
#         best_token_num: str = ""
#         generated_numbers: str = ""
#         possible_token: list[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", ",", "}"]
#         stopping_tokens: list[str] = [",", "}"]
#         possible_token_ids: list[int] = []

#         for token in possible_token:
#             possible_token_ids.append(self.tokenizer.encode(token))

#         while True:
#             logits = np.array(self.tokenizer.get_logits(input_ids))
#             mask = np.full(len(logits), -np.inf)
#             mask[possible_token_ids] = 0
#             masked_num_logits = logits + mask
#             best_token_num_id = np.argmax(masked_num_logits)
#             best_token_num = self.tokenizer.decode(best_token_num_id)
#             if best_token_num in possible_token:
#                 if best_token_num in stopping_tokens:
#                     break
#                 else:
#                     input_ids.append(best_token_num_id)
#                     generated_numbers += best_token_num
#         return generated_numbers


#     def generate_string(self, logits, mask, input_ids: list[int]):
#         generated_string: str = ""
#         started: bool = False

#         while True:
#             logits = np.array(self.tokenizer.get_logits(input_ids))

#             best_token_str_id = np.argmax(logits)
#             best_token_str = self.tokenizer.decode(best_token_str_id)

#             input_ids.append(best_token_str_id)
#             generated_string += best_token_str

#             if best_token_str == '"':
#                 if started:
#                     break
#             else:
#                 started = True

#         return generated_string


