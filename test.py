# # from llm_sdk import Small_LLM_Model

# # llm = Small_LLM_Model()
# # print("This is add number", llm.encode("fn_add_numbers").squeeze().tolist())
# # print("This is greet",llm.encode("fn_greet").squeeze().tolist())
# # print("This is reverse str",llm.encode("fn_reverse_string").squeeze().tolist())
# # print("This is square root",llm.encode("fn_get_square_root").squeeze().tolist())
# # print("This is regex",llm.encode("fn_substitute_string_with_regex").squeeze().tolist())


# arrays = [[41, 42, 43], [51, 52, 53], [61, 62, 63]]

# for array in arrays:
#     print(array[:0])

# ex = {1, 2}
# e = {3, 4}
# exx = []

# exx.append(ex)
# exx.append(e)
# print(exx

from src.decoder import Decoder
from src.tokenizer import Tokenizer
from src.grammar import Grammar
from src.schema import Schema


schema = Schema("data/input/functions_definition.json")
func_defs = schema.create_schema()
grammar = Grammar(func_defs)
tokenizer = Tokenizer()
decoder = Decoder(grammar, tokenizer)

input_ids, generated, remaining_candidates = decoder.initiliaze_decoder("Available functions:
                                                                        fn_add_numbers:
                                                                        Add two numbers.
                                                                        fn_greet:
                                                                        Generate a greeting.
                                                                        fn_reverse_string:
                                                                        Reverse a string.
                                                                        fn_get_square_root:
                                                                        Calculate the square root.
                                                                        fn_substitute_string_with_regex:
                                                                        Replace regex matches.
                                                                        User:
                                                                        What is the sum of 2 and 3?")
print("These are the input_ids", tokenizer.decode(input_ids))
print("These are the generated", generated)
print("These are the remaining candidates", remaining_candidates)
