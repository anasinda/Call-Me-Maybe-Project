from tokenizer import Tokenizer
from grammar import Grammar
from utils import State
import numpy as np
from llm_sdk import Small_LLM_Model

class Decoder():
    def __init__(self, grammar: Grammar, tokenizer: Tokenizer):
        self.grammar = grammar
        self.tokenizer = tokenizer
        self.

    def initiliaze_decoder(self, prompt: str):

        input_ids: list[int] = self.tokenizer.encode(prompt)

        while self.grammar.current_state != State.END:
            tokens_to_int: list[int] = []
            allowed_tokens = self.grammar.get_allowed_tokens()
            logits = np.array(self.tokenizer.get_logits(input_ids))
            constrain_logits = np.full(len(logits), -np.inf)

            for token in allowed_tokens.check_value_type():
                tokens_to_int.extend(self.tokenizer.encode(token))

            constrain_logits[tokens_to_int] = 0
            masked_logits = logits + constrain_logits
            best_token_id = np.argmax(masked_logits)
            input_ids.append(best_token_id)
            token_id_str = self.tokenizer.decode([best_token_id])
            self.grammar.consume(token_id_str)
