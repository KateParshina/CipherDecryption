import nltk.data
from string import ascii_lowercase


PUNKT_DATA_PATH = "tokenizers/punkt/english.pickle"
try:
    nltk.data.find(PUNKT_DATA_PATH)
except LookupError:
    nltk.download(PUNKT_DATA_PATH)


class Preprocessor:
    def __init__(self):
        self.punkt_spliter = nltk.data.load(PUNKT_DATA_PATH)

    def document_to_sequences(self, text: str):
        sentences = self.punkt_spliter.tokenize(text)
        sequences = [self.sentence_to_sequences(s) for s in sentences]
        return sequences

    def sentence_to_sequences(self, sentence: str):
        sentence = sentence.lower()
        filtered_sentence = self.filter_not_alphabet(sentence)
        return [list(w) for w in filtered_sentence.split() if w]

    @staticmethod
    def filter_not_alphabet(text: str):
        new_text = ""

        for word in text.split():
            new_word = ""
            for ch in word:
                if ch in ascii_lowercase:
                    new_word += ch

            if new_word:
                new_text += f"{new_word} "

        return new_text.strip()
