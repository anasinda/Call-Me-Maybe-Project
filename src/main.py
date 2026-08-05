from schema import Schema
from function_constraint_decoder import Generator
from base_prompt import CreatePrompt
from models import FunctionDefenition
from typing import Any
# from parameter_constraint_decoder import ParameterDecoder

def main():

    promtes = [{"prompte":"str"}]
    schema = Schema("../data/input/functions_definition.json", "../data/input/function_calling_tests.json")

    llm_usable_functions, llm_given_prompts = schema.create_schema()
    use_given_functions: dict[str, FunctionDefenition] = llm_usable_functions
    use_given_prompts: list[dict, Any] = llm_given_prompts #[value.prompt for value in llm_given_prompts.values()]

    if use_given_prompts:
        prompt_creator = CreatePrompt(use_given_functions)
        generator = Generator(use_given_functions, use_given_prompts)
        # parameter_decoder = ParameterDecoder()
        main_prompt = prompt_creator.create_main_prompt()
        print(main_prompt)

        for prompt in use_given_prompts:
            # main_prompt , parameters_prompt = prompt_creator.create_main_prompt()
            value = next(iter(prompt.values())) + '\n'
            generated_function = generator.start_model(main_prompt + value, value)
            # parameter_decoder.generate_parameters(parameters_prompt, generated_function, use_given_functions[generated_function])

if __name__ == "__main__":
    main()


# generator = Generator(use_given_functions, use_given_prompts, main_prompt)
# generator.start_model()

# print("Function names:", use_given_functions)
# print("Prompt names:", use_given_prompts)
