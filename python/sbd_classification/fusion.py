import argparse
from preprocessing.word2vec_file import Word2VecFile
from sbd_classification.lexical_classification import LexicalClassifier
from sbd_classification.util import *

class FusionClassifier(object):
    def __init__(self):
        pass

    def read_lexical_config(self, punctuation_pos = None, pos_tagging = None):
        self.LEXICAL_PUNCTUATION_POS = sbd.config.getint('windowing', 'punctuation_position') if punctuation_pos == None else punctuation_pos
        self.POS_TAGGING = sbd.config.getboolean('features', 'pos_tagging') if pos_tagging == None else pos_tagging

    def read_audio_config(self, punctuation_pos = None):
        self.AUDIO_PUNCTUATION_POS = sbd.config.getint('windowing', 'punctuation_position') if punctuation_pos == None else punctuation_pos

    def fuse(self, tokens, lex_punctuations_probs, au_punctuations_probs):
        print tokens, lex_punctuations_probs, au_punctuations_probs

    def _debug(self):
        print self.LEXICAL_PUNCTUATION_POS, self.POS_TAGGING
        print self.AUDIO_PUNCTUATION_POS


################
# Example call #
################

def norm(probs_list):
    for probs in probs_list:
        s = 0.0
        for p in probs:
            s += p
        for i in range(0, len(probs)):
            probs[i] = probs[i] / s
    return probs_list

def main():
    import random
    fc = FusionClassifier()

    pos_lexic = 4
    pos_audio = 1

    fc.read_lexical_config(pos_lexic, False)
    fc.read_audio_config(pos_audio)

    tokens = ["test" + str(i) for i in range(0,12)]
    probs_lexic = [[random.random(), random.random(), random.random()] for i in range(0, 7)]
    probs_audio = [[random.random(), random.random()] for i in range(0, 10)]

    probs_lexic = norm(probs_lexic)
    probs_audio = norm(probs_lexic)

    fc.fuse(tokens, probs_lexic, probs_audio)

if __name__ == '__main__':
    main()
