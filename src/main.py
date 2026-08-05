from schema import Schema
from function_constraint_decoder import Generator
from base_prompt import CreatePrompt
from models import FunctionDefenition
from typing import Any
from parameter_constraint_decoder import ParameterDecoder
from tokenizer import Tokenizer

def main():
    schema = Schema("../data/input/functions_definition.json", "../data/input/function_calling_tests.json")
    tokenizer: Tokenizer = Tokenizer()
    llm_usable_functions, llm_given_prompts = schema.create_schema()
    use_given_functions: dict[str, FunctionDefenition] = llm_usable_functions
    use_given_prompts: list[dict, Any] = llm_given_prompts #[value.prompt for value in llm_given_prompts.values()]
    json_func_dict: dict[str, str] = {}


    if use_given_prompts:
        prompt_creator = CreatePrompt(use_given_functions)
        generator = Generator(tokenizer, use_given_functions, use_given_prompts)
        parameter_decoder = ParameterDecoder(tokenizer)
        function_prompt = prompt_creator.create_main_prompt()


        for prompt in use_given_prompts:
            user_prompt = next(iter(prompt.values())) + '\n'
            prompt_result_func, selected_input_ids = generator.start_model(function_prompt + user_prompt, user_prompt)
            parameters_prompt = prompt_creator.create_parameters_prompt(prompt_result_func, user_prompt)
            prompt_result_parm = parameter_decoder.generate_parameters(user_prompt, parameters_prompt, selected_input_ids, use_given_functions[prompt_result_func])
            # json_func_dict["prompt"] = user_prompt
            # json_func_dict["name"] = prompt_result_func

if __name__ == "__main__":
    main()
