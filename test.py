from src.decoder import Decoder
from src.tokenizer import Tokenizer
from src.grammar import Grammar
from src.schema import Schema


schema = Schema("data/input/functions_definition.json")
func_defs = schema.create_schema()
grammar = Grammar(func_defs)
tokenizer = Tokenizer()
decoder = Decoder(grammar, tokenizer, func_defs)

prompt = f"""
You are an llm that returns a json structre statement.
# the statment has the json format, a "name": {func_defs}
# followed by the description for each function to get the context.
# and you MUST follow these instructions:
# name == {func_defs['fn_add_numbers'].name}
# description == {func_defs["fn_add_numbers"].description}.
# parameters == {func_defs['fn_add_numbers'].parameters}
Take the user prompt, use the above set of instructions to generate
a proper response.
When you see 'User:', anything after that is the prompt
Example:
User: Greet shrek
Response:
"name": fn_greet
"parameters" : a: number, b: number
IMPORTANT NOTES:
- number == anything from 0 to 9 and has a '-', '-' means it is a negative number
- string == generate anything you see fit based on the context and rules provided
- generate all paramters in consistent order
END OF PROMPT ON WHAT YOU DO


"""
user_prompt = "What is the sum of 2 and 3?"
generated_response = decoder.generate_first_json(prompt, user_prompt)
print(generated_response)
# input_ids, generated, remaining_candidates = decoder.initiliaze_decoder(prompt + "User: Reverse the string 'hello'")
# print("These are the input_ids", tokenizer.decode(input_ids))
# print("These are the generated", generated)
# print("These are the remaining candidates", remaining_candidates)
