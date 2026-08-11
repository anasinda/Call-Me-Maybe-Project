from models import FunctionDefenition


class CreatePrompt():
    def __init__(self, use_given_functions: dict[str, FunctionDefenition]):
        self.use_given_functions = use_given_functions
        self.function_examples: dict[str, str] = {
            "fn_no_match": "Anything that the other functions can't handle: null.",
            "fn_add_numbers": "I need to add two numbers: 43 and 81.",
            "fn_greet": "Can you greet Mike?",
            "fn_reverse_string": "Can you reverse 'byebye'?",
            "fn_get_square_root": "What's the square root of 81?",
            "fn_substitute_string_with_regex": "Substitute the word 'up' with 'down' in 'I went up and down then left then right'"
        }

        self.functions_example_select: dict[str, str] = {
            "fn_no_match": "Only used when you can not find another function to use for the user prompt",
            "fn_add_numbers": "Only use this for arithmetic addition of two numbers — not for text replacement or substitution.",
            "fn_greet": "Only use this for producing a greeting for a named person — not for math or text editing.",
            "fn_reverse_string": "Only use this to flip the entire order of a string end-to-end — not for replacing or substituting parts of it.",
            "fn_get_square_root": "Only use this for computing a square root of a single number — not for addition or any text operation.",
            "fn_substitute_string_with_regex": "Use this whenever the request involves replacing, substituting, or swapping words, characters, or patterns within text — not for arithmetic.",
        }

        self.function_parameter_getter: dict[str, str] = {
            "fn_no_match": "Takes value = no_match.",
            "fn_add_numbers": "Takes a = the first number, b = the second number.",
            "fn_greet": "Takes name = the person's name only, with no action word attached.",
            "fn_reverse_string": "Takes s = the exact string to reverse, unreversed.",
            "fn_get_square_root": "Takes a = the number as-is, never the computed result.",
            "fn_substitute_string_with_regex": "Takes source_string = the original text, regex = the pattern to match, replacement = the text to substitute in.",
        }





    def create_main_prompt(self):
        func_prompt = f"""
==================================================
FUNCTION SELECTION RULES
==================================================

1. Select a function only when the user's request clearly matches
   what that function is designed to do.

2. Match the MEANING of the request, not just individual words.

3. A shared word is NOT enough to select a function.

4. Do not select a function just because part of the request
   looks similar to its description.

5. If the request requires an operation that none of the functions
   provide, select fn_no_match.

6. If the request is unrelated to every available function,
   select fn_no_match.

7. If you are uncertain whether a function is appropriate,
   select fn_no_match.

8. Never invent a function that is not in the available list.

==================================================
WHEN TO USE fn_no_match
==================================================

Select fn_no_match ONLY when none of the available functions can
correctly handle the user's request.

Use fn_no_match when:

- The requested operation is not provided by any available function.
- The request is unrelated to all available functions.
- The request asks for general information or conversation.
- The request requires an operation that no available function supports.
- A function only shares a word with the request but does not match
  the requested operation.
- The request cannot be handled correctly by any single available
  function.

Do NOT select fn_no_match when an available function clearly matches
the requested operation.

==================================================
VALID FUNCTION EXAMPLES
==================================================

These requests MUST NOT use fn_no_match because a suitable function
exists.

Request:
"Add -43 and 81."
Selected function:
fn_add_numbers

Request:
"Say hello to Sarah."
Selected function:
fn_greet

Request:
"Flip the string 'Programming' backwards."
Selected function:
fn_reverse_string

Request:
"What is the square root of 81?"
Selected function:
fn_get_square_root

Request:
"Replace all numbers in \"My age is 25 and my brother is 17\" with NUMBERS"
Selected function:
fn_substitute_string_with_regex

Request:
"Replace every occurrence of 'hello' with 'hi' in 'hello world hello'."
Selected function:
fn_substitute_string_with_regex

==================================================
FN_NO_MATCH EXAMPLES
==================================================

These requests MUST use fn_no_match because no available function
can correctly perform the requested operation.

Request:
"What is the capital of Morocco?"
Selected function:
fn_no_match

Request:
"What's the weather today?"
Selected function:
fn_no_match

Request:
"Tell me a joke."
Selected function:
fn_no_match

Request:
"Translate 'hello' into French."
Selected function:
fn_no_match

Request:
"Multiply 7 by 8."
Selected function:
fn_no_match

Request:
"Divide 100 by 5."
Selected function:
fn_no_match

Request:
"Sort these numbers: 8, 2, 5, 1."
Selected function:
fn_no_match


Request:
"Calculate 20 percent of 50."
Selected function:
fn_no_match

Request:
"What's the largest city in Morocco?"
Selected function:
fn_no_match

Request:
"Write a Python program that adds two numbers."
Selected function:
fn_no_match

Request:
"Convert 100 dollars to euros."
Selected function:
fn_no_match

Request:
"Summarize this text for me."
Selected function:
fn_no_match

==================================================
IMPORTANT DISTINCTION
==================================================

Do NOT choose a function merely because a word appears in the
request.

For example:

Request:
"How many people live in a city?"

Selected function:
fn_no_match

The word "number" or a numeric concept does NOT automatically mean
fn_add_numbers or fn_get_square_root.

Request:
"Tell me a joke about adding numbers."

Selected function:
fn_no_match

The word "adding" does NOT automatically mean fn_add_numbers.
The actual requested operation is telling a joke.

Request:
"Explain what a square root is."

Selected function:
fn_no_match

The request asks for an explanation, not for calculating the square
root of a number.

Request:
"Reverse the order of these numbers: 1, 2, 3."

Selected function:
fn_no_match

fn_reverse_string only handles strings, not numeric lists.

Request:
"Replace the number 5 with 10 in my calculation."

Selected function:
fn_no_match

This is not necessarily a string substitution request because no
source string is provided.

==================================================
DECISION RULE
==================================================

First determine what operation the user is asking for.

Then compare that operation with the available functions.

If exactly one available function clearly supports the operation,
select that function.

If no available function supports the operation, select fn_no_match.

Never choose a function based only on a matching word.

Return ONLY the function name.
"""

        func_prompt += "\nAVAILABLE FUNCTIONS:\n"
        for func, func_obj in self.use_given_functions.items():
            func_prompt += f"\nFunction name:\n{func}\n"
            func_prompt += f"\nDescription for {func}:\n{func_obj.description}\n"
            # func_prompt += f"\n Use case: {self.functions_example_select[func]}"

        func_prompt += "\nRequest:"
        return func_prompt


    def create_parameters_prompt(self):
        param_func = "You extract ONLY function arguments from a user request.\n"


        param_func += "\nHARD RULES:\n"
        param_func += "\nDO NOT GIVE BACK A REVERSED PARAMETER FOR fn_reverse_string\n"
        param_func += "- Return ONLY a valid JSON object.\n"
        param_func += "- Do NOT explain anything.\n"
        param_func += "- Do NOT run the function.\n"
        param_func += "- Do NOT infer outputs, only extract inputs.\n"
        param_func += "- Do NOT try to reverse the parameter.\n"
        param_func += "- You MUST take the parameter as is in the same sequence. THIS IS VERY IMPORTANT.\n"

        param_func += "\nCRITICAL — NEVER RUN THE FUNCTION:\n"
        param_func += "- Extract ONLY what the user gave as raw input.\n"
        param_func += "- NEVER compute, reverse, sort, add, transform, square,"
        param_func += " or process the value.\n"
        # param_func += "- The function will be called separately — your job is"
        # param_func += " ONLY to extract.\n"
        # param_func += "- 'square root of X' -> extract X as-is,"
        # param_func += " do NOT compute √X\n"
        # param_func += "- 'cube of X' -> extract X as-is,"
        # param_func += " do NOT compute X^3\n"
        # param_func += "- 'plus signs' or 'a plus sign' -> use EXACTLY \"+\""
        # param_func += " (the character, not the word)\n"
        # param_func += "- 'reverse string X' -> extract X as-is,"
        # param_func += " do NOT compute the reversal\n"

        param_func += "\nCRITICAL — NEVER INCLUDE THE VERB OR ACTION WORD:\n"
        param_func += "- Extract ONLY the argument itself, never the command"
        param_func += " word that triggered it.\n"
        param_func += "- 'greet' / 'say hello to' / 'welcome' are ACTIONS,"
        # param_func += " not part of the name — never include them.\n"
        # param_func += "- 'Greet Shrek' -> the name is 'Shrek', NOT"
        # param_func += " 'greet' or 'greet Shrek'\n"

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


        param_func += "\nSAMPLES:\n"

        param_func += "Function: fn_reverse_string(s: string)\n"
        param_func += "Request: Reverse the string 'hello'\n"
        param_func += 'Answer:\n{"s": "hello"}\n\n'

        param_func += "Function: fn_reverse_string(s: string)\n"
        param_func += "Request: Can you reverse 'hey'\n"
        param_func += 'Answer:\n{"s": "hey"}\n'

        param_func += "Function: fn_reverse_string(s: string)\n"
        param_func += "Request: Flip the order of 'swallow'\n"
        param_func += 'Answer:\n{"s": "swallow"}\n'

        param_func += "Function: fn_get_square_root(a: number)\n"
        param_func += "Request: Square root of 7 please\n"
        param_func += 'Answer:\n{"a": 7}\n'

        param_func += "Function: fn_greet(name: string)\n"
        param_func += "Request: Say hello to Fiona\n"
        param_func += 'Answer:\n{"name": "Fiona"}\n'

        param_func += "EXAMPLES OF HOW TO ANSWER FOR REGEX FUNCTION:\n"
        param_func += "Function: fn_substitute_string_with_regex(source_string:"
        param_func += " string, regex: string, replacement: string)\n"
        param_func += 'Request: '
        param_func += 'Replace all numbers in "Room 12 has 4 chairs" with NUM\n'
        param_func += 'Answer:\n{"source_string": "Room 12 has 4 chairs",'
        param_func += ' "regex": "\\\\d+", "replacement": "NUM"}\n'

        param_func += "Function: fn_substitute_string_with_regex(source_string: "
        param_func += "string, regex: string, replacement: string)\n"
        param_func += 'Request: '
        param_func += 'Replace all vowels in "Learning to code" with "#"\n'
        param_func += 'Answer:\n{"source_string": "Learning to code",'
        param_func += ' "regex": "[aeiouAEIOU]", "replacement": "#"}\n'

        param_func += "\nNow extract arguments for this request.\n"

        return param_func
