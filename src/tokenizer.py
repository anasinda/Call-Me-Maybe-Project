from llm_sdk import Small_LLM_Model

class Tokenizer:
    def __init__(self, llm: Small_LLM_Model):
        self.llm = llm

    def encode(self, text: str):
        return self.llm.encode(text)

    def decode(self, ids):
        return self.llm.decode(ids)

    def vocab_path(self):
        return self.llm.get_path_to_vocab_file()

    def tokenizer_path(self):
        return self.llm.get_path_to_tokenizer_file()
