import local_storage as local

from math import log
from typing import List


class MarkovChain:
    def __init__(self, levels: int = 1, unknown_token: str = "", model=None):
        self.levels = levels
        self.grams = {}

        if model:
            self.grams = local.load_json_file(model)

        self.unknown_token = unknown_token

    def train(self, document: List[List[int | str]], save_path=None):
        if not document:
            raise "Define input document dataset"

        grams = {}

        tokens_set = list(set(token for sequence in document for token in sequence))
        tokens_set.append(self.unknown_token)
        pi_vector = {t: 1 for t in tokens_set}

        for sequence in document:
            first_token = sequence[0]
            pi_vector[first_token] += 1
        grams[0] = {"": pi_vector}

        sum_pi_values = sum([v for v in pi_vector.values()])
        for token in pi_vector:
            pi_vector[token] = pi_vector[token] / sum_pi_values

        for level in range(1, self.levels + 1):
            gram_matrix = {self.unknown_token: {t: 1 / len(tokens_set) for t in tokens_set}}
            for sequence in document:
                start = 0
                while True:
                    end = start + level
                    if end > len(sequence) - 1:
                        break

                    token = "".join(sequence[start:end])

                    if token not in gram_matrix:
                        gram_matrix[token] = {character: 1 for character in tokens_set}
                        # gram_matrix[token][self.unknown_token] = 1

                    next_token = sequence[end]
                    if next_token not in gram_matrix[token]:
                        gram_matrix[token][next_token] = 0

                    gram_matrix[token][next_token] += 1
                    start += 1

            for parent_token, next_tokens in gram_matrix.items():
                parent_token_count = sum(next_tokens.values())
                gram_matrix[parent_token] = {t: (c + 1) / (len(next_tokens) + parent_token_count) for t, c in
                                             next_tokens.items()}

            grams[level] = gram_matrix

        self.grams = grams

        if save_path:
            local.save_json_file(grams, save_path)

    def get_score(self, sequence: List[int | str], levels: int = 4):
        required_levels = range(levels + 1)

        for required_level in required_levels:
            if required_level not in self.grams:
                raise f"Level {required_level} does not exist in {self.grams.keys()}"

        score = 0
        first_pi_token = sequence[0]
        pi_gram = self.grams[0][self.unknown_token]
        if first_pi_token not in pi_gram:
            first_pi_token = self.unknown_token
        pi_token_proba = pi_gram[first_pi_token]
        score += log(pi_token_proba)

        for level in required_levels[1:]:
            start = 0
            while True:
                end = start + level
                if end > len(sequence) - 1:
                    break

                first_m_token_sequence = sequence[start: end]
                first_m_token = "".join(first_m_token_sequence)
                if first_m_token not in self.grams[level]:
                    first_m_token = self.unknown_token
                next_m_token = sequence[end]
                if next_m_token not in self.grams[level][first_m_token]:
                    next_m_token = self.unknown_token

                next_token_proba = self.grams[level][first_m_token][next_m_token]
                score += log(next_token_proba)
                start += 1

        return score
