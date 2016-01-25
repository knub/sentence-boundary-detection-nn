import argparse
from preprocessing.word2vec_file import Word2VecFile
from sbd_classification.lexical_classification import LexicalClassifier
from sbd_classification.util import *

class FusionClassifier(object):
    def __init__(self, lexical_model_folder, audio_model_folder, word_vector):
        self.__init_lexical_classifier(lexical_model_folder, word_vector)
        self.__init_audio_classifier(audio_model_folder)

    def __init_lexical_classifier(self, folder, word_vector):
        self.lexical_classifier = load_lexical_classifier(folder, word_vector)

    def __init_audio_classifier(self, folder):
        self.audio_classifier = folder


################
# Example call #
################

def main(lexical, audio, vectorfile, debug):
    config_file, _, _ = get_filenames(lexical)
    sbd.SbdConfig(config_file)

    if debug:
        word_vector = None
    else:
        word_vector = Word2VecFile(vectorfile)

    fusion_classifier = FusionClassifier(lexical, audio, word_vector)

    # MASTERPLAN
    # read lexical files and model
    # read audio files and model
    # run both models
    # combine results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test fusion of two models', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--vectorfile', help='the google news word vector', default='demo_data/GoogleNews-vectors-negative300.bin', nargs='?')
    parser.add_argument('-l', '--lexical', help='folder with model, prototxt, and config', default='demo_data/lexical_models/20160108-072841_google_ted_wiki_window-8-4_pos-false_qm-false_balanced-false_nr-rep-true_word-this', nargs='?')
    parser.add_argument('-a', '--audio', help='folder with model, prototxt, and config', default='demo_data/lexical_models/20160108-032648_google_ted_wiki_window-5-4_pos-true_qm-false_balanced-false_nr-rep-true_word-this', nargs='?')
    parser.add_argument('-d', '--debug', help='do not use debug mode, google vector is read', action='store_true')
    args = parser.parse_args()

    main(args.lexical, args.audio, args.vectorfile, args.debug)
