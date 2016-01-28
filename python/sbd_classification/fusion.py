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
    def __init__(self):
        pass

    def read_lexical_config(self, punct_pos = None, window_size = None, pos_tagging = None):
        self.LEXICAL_PUNCTUATION_POS = sbd.config.getint('windowing', 'punctuation_position') if punct_pos == None else punct_pos
        self.LEXICAL_WINDOW_SIZE = sbd.config.getint('windowing', 'window_size')  if window_size == None else window_size
        self.POS_TAGGING = sbd.config.getboolean('features', 'pos_tagging') if pos_tagging == None else pos_tagging

    def read_audio_config(self, punct_pos = None, window_size = None):
        self.AUDIO_PUNCTUATION_POS = sbd.config.getint('windowing', 'punctuation_position') if punct_pos == None else punct_pos
        self.AUDIO_WINDOW_SIZE = sbd.config.getint('windowing', 'window_size')  if window_size == None else window_size

    def fuse(self, tokens, lexical_probs, audio_probs):
        # TODO:
        # Die Window-Size und Punctuation-Position vom Audio Model beruecksichtigen
        # Bessere Fusion einbauen!
        # Assertion is not correct!
        assert(len(lexical_probs) + self.LEXICAL_WINDOW_SIZE - 1 == len(audio_probs) + self.AUDIO_WINDOW_SIZE - 1)
        assert(len(tokens) == len(audio_probs) + self.AUDIO_WINDOW_SIZE - 1)

        fusion_probs = []
        for i in range(0, len(tokens)):
            lexic_pos = get_index(i, len(lexical_probs), self.LEXICAL_PUNCTUATION_POS)
            audio_pos = get_index(i, len(audio_probs), self.AUDIO_PUNCTUATION_POS)

            # if we have no predictions return NONE
            if lexic_pos < 0 and audio_pos < 0:
                fusion_probs.append([1.0, 0.0, 0.0])
                continue

            # if we have no audio prediction return lexical prediction
            if audio_pos < 0:
                fusion_probs.append(lexical_probs[lexic_pos])
                continue

            audio_none = audio_probs[audio_pos][0]
            audio_period = audio_probs[audio_pos][1]

            # if we have no lexical prediction return audio prediction
            if lexic_pos < 0:
                fusion_probs.append([audio_none, 0.0, audio_period])
                continue

            lexical_none = lexical_probs[lexic_pos][0]
            lexical_comma = lexical_probs[lexic_pos][1]
            lexical_period = lexical_probs[lexic_pos][2]

            # sophisticated fusion happening here
            threshold_audio = 0.5
            threshold_lexical = 0.8
            # if audio model predicts a period, and lexical is not very confident, that there is no period, use audio prediction
            if audio_period > threshold_audio and lexical_none < threshold_lexical:
                fusion_probs.append(norm_single([lexical_none, lexical_comma + audio_period, lexical_period + audio_period]))
            else:
                fusion_probs.append([lexical_none, lexical_comma, lexical_period])

        return tokens, fusion_probs

    def _debug(self):
        pass
        # print self.LEXICAL_PUNCTUATION_POS, self.POS_TAGGING
        # print self.AUDIO_PUNCTUATION_POS


################
# Example call #
################

def main():
    import random
    fc = Fusion()

    num_words = 12

    pos_lexic = 4
    size_lexic = 8
    pos_audio = 2
    size_audio = 4

    fc.read_lexical_config(pos_lexic, size_lexic, False)
    fc.read_audio_config(pos_audio, size_audio)

    tokens = ["test" + str(i) for i in range(1, 1 + num_words)]
    probs_lexic = [[random.random(), random.random(), random.random()] for i in range(0, num_words - size_lexic + 1)]
    probs_audio = [[random.random(), random.random()] for i in range(0, num_words - size_audio + 1)]

    probs_lexic = norm(probs_lexic)
    probs_audio = norm(probs_audio)

    print tokens, len(probs_lexic), len(probs_audio)
    print fc.fuse(tokens, probs_lexic, probs_audio)

if __name__ == '__main__':
    main()
