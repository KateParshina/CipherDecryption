from argparse import ArgumentParser
from local_storage import load_text_file

parser = ArgumentParser(description='TRAIN PROCESS')
parser.add_argument('-t', metavar='-t', type=str, help='text to decrypt', required=False)
parser.add_argument('-d', metavar='-d', type=str, help='path to txt file to decrypt', required=False)
parser.add_argument('-m', metavar='-m', type=str, help='json file path to MC model', required=True)
args = parser.parse_args()


if __name__ == '__main__':
    if args.t:
        text_to_decrypt = args.t
    elif args.d:
        text_to_decrypt = load_text_file(args.d)
    else:
        raise "Input text is not provided"

    # RUN GENETIC ALGORITHM

    # LOG DECRYPTED TEXT
