from sbd_classification.lexical_classification import LexicalClassifier
from sbd_classification.util import *

class FusionClassifier(object):
    def __init__(self):
        pass

################
# Example call #
################

def main(lexical, audio):
    # read lexical files and model

    # read audio files and model

    # run both models

    # combine results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test fusion of two models')
    parser.add_argument('-l', '--lexical', help='folder with model, prototxt, and config', default='models/20160108-072841_google_ted_wiki_window-8-4_pos-false_qm-false_balanced-false_nr-rep-true_word-this', nargs='?')
    parser.add_argument('-a', '--audio', help='folder with model, prototxt, and config', default='models/20160108-032648_google_ted_wiki_window-5-4_pos-true_qm-false_balanced-false_nr-rep-true_word-this', nargs='?')
    args = parser.parse_args()

    main(args.lexical, args.audio)
