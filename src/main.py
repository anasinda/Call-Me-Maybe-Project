from schema import Schema
from generator import Generator

promtes = [{"prompte":"str"}]

schema = Schema("../data/input/functions_definition.json", "../data/input/function_calling_tests.json")

llm_usable_functions, llm_given_prompts = schema.create_schema()
use_given_functions: list[dict] = llm_usable_functions #list(llm_usable_functions.keys())
use_given_prompts: list[dict] = llm_given_prompts #[value.prompt for value in llm_given_prompts.values()]

main_prompt = f"""
You are a function selector.
You have a list of dictionaries {llm_usable_functions} that has all the functions that you can use.
{llm_usable_functions} is a list of dictionaries as I said, so you need to enter the list, and go into each dictionary
and search for this first, search for '"description":', which will give you context and an idea about which function to choose
for the prompts given to you to anwser.
You will use whatever value in '"description":' key to get an idea about the context, and what function suits the needs of the prompt.
After that, you will search specificly for '"name":' key, if you find this, that means you need to take the next thing to it, which is the value of the key,
and that will MOST CERTAINLY BE, the function name.
After you get the function name, description about what the function does, you will search for the '"parameters":' key. it will be another dictionary, so a nested
dictionary withen our function definition dictionary. You will get the keys for that nested dictionary for example, they could be '"a":' and or '"b":', etc...
Get each key and its value, the value will be after ':'. If the value == '"number"' it is an integer starting from 0 to 9, if there is a '-', that is also part of the number.
'-0123456789' == what a '"number can consist of"'. If the value == "string", you can decide for yourself based on the user prompt, description of the function definition, and function name.
You will return a structured json format, here is an example bellow:
{{"name": fn_add_numbers, "parameters": "a": value, "b": value}}
The format above is what you will try to imitate, only changing name value and parameters based on context, prompt, description, and function name you chose.


Available functions:
{llm_usable_functions}

You will decide what a prompt is if it follows a similar structure bellow, and "User":' will be before it, above it or next to it like in the examples bellow:

Examples:

User: What is the sum of 2 and 3?
Output:
fn_add_number

User: Add 15 and 42.
Output:
fn_add_number

User: What's 100 plus 250?
Output:
fn_add_number

User: Can you add 1 and 9?
Output:
fn_add_number

User: Greet Shrek.
Output:
fn_greet

User: Say hello to John.
Output:
fn_greet

User: Welcome Alice.
Output:
fn_greet

User: Greet my friend Bob.
Output:
fn_greet

User: Reverse the string "hello".
Output:
fn_reverse_string

User: Reverse "world".
Output:
fn_reverse_string

User: Flip the text "abcdef".
Output:
fn_reverse_string

User: Reverse this string: "Python".
Output:
fn_reverse_string

User: What is the square root of 16?
Output:
fn_square_root

User: Calculate the square root of 144.
Output:
fn_square_root

User: Find √81.
Output:
fn_square_root

User: What's the square root of 225?
Output:
fn_square_root

User: Replace all numbers in "Hello 34 I'm 233 years old" with "NUMBERS".
Output:
fn_replace_regex

User: Replace every vowel in "Programming is fun" with "*".
Output:
fn_replace_regex

User: Replace "cat" with "dog" in "The cat sat on the mat with another cat".
Output:
fn_replace_regex

User: Replace every space with "_".
Output:
fn_replace_regex

User: Replace all digits with "#".
Output:
fn_replace_regex

END OF EXAMPLES

User:
"""


generator = Generator(use_given_functions, use_given_prompts, main_prompt)
generator.start_model()

# print("Function names:", use_given_functions)
# print("Prompt names:", use_given_prompts)
