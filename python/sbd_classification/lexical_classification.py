import numpy, caffe, argparse
import common.sbd_config as sbd
from preprocessing.nlp_pipeline import NlpPipeline, PosTag
from preprocessing.sliding_window import SlidingWindow
from preprocessing.word2vec_file import Word2VecFile
from classification_input import InputText
from abstract_classification import AbstractClassifier


class LexicalClassifier(AbstractClassifier):

    def __init__(self, net, word2vec):

        self.WINDOW_SIZE = sbd.config.getint('windowing', 'window_size')
        self.PUNCTUATION_POS = sbd.config.getint('windowing', 'punctuation_position')
        self.POS_TAGGING = sbd.config.getboolean('features', 'pos_tagging')

        self.FEATURE_LENGTH = 300 if not self.POS_TAGGING else 300 + len(PosTag)

        self.word2vec = word2vec
        self.net = net

    def predict(self, input_text):
        for token in input_text.tokens:
            if not token.is_punctuation():
                if not self.word2vec:
                    token.word_vec = numpy.random.rand(300)
                else:
                    token.word_vec = self.word2vec.get_vector(token.word.lower())

        sliding_window = SlidingWindow()
        instances = sliding_window.list_windows(input_text)

        return self._predict_caffe(instances)

    def get_lexical_parameter(self):
        return (self.WINDOW_SIZE, self.PUNCTUATION_POS, self.POS_TAGGING)

################
# Example call #
################

def main(caffeproto, caffemodel):
    net = caffe.Net(caffeproto, caffemodel, caffe.TEST)
    classifier = LexicalClassifier(net, None, True)

    text = "This is a very long text This text has two sentences"
    data = classifier.predict_text(text)
    print(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run the web demo')
    parser.add_argument('caffeproto', help='the deploy prototxt of your trained model', default='models/deploy.prototxt', nargs='?')
    parser.add_argument('caffemodel', help='the trained caffemodel', default='models/model.caffemodel', nargs='?')
    args = parser.parse_args()

    main(args.caffeproto, args.caffemodel)
