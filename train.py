from argparse import ArgumentParser
from markov_chain import MarkovChain
from preprocessing import Preprocessor
from local_storage import load_text_file


parser = ArgumentParser(description='TRAIN PROCESS')
parser.add_argument('-d', metavar='-d', type=str, help='path to txt file with dataset', required=True)
parser.add_argument('-m', metavar='-m', type=str, help='json file path for model generation', default="markov_chain.json")
args = parser.parse_args()
MARKOV_DEEP_LEVEL = 6


if __name__ == '__main__':
    model_path = args.m
    dataset_path = args.d

    # LOAD TXT FILE DATASET
    text = load_text_file(dataset_path)

    # CREATE SEQUENCES FROM TEXT FILE
    preprocessor = Preprocessor()
    sequences = preprocessor.sentence_to_sequences(text)

    # TRAIN MARKOV CHAIN MODEL AND SAVE TO LOCAL STORAGE
    markov_model = MarkovChain(levels=MARKOV_DEEP_LEVEL)
    markov_model.train(sequences, save_path=model_path)
