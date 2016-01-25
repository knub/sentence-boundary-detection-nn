import numpy, caffe, argparse
import common.sbd_config as sbd
from preprocessing.nlp_pipeline import NlpPipeline, PosTag
from preprocessing.sliding_window import SlidingWindow
from preprocessing.word2vec_file import Word2VecFile


class InputText(object):

    def __init__(self, text):
        self.text = text

        self.nlp_pipeline = NlpPipeline()
        self.tokens = self.nlp_pipeline.parse_text(self.text)

    def get_tokens(self):
        return self.tokens


class LexicalClassifier(object):

    def __init__(self, net, word2vec, debug = False):

        self.WINDOW_SIZE = sbd.config.getint('windowing', 'window_size')
        self.POS_TAGGING = sbd.config.getboolean('features', 'pos_tagging')

        self.FEATURE_LENGTH = 300 if not self.POS_TAGGING else 300 + len(PosTag)

        self.word2vec = word2vec
        self.net = net
        self.debug = debug

    def predict_text(self, text):
        input_text = InputText(text)

        for token in input_text.tokens:
            if not token.is_punctuation():
                if self.debug:
                    token.word_vec = numpy.random.rand(300)
                else:
                    token.word_vec = self.word2vec.get_vector(token.word.lower())

        sliding_window = SlidingWindow()
        instances = sliding_window.list_windows(input_text)

        # get caffe predictions
        punctuation_probs = []
        for instance in instances:
            probs = self.predict_caffe(instance)
            punctuation_probs.extend(numpy.copy(probs))

        return (input_text.tokens, punctuation_probs)

    def predict_caffe(self, instance):
        caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})

        # batchsize = 1
        # self.net.blobs['data'].reshape(batchsize, 1, self.WINDOW_SIZE, self.FEATURE_LENGTH)
        reshaped_array = numpy.expand_dims(instance.get_array(), axis=0)

        self.net.blobs['data'].data[...] = reshaped_array

        out = self.net.forward()
        return out['softmax']



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
