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




    def create_main_prompt(self):
        func_prompt = "You pick the right function name based on a user"
        func_prompt += " query.\n"

        func_prompt += "\nHARD RULES:\n"
        func_prompt += "- Output ONLY the function name as plain text.\n"
        func_prompt += "- Do NOT return JSON.\n"
        func_prompt += "- Do NOT add quotes.\n"
        func_prompt += "- Do NOT explain.\n"

        func_prompt += "\nSELECTION RULES:\n"
        func_prompt += "- Pick ONLY from the available functions.\n"
        func_prompt += "- Do NOT make up new function names.\n"

        func_prompt += "\nSPECIAL CASES:\n"
        func_prompt += "- If the query is empty → return: null\n"
        func_prompt += "- If no function fits → return: null\n"

        func_prompt += "\nAVAILABLE FUNCTIONS:\n"
        for func, func_obj in self.use_given_functions.items():
            func_prompt += f"\nFunction name:\n{func}\n"
            func_prompt += f"\nDescription for {func}:\n{func_obj.description}\n"
        func_prompt += "\nSAMPLES:\n"

        func_prompt += "Query: What is the sum of 2 and 3?\n"
        func_prompt += "Answer:\nfn_add_numbers\n\n"

        func_prompt += "Query: Greet John\n"
        func_prompt += "Answer:\nfn_greet\n\n"

        func_prompt += "Query: Reverse the string \"hello\"\n"
        func_prompt += "Answer:\nfn_reverse_string\n\n"

        func_prompt += "Query: What is the square root of 16?\n"
        func_prompt += "Answer:\nfn_get_square_root\n\n"

        func_prompt += "Query: Replace numbers in text\n"
        func_prompt += "Answer:\nfn_substitute_string_with_regex\n\n"

        func_prompt += "Query: Tell me a joke\n"
        func_prompt += "Answer:\nnull\n\n"

        func_prompt += "Query:\n"
        func_prompt += "Answer:\nnull\n\n"

        func_prompt += "\nNow pick the function name.\n"

        func_prompt += "\nUSER QUERY:"
        return func_prompt


    def create_parameters_prompt(self):
        param_func = "You extract ONLY function arguments from a user request.\n"

        param_func += "\nHARD RULES:\n"
        param_func += "- Return ONLY a valid JSON object.\n"
        param_func += "- Do NOT explain anything.\n"
        param_func += "- Do NOT run the function.\n"
        param_func += "- Do NOT infer outputs, only extract inputs.\n"

        param_func += "\nCRITICAL — NEVER RUN THE FUNCTION:\n"
        param_func += "- Extract ONLY what the user gave as raw input.\n"
        param_func += "- NEVER compute, reverse, sort, add, transform, square,"
        param_func += " or process the value.\n"
        param_func += "- The function will be called separately — your job is"
        param_func += " ONLY to extract.\n"
        param_func += "- 'square root of X' -> extract X as-is,"
        param_func += " do NOT compute √X\n"
        param_func += "- 'asterisks' or 'an asterisk' -> use EXACTLY \"*\""
        param_func += " (the character, not the word)\n"
        param_func += "- 'reverse string X' -> extract X as-is,"
        param_func += " do NOT compute the reversal\n"

        param_func += "\nTYPE RULES:\n"
        param_func += "- Numbers or integers must be numeric (no quotes).\n"
        param_func += "- Strings must be valid JSON strings.\n"

        param_func += "\nREGEX RULES (VERY IMPORTANT):\n"
        param_func += "- Regex must ALWAYS be a valid JSON string.\n"
        param_func += "- Escape backslashes correctly.\n"
        param_func += "- Use EXACT patterns, no variation allowed.\n"

        param_func += "- For 'all numbers' → use EXACTLY \"\\\\d+\"\n"
        param_func += "- For 'all vowels' → use EXACTLY \"[aeiouAEIOU]\"\n"

        param_func += "- ONLY use the exact allowed regex.\n"

        param_func += "\nLANGUAGE RULES:\n"
        param_func += "- 'half of X' → X / 2\n"
        param_func += "- Convert words to numbers: one=1, two=2, three=3\n"

        param_func += "\nSQUARE ROOT RULES :\n"
        param_func += "\nTake the parameter number for square root. DON'T COMPUTE OR DO MATH :\n"

        param_func += "\nSAMPLES:\n"

        param_func += "Function: fn_get_square_root(a: number)\n"
        param_func += "Request: Calculate the square root of 45?\n"
        param_func += 'Answer:\n{"a": 45}\n'

        param_func += "Function: fn_get_square_root(a: number)\n"
        param_func += "Request: Calculate the square root of 144?\n"
        param_func += 'Answer:\n{"a": 144}\n'

        param_func += "Function: fn_get_square_root(a: number)\n"
        param_func += "Request: Calculate the square root of 5?\n"
        param_func += 'Answer:\n{"a": 5}\n'

        param_func += "EXAMPLES OF HOW TO ANWSER FOR REGEX FUNCTION"
        param_func += "Function: fn_substitute_string_with_regex(source_string:"
        param_func += " string, regex: string, replacement: string)\n"
        param_func += 'Replace all numbers in \"Hello 34 I\'m 233 years old\" with NUMBERS'
        param_func += '"Hello 34 I\'m 233 years old" with NUMBERS\n'
        param_func += 'Answer:\n{"source_string": "Hello 34 I\'m 233 years old",'
        param_func += ' "regex": "\\\\d+", "replacement": "NUMBERS"}\n'

        param_func += "Function: fn_substitute_string_with_regex(source_string: "
        param_func += "string, regex: string, replacement: string)\n"
        param_func += 'Request: '
        param_func += 'Replace all vowels in "Programming is fun" with "*"\n'
        param_func += 'Answer:\n{"source_string": "Programming is fun",'
        param_func += ' "regex": "[aeiouAEIOU]", "replacement": "*"}\n'

        param_func += "Function: fn_substitute_string_with_regex(source_string: "
        param_func += "string, regex: string, replacement: string)\n"
        param_func += "Request: "
        param_func += "Substitute the word 'cat' with 'dog' in "
        param_func += "'The cat sat on the mat with another cat'\n"
        param_func += 'Answer:\n{"source_string": "The cat sat on the mat with another cat",'
        param_func += ' "regex": "cat", "replacement": "dog"}\n'
        param_func += "\nNow extract arguments for this request.\n"

        return param_func

    def create_regex_prompt(self):
        # regex_param = "VERY IMPORTAN FIRST RULE:\n"

        # regex_param += "\nSPECIAL RULE FOR fn_substitute_string_with_regex:\n"
        # regex_param += "- This function has exactly three parameters:\n"
        # regex_param += "  source_string, regex, replacement.\n"
        # regex_param += "- source_string is the text the user wants to modify.\n"
        # regex_param += "- replacement is exactly what the user wants to insert.\n"
        # regex_param += "- regex is NOT described in words.\n"
        # regex_param += "- Convert the user's request into the correct regex.\n"

        # regex_param += "\nRegex mapping:\n"
        # regex_param += "- numbers / digits / numeric values -> \"\\\\d+\"\n"
        # regex_param += "- vowels -> \"[aeiouAEIOU]\"\n"
        # regex_param += "- spaces / whitespace -> \"\\\\s+\"\n"
        # regex_param += "- letters -> \"[A-Za-z]+\"\n"
        # regex_param += "- words -> \"\\\\w+\"\n"

        # regex_param += "- Never explain the regex.\n"
        # regex_param += "- Only output the regex string.\n"


        regex_param = "\nEXAMPLES:\n"
        regex_param += (
        '{"source_string":"Hello 34 I\'m 233 years old","regex":"\\\\d+","replacement":"NUMBERS"}\n\n'
        )

        # regex_param += (
        # 'Function: fn_substitute_string_with_regex(source_string: string, regex: string, replacement: string)\n'
        # 'Request: Replace all digits in "abc123xyz" with "#"\n'
        # 'Answer:\n'
        # '{"source_string":"abc123xyz","regex":"\\\\d+","replacement":"#"}\n\n'
        # )

        # regex_param += (
        # 'Function: fn_substitute_string_with_regex(source_string: string, regex: string, replacement: string)\n'
        # 'Request: Replace all vowels in "Programming is fun" with "*"\n'
        # 'Answer:\n'
        # '{"source_string":"Programming is fun","regex":"[aeiouAEIOU]","replacement":"*"}\n\n'
        # )

        # regex_param += (
        # 'Function: fn_substitute_string_with_regex(source_string: string, regex: string, replacement: string)\n'
        # 'Request: Replace all spaces in "hello world" with "_"\n'
        # 'Answer:\n'
        # '{"source_string":"hello world","regex":"\\\\s+","replacement":"_"}\n\n'
        # )

        # regex_param += "\nUse the following information to extract arguments for this request.\n"

        return regex_param
    # def create_parameters_prompt(self, function_name: str, user_prompt: str):
    #     selected_func_obj = self.use_given_functions[function_name]
    #     full_parameters_prompt = self.parameters_prompt
    #     full_parameters_prompt += f"\nFunction name:\n{selected_func_obj.name}\n"
    #     full_parameters_prompt += f"\nDescription for {selected_func_obj.name}:\n{selected_func_obj.description}\n"
    #     # full_parameters_prompt += f"\nUsage: {self.function_examples[selected_func_obj.name]}\n"
    #     full_parameters_prompt += f"\nParameters:\n"
    #     for key, value in selected_func_obj.parameters.items():
    #         full_parameters_prompt += f"- {key} : {value.type}\n"

    #     full_parameters_prompt += "\nUSER PROMPT:\n"
    #     full_parameters_prompt += f"{user_prompt}\n"
    #     full_parameters_prompt += f"\nOutput:\n"
    #     return full_parameters_prompt


