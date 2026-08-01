from src.tokenizer import Tokenizer
from src.grammar import Grammar
from src.utils import State
import numpy as np

class Decoder():
    def __init__(self, grammar: Grammar, tokenizer: Tokenizer):
        self.grammar = grammar
        self.tokenizer = tokenizer

    def initiliaze_decoder(self, prompt: str):

        input_ids: list[int] = self.tokenizer.encode(prompt)
        generated: list[int] = []
        remaining_candidates: list[list[int]] = []

        while self.grammar.current_state != State.END:
            logits = np.array(self.tokenizer.get_logits(input_ids))
            mask = np.full(len(logits), -np.inf)
            next_tokens: set[int] = set()
            if not remaining_candidates:
                allowed_tokens = self.grammar.get_allowed_tokens()

                for token in allowed_tokens.check_value_type():
                    remaining_candidates.append(self.tokenizer.encode(token))

            for token in remaining_candidates:
                if len(generated) < len(token):
                    next_tokens.add(token[len(generated)])

            mask[list(next_tokens)] = 0
            masked_logits = logits + mask
            best_token_id = np.argmax(masked_logits)
            input_ids.append(best_token_id)
            generated.append(best_token_id)

            new_remaining_canidates: list[list[int]] = []
            for token in remaining_candidates:
                if token[:len(generated)] == generated:
                    new_remaining_canidates.append(token)
            remaining_candidates = new_remaining_canidates

            if len(remaining_candidates) == 1:
                if remaining_candidates[0] == generated:
                    decode_remaining_canididate = self.tokenizer.decode(generated)
                    self.grammar.consume(decode_remaining_canididate)
                    generated.clear()
                    remaining_candidates.clear()

        return input_ids, generated, remaining_candidates
