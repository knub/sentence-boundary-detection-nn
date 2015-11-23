import numpy
#import sliding_window
from nlp_pipeline import PosTag
import config

WINDOW_SIZE = 5
POS_TAGGING = config.get_boolean('features', 'pos_tagging')

class TrainingInstance(object):

    def __init__(self, tokens, label):
        self.tokens = tokens
        self.label = label

    def __repr__(self):
        return "TOKENS: %s \nLABEL: %s \n" % (" ".join(map(unicode, self.tokens)), str(self.label))

    def get_array(self):
        word_vec_size = len(self.tokens[0].word_vec)
        feature_size = word_vec_size

        if POS_TAGGING:
            feature_size += len(PosTag)

        dimensions = (1, WINDOW_SIZE, feature_size)
        arr = numpy.zeros(dimensions, float)

        for i in range(0, WINDOW_SIZE):
            arr[0][i][0:word_vec_size] = self.tokens[i].word_vec

            if POS_TAGGING:
                for pos_tag in self.tokens[i].pos_tags:
                    arr[0][i][word_vec_size + pos_tag.value] = 1.0

        return arr

    def get_label(self):
        return self.label.value
