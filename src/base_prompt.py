from models import FunctionDefenition


class CreatePrompt():
    def __init__(self, use_given_functions: dict[str, FunctionDefenition]):
        self.use_given_functions = use_given_functions
        self.function_examples: dict[str, str] = {
            "fn_add_numbers": "I need to add two numbers: 43 and 81.",
            "fn_greet": "Can you greet Mike?",
            "fn_reverse_string": "Can you reverse 'byebye'?",
            "fn_get_square_root": "What's the square root of 81?",
            "fn_substitute_string_with_regex": "Substitute the word 'up' with 'down' in 'I went up and down then left then right'"
        }

        self.functions_example_select: dict[str, str] = {
            "fn_add_numbers": "Only use this for arithmetic addition of two numbers — not for text replacement or substitution.",
            "fn_greet": "Only use this for producing a greeting for a named person — not for math or text editing.",
            "fn_reverse_string": "Only use this to flip the entire order of a string end-to-end — not for replacing or substituting parts of it.",
            "fn_get_square_root": "Only use this for computing a square root of a single number — not for addition or any text operation.",
            "fn_substitute_string_with_regex": "Use this whenever the request involves replacing, substituting, or swapping words, characters, or patterns within text — not for arithmetic.",
        }
        self.main_prompt = f"""
You are an API function caller.

Your task is to complete a JSON object describing the function call.

Rules:
- Output valid JSON only.
- Do not explain anything.
- The function name MUST be one of the available functions.
- Choose the function whose description best matches the user's request.
"""
        self.parameters_prompt: str = """
You are extracting arguments for ONE function.
You already found the correct function
It is 100% the right function for the USER PROMPT

Rules:
- Only produce the value(s) for the parameters.
- Do not choose another function.
- Use information from the user's request only.
- If a parameter is a number, output only the number or numbers.
- If a parameter is a string, output only the string exactly as requested.


"""
        self.main_prompt_temp = self.main_prompt


    def create_main_prompt(self):
        full_prompt = self.main_prompt
        full_parameters_prompt = self.parameters_prompt
        for func, func_obj in self.use_given_functions.items():
            full_prompt += f"\nFunction name: {func}"
            full_parameters_prompt += f"\nFunction name: {func}"
            full_prompt += f"\nDescription for {func}: {func_obj.description}\n"
            full_parameters_prompt += f"\nDescription for {func}: {func_obj.description}\n"
            full_prompt += f"\nParameters:\n"
            full_parameters_prompt += f"\nParameters:\n"
            for param, param_value in func_obj.parameters.items():
                full_prompt += f"- {param} : {param_value}\n"
                full_parameters_prompt += f"- {param} : {param_value}\n"
                full_prompt += f"\nExample:\n"
                full_prompt += f"{self.function_examples[func]}\n"
                full_prompt += f"\nResponse:"
                full_prompt += f"\n{func}\n"
                full_prompt += f"\nUse case:"
                full_prompt += f"\n{self.functions_example_select[func]}\n"
                full_prompt += "\n----------------\n"

        full_prompt += "\nUSER PROMPT:"
        full_parameters_prompt += "\nUSER PROMPT:"
        return full_prompt, f

    # def create_parameters_prompt(self):
    #     full_parameters_prompt = self.parameters_prompt
    #     for
