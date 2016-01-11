import numpy

import common.sbd_config as sbd
from nlp_pipeline import PosTag
from tokens import Punctuation, AudioToken


class TrainingInstance(object):

    def __init__(self, tokens, label):
        self.WINDOW_SIZE = sbd.config.getint('windowing', 'window_size')
        self.POS_TAGGING = sbd.config.getboolean('features', 'pos_tagging')
        self.USE_QUESTION_MARK = sbd.config.getboolean('features', 'use_question_mark')

        self.tokens = tokens
        self.label = label

    def __repr__(self):
        return "TOKENS: %s \nLABEL: %s \n" % (" ".join(map(unicode, self.tokens)), str(self.label))

    def get_array(self):
        if isinstance(self.tokens[0], AudioToken):
            return self.get_audio_array()
        else:
            return self.get_lexical_array()

    def get_lexical_array(self):
        word_vec_size = len(self.tokens[0].word_vec)
        feature_size = word_vec_size

        if self.POS_TAGGING:
            feature_size += len(PosTag)

        dimensions = (1, self.WINDOW_SIZE, feature_size)
        arr = numpy.zeros(dimensions, float)

        for i in range(0, self.WINDOW_SIZE):
            arr[0][i][0:word_vec_size] = self.tokens[i].word_vec

            if self.POS_TAGGING:
                for pos_tag in self.tokens[i].pos_tags:
                    arr[0][i][word_vec_size + pos_tag.value] = 1.0

        return arr

    def get_audio_array(self):
        feature_size = 4

        dimensions = (1, self.WINDOW_SIZE, feature_size)
        arr = numpy.zeros(dimensions, float)

        for i in range(0, self.WINDOW_SIZE):
            arr[0][i][0] = self.tokens[i].pause_before
            arr[0][i][1] = self.tokens[i].pause_after
            arr[0][i][2] = self.tokens[i].pause_energy
            arr[0][i][3] = self.tokens[i].pause_pitch

        return arr

    def get_label(self):
        if not self.USE_QUESTION_MARK and self.label == Punctuation.QUESTION:
            return Punctuation.PERIOD.value
        return self.label.value

    def get_tokens(self):
        return self.tokens
