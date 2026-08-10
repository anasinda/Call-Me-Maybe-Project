from typing import Any, cast

from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]


class Tokenizer:
    def __init__(self) -> None:
        self.model: Any = Small_LLM_Model()

    def encode(self, text: str) -> list[int]:
        ids = self.model.encode(text).squeeze().tolist()

        if isinstance(ids, int):
            return [ids]
        return cast(list[int], ids)

    def decode(self, ids: list[int]) -> str:
        return cast(str, self.model.decode(ids))

    def get_logits(self, ids: list[int]) -> list[float]:
        logits = self.model.get_logits_from_input_ids(ids)
        return cast(list[float], logits)

    def vocab_file_path(self) -> str:
        return cast(str, self.model.get_path_to_vocab_file())

    def tokenizer_path(self) -> str:
        return cast(str, self.model.get_path_to_tokenizer_file())
