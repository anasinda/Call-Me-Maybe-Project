from tokenizer import Tokenizer
from grammar import Grammar
from utils import State
import numpy as np
from llm_sdk import Small_LLM_Model

class Decoder():
    def __init__(self, grammar: Grammar, tokenizer: Tokenizer):
        self.grammar = grammar
        self.tokenizer = tokenizer

    def initiliaze_decoder(self, prompt: str):

        input_ids: list[int] = self.tokenizer.encode(prompt).squeeze().tolist()

        while self.grammar.current_state != State.END:
            select_token = None
            allowed_tokens = self.grammar.get_allowed_tokens()

            if allowed_tokens.literal is not None:
                select_token = allowed_tokens.literal
            elif allowed_tokens.choices is not None:
                select_token = allowed_tokens.choices
            elif allowed_tokens.usable_funcs is not None:
                select_token = allowed_tokens.usable_funcs
            elif allowed_tokens.value_type is not None:
                select_token = allowed_tokens.value_type


            select_token_id: list[int] = []
            logits = np.array(self.tokenizer.get_logits(input_ids))
            constrain_logits = np.full(len(logits), -np.inf)

            if allowed_tokens.check_attributes():
                for token in select_token:
                    ids = self.tokenizer.encode(token).squeeze().tolist()
                    if isinstance(ids, int):
                        select_token_id.append(ids)
                    else:
                        select_token_id.extend(ids)
            else:
                select_token_id = self.tokenizer.encode(select_token).squeeze().tolist()

            constrain_logits[select_token_id] = 0
            masked_logits = logits + constrain_logits
            best_token_id = np.argmax(masked_logits)
            input_ids.append(best_token_id)
            token_id_str = self.tokenizer.decode(best_token_id)
            self.grammar.consume(token_id_str)
