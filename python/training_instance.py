import numpy
import WINDOW_SIZE from sliding_window

class TrainingInstance(object):

    def __init__(self, tokens, label):
        self.tokens = tokens
        self.label = label

    def __repr__(self):
        return "TOKENS: %s \nLABEL: %s \n" % (" ".join(map(unicode, self.tokens)), str(self.label))

    def get_array(self):
        dimensions = (1, WINDOW_SIZE, len(self.tokens[0].word_vec))
        arr = numpy.zeros(dimensions, float)
        for i in range(0, WINDOW_SIZE):
            arr[0][i] = self.tokens[i].word_vec
        return arr

    def get_label(self):
        return self.label.value
