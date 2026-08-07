# from tokenizer import Tokenizer
# from models import FunctionDefenition, Parameter
# import numpy as np

# class ParameterDecoder():
#     def __init__(self, tokenizer: Tokenizer):
#         self.tokenizer: Tokenizer = tokenizer
#         self.input_ids: list[int] = []
#         self.generate_result: str = ""
#         self.parameters_prompt: str = """
# You are extracting parameters for an already selected function.

# The function has already been chosen correctly.
# Your ONLY job is to extract the parameter values.

# Rules:
# - Output ONLY the parameter values.
# - Do not output JSON.
# - Do not output the function name.
# - Do not explain your reasoning.
# - Do not invent values.
# - If the value appears in the user's prompt, copy it exactly.
# - If there are multiple parameters, output them in the same order they are listed.
# - If a parameter is a number, output only the numeric value.
# - If a parameter is a string, output only the string exactly as it appears in the user's prompt.

# User prompt:

# """
#         self.parameters_ids: list[int] = self.tokenizer.encode(self.parameters_prompt)


#     def generate_parameters(self, user_prompt: str, function_name: str, function_obj: FunctionDefenition):
#         parameter_ids = self.parameters_ids.copy()
#         parameter_ids.extend(self.tokenizer.encode(user_prompt))
#         parameter_ids.extend(self.tokenizer.encode(function_name))
#         parameters_found: dict[str, str] = {}
#         for name, parameter in function_obj.parameters.items():
#             if parameter.type == "number":
#                 possible = []
#                 stop_tokens = [",", "}"]
#                 for charachter in "0123456789-.":
#                     possible += self.tokenizer.encode(charachter)
#                 # for stop_char in ",}\n":
#                 #     possible.extend(self.tokenizer.encode(stop_char))
#             elif parameter.type == "string":
#                 possible = []
#                 stop_tokens = ['"', "}", ","]
#             while True:
#                 logits = self.tokenizer.get_logits(parameter_ids)
#                 if parameter.type == "number":
#                     mask = np.full(len(logits), -np.inf)
#                     for token in possible:
#                         print("this is tokens", token)
#                         mask[token] = 0
#                     masked_logits = logits + mask
#                 elif parameter.type == "string":
#                     masked_logits = logits
#                 best_token = np.argmax(masked_logits)
#                 parameter_ids.append(best_token)
#                 decode_token = self.tokenizer.decode([best_token])
#                 print("THis is decode token", decode_token)
#                 if decode_token in stop_tokens:
#                     break
#                 self.generate_result += decode_token
#             parameter_ids.extend(self.tokenizer.encode(f"\nParameter {name}: {self.generate_result} Found\n"))
#             parameter_ids.extend(self.tokenizer.encode(f"Searching for next parameter\n"))
#             parameters_found[name] = self.generate_result
#             print("THis is name:", name)
#             print("THis is generated result:", self.generate_result)
#             self.generate_result = ""
#         return parameters_found

