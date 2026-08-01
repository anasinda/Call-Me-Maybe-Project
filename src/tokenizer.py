from llm_sdk import Small_LLM_Model

class Tokenizer:
    def __init__(self):
        self.model = Small_LLM_Model()

    def encode(self, text):
        ids = self.model.encode(text).squeeze().tolist()

        if isinstance(ids, int):
            return [ids]
        return ids


    def decode(self, ids):
        return self.model.decode(ids)

    def get_logits(self, ids):
        return self.model.get_logits_from_input_ids(ids)

    def vocab_file_path(self):
        return self.model.get_path_to_vocab_file()

    def tokenizer_path(self):
        return self.model.get_path_to_tokenizer_file()

    def vocab_size(self) -> int:
        return self._tokenizer.vocab_size
