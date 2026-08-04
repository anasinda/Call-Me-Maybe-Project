from models import FunctionDefenition


class CreatePrompt():
    def __init__(self, use_given_functions: dict[str, FunctionDefenition]):
        self.use_given_functions = use_given_functions
        self.main_prompt = f"""
You are a function selector.
Based on the available functions, you are free to choose
whichever you deem to be of correct use to the USER PROMPT.
Look at the function type, it's description to get an idea for what it does.
The parameters are there as well to help with what you will output
LOOK at the description first always, then read the context of the USER PROMPT
Choose the function you find the most suited

Available functions:
"""

    def create_main_prompt(self):
        end = len(self.use_given_functions.keys())
        while end > 0:
            for func, func_obj in self.use_given_functions.items():
                self.main_prompt += f"\nFunction:\n{func}\n"
                self.main_prompt += f"\nDescription:\n{func_obj.description}\n"
                self.main_prompt += f"\nParameters:\n"
                for param, param_value in func_obj.parameters.items():
                    self.main_prompt += f"{param}: {param_value}\n"
                self.main_prompt += "\n----------------\n"
                end -= 1
            if end <= 0:
                self.main_prompt += "\nUSER PROMPT:\n"
        return self.main_prompt
