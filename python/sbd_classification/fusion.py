import argparse
from preprocessing.word2vec_file import Word2VecFile
from sbd_classification.lexical_classification import LexicalClassifier
from sbd_classification.util import *


def norm_single(probs):
    s = 0.0
    for p in probs:
        s += p
    for i in range(0, len(probs)):
        probs[i] = probs[i] / s
    return probs

def norm(probs_list):
    for probs in probs_list:
        norm_single(probs)
    return probs_list


class Fusion(object):

    def __init__(self, lexical_punctuation_pos, lexical_window_size, audio_punctuation_pos, audio_window_size):
        self.LEXICAL_PUNCTUATION_POS = lexical_punctuation_pos
        self.LEXICAL_WINDOW_SIZE = lexical_window_size
        self.AUDIO_PUNCTUATION_POS = audio_punctuation_pos
        self.AUDIO_WINDOW_SIZE = audio_window_size

        # constants for index access into the probability vectors
        self.AUDIO_NONE_IDX = 0
        self.AUDIO_PERIOD_IDX = 1
        self.LEX_NONE_IDX = 0
        self.LEX_COMMA_IDX = 1
        self.LEX_PERIOD_IDX = 2

    def fuse(self, tokens, lexical_probs, audio_probs):
        assert(len(lexical_probs) + self.LEXICAL_WINDOW_SIZE == len(audio_probs) + self.AUDIO_WINDOW_SIZE)
        assert(len(tokens) == len(audio_probs) + self.AUDIO_WINDOW_SIZE - 1)
        assert(len(tokens) == len(lexical_probs) + self.LEXICAL_WINDOW_SIZE - 1)

        fusion_probs = []
        for i in range(0, len(tokens)):
            lexical_pos = get_index(i, len(lexical_probs), self.LEXICAL_PUNCTUATION_POS)
            audio_pos = get_index(i, len(audio_probs), self.AUDIO_PUNCTUATION_POS)

            # if we have no predictions return NONE
            if lexical_pos < 0 and audio_pos < 0:
                fusion_probs.append([1.0, 0.0, 0.0])
                continue

            # if we have no audio prediction return lexical prediction
            if audio_pos < 0:
                fusion_probs.append(lexical_probs[lexical_pos])
                continue

            audio_none = audio_probs[audio_pos][self.AUDIO_NONE_IDX]
            audio_period = audio_probs[audio_pos][self.AUDIO_PERIOD_IDX]

            # if we have no lexical prediction return audio prediction
            if lexical_pos < 0:
                fusion_probs.append([audio_none, 0.0, audio_period])
                continue

            fusion_probs.append(self.sophisticated_fusion(lexical_probs, audio_probs))

    def sophisticated_fusion(self, lexical_probs, audio_probs):
        raise Exception("Abstract base class")

class ThresholdFusion(Fusion):

    def sophisticated_fusion(self, lexical_probs, audio_probs):
        threshold_audio = 0.5
        threshold_lexical = 0.8

        audio_none = audio_probs[audio_pos][self.AUDIO_NONE_IDX]
        audio_period = audio_probs[audio_pos][self.AUDIO_PERIOD_IDX]

        lexical_none = lexical_probs[lexical_pos][self.LEX_NONE_IDX]
        lexical_comma = lexical_probs[lexical_pos][self.LEX_COMMA_IDX]
        lexical_period = lexical_probs[lexical_pos][self.LEX_PERIOD_IDX]

        # if audio model predicts a period, and lexical is not very confident, that there is no period, use audio prediction
        if audio_period > threshold_audio and lexical_none < threshold_lexical:
            return norm_single([lexical_none, lexical_comma, lexical_period + audio_period])
        else:
            return [lexical_none, lexical_comma, lexical_period]

        return fusion_probs


################
# Example call #
################

def main():
    import random
    fc = Fusion()

    num_words = 12

    lexical_punctuation_pos = 4
    lexical_window_size = 8
    audio_punctuation_pos = 2
    audio_window_size = 4

    fc.read_lexical_config(lexical_punctuation_pos, lexical_window_size)
    fc.read_audio_config(audio_punctuation_pos, audio_window_size)

    tokens = ["test" + str(i) for i in range(1, 1 + num_words)]
    probs_lexic = [[random.random(), random.random(), random.random()] for i in range(0, num_words - lexical_window_size + 1)]
    probs_audio = [[random.random(), random.random()] for i in range(0, num_words - audio_window_size + 1)]

    probs_lexic = norm(probs_lexic)
    probs_audio = norm(probs_audio)

    print tokens, len(probs_lexic), len(probs_audio)
    print fc.fuse(tokens, probs_lexic, probs_audio)

if __name__ == '__main__':
    main()
