from grammar import Grammar
from llm_sdk import Small_LLM_Model

class Tokenizer:
    def __init__(self):
        self.model = Small_LLM_Model()

    def encode(self, text):
        return self.model.encode(text)


    def decode(self, ids):
        return self.model.decode(ids)

    def token_to_id(self, token):
        return self.model.encode(token).squeeze().tolist()

    def get_logits(self, ids):
        return self.model.get_logits_from_input_ids(ids)

    def vocab_file_path(self):
        return self.model.get_path_to_vocab_file()
