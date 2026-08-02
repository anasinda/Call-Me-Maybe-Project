from src.decoder import Decoder
from src.tokenizer import Tokenizer
from src.grammar import Grammar
from src.schema import Schema


schema = Schema("data/input/functions_definition.json")
func_defs = schema.create_schema()
grammar = Grammar(func_defs)
tokenizer = Tokenizer()
decoder = Decoder(grammar, tokenizer)

prompt = """
Available functions:

fn_add_numbers:
Add two numbers together and return their sum.

fn_greet:
Generate a greeting message for a person by name.

fn_reverse_string:
Reverse a string and return the reversed result.

fn_get_square_root:
Calculate the square root of a number.

fn_substitute_string_with_regex:
Replace all occurrences matching a regex pattern in a string.

User:
Greet john
""".strip()

input_ids, generated, remaining_candidates = decoder.initiliaze_decoder(prompt)
print("These are the input_ids", tokenizer.decode(input_ids))
print("These are the generated", generated)
print("These are the remaining candidates", remaining_candidates)
