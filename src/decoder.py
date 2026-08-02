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

            if self.grammar.current_state == State.EXPECT_PARAMETERS_VALUE:
                allowed_tokens = self.grammar.get_allowed_tokens()
                if allowed_tokens.value_type == "number":
                    gen_num = self.generate_numbers(logits, mask, input_ids)
                    self.grammar.consume(gen_num)
                    continue
            elif not remaining_candidates:
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


    def generate_numbers(self, logits, mask, input_ids: list[int]):
        best_token_num: str = ""
        generated_param: str = ""
        possible_token: list[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"]
        possible_token_ids: list[int] = []

        for token in possible_token:
            possible_token_ids.append(self.tokenizer.encode(token))

        while True:
            mask[possible_token_ids] = 0
            masked_num_logits = logits + mask
            best_token_num_id = np.argmax(masked_num_logits)
            best_token_num = self.tokenizer.decode(best_token_num_id)
            if best_token_num in possible_token:
                input_ids.append(best_token_num_id)
                generated_param += best_token_num
            else:
                break




