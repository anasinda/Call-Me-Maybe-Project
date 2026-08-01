from llm_sdk import Small_LLM_Model

llm = Small_LLM_Model()
print("This is add number", llm.encode("fn_add_numbers").squeeze().tolist())
print("This is greet",llm.encode("fn_greet").squeeze().tolist())
print("This is reverse str",llm.encode("fn_reverse_string").squeeze().tolist())
print("This is square root",llm.encode("fn_get_square_root").squeeze().tolist())
print("This is regex",llm.encode("fn_substitute_string_with_regex").squeeze().tolist())
