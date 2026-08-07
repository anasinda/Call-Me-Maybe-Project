from schema import Schema
from function_constraint_decoder import Generator
from base_prompt import CreatePrompt
from models import FunctionDefenition
from typing import Any
from tokenizer import Tokenizer
import numpy as np

def main():
    schema = Schema("../data/input/functions_definition.json", "../data/input/function_calling_tests.json")
    tokenizer: Tokenizer = Tokenizer()
    llm_usable_functions, llm_given_prompts = schema.create_schema()
    use_given_functions: dict[str, FunctionDefenition] = llm_usable_functions
    use_given_prompts: list[dict, Any] = llm_given_prompts
    json_func_dict: dict[str, str] = {}


    if use_given_prompts:
        prompt_creator = CreatePrompt(use_given_functions)
        generator = Generator(tokenizer, use_given_functions, use_given_prompts)
        function_prompt = prompt_creator.create_main_prompt()


        # user_prompt = "Replace all numbers in \"Hello 34 I'm 233 years old\" with NUMBERS"
        parameter_prompt = prompt_creator.create_parameters_prompt()


        regex_prompt = prompt_creator.create_regex_prompt()
        for dic in use_given_prompts:
            prompt_get = str(dic.values())
            found_function_name = generator.start_model(function_prompt + prompt_get, prompt_get)
            function_obj = use_given_functions[found_function_name]
            add_parameters = "("
            first = False
            for key, value in function_obj.parameters.items():
                if first:
                    add_parameters += ","
                first = True
                add_parameters += f"{key}: "
                add_parameters += f"{value.type}"
            if first:
                add_parameters += ")"
            print("This is found func", found_function_name)
            add_function = f"Function: {found_function_name}{add_parameters}\n"
            add_prompt = f"Request: {prompt_get}\n"
            add_response = f"Anwser: {{ "
            sum_prompt_req = (add_function + add_prompt + add_response)
            encoded_para_prompt = tokenizer.encode((parameter_prompt + sum_prompt_req))
            for key_p, value_p in function_obj.parameters.items():
                encoded_para_prompt.extend(tokenizer.encode(f"{key_p}: "))
                generated_result = ""
                # if found_function_name == "fn_substitute_string_with_regex":
                #     encoded_para_prompt.extend(tokenizer.encode((regex_prompt)))
                    # while True:
                    #     encoded_para_prompt.extend(encoded_regex_prompt)
                    #     logits = tokenizer.get_logits(encoded_para_prompt)
                    #     best_token = np.argmax(logits)
                    #     decoded_token = tokenizer.decode([best_token])
                    #     encoded_para_prompt.append(best_token)
                    #     generated_result += decoded_token
                    #     print("THis is decoded in regex", decoded_token)
                    #     if decoded_token == "ĠFinished":
                    #         break
                if value_p.type == "number":
                    possible = []
                    for char in "0123456789-.,}":
                        possible.extend(tokenizer.encode(char))
                    while True:
                        logits = tokenizer.get_logits(encoded_para_prompt)
                        mask = np.full(len(logits), -np.inf)
                        mask[possible] = 0
                        masked_logits = logits + mask
                        best_token = np.argmax(masked_logits)
                        decoded_token = tokenizer.decode([best_token])
                        if decoded_token == "," or decoded_token == "}":
                            break
                        else:
                            encoded_para_prompt.append(best_token)
                            generated_result += decoded_token
                elif value_p.type == "string":
                    # possible = list(set(tokenizer.encode(user_prompt)))
                    # possible.extend(tokenizer.encode('"'))
                    # possible.extend(tokenizer.encode(","))
                    # possible.extend(tokenizer.encode("}"))
                    while True:
                        logits = tokenizer.get_logits(encoded_para_prompt)
                        # mask = np.full(len(logits), -np.inf)
                        # mask[possible] = 0
                        # masked_logits = logits + mask
                        best_token = np.argmax(logits)
                        decoded = tokenizer.decode([best_token])
                        print("THis is decoded in string", decoded)
                        # if decoded == ',':
                        #     break
                        encoded_para_prompt.append(best_token)
                        generated_result += decoded

                        # if "," in generated_result:
                        #     generated_result = generated_result.split(",")[0]
                        #     break

                        if "}" in generated_result:
                            generated_result = generated_result.split("}")[0]
                            break
                print("This is generated", generated_result)
                # print("This parameter prompt", parameter_prompt)

if __name__ == "__main__":
    main()
