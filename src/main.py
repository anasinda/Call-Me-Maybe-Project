from schema import Schema
from generator import Generator
from utils import CreatePrompt
from models import FunctionDefenition
from typing import Any

def main():

    promtes = [{"prompte":"str"}]
    schema = Schema("../data/input/functions_definition.json", "../data/input/function_calling_tests.json")

    llm_usable_functions, llm_given_prompts = schema.create_schema()
    use_given_functions: dict[str, FunctionDefenition] = llm_usable_functions
    use_given_prompts: list[dict, Any] = llm_given_prompts #[value.prompt for value in llm_given_prompts.values()]

    if use_given_prompts:
        prompt_creator = CreatePrompt(use_given_functions)
        main_prompt = prompt_creator.create_main_prompt()
        print(main_prompt)
        user_prompt = "What is the sum of 2 and 3?"
        generator = Generator(use_given_functions, use_given_prompts, (main_prompt + user_prompt))
        generator.start_model()
        
if __name__ == "__main__":
    main()


# generator = Generator(use_given_functions, use_given_prompts, main_prompt)
# generator.start_model()

# print("Function names:", use_given_functions)
# print("Prompt names:", use_given_prompts)
