import sys
sys.path.append("../python/")
import numpy, caffe
import json
from word2vec_file import Word2VecFile
from sliding_window import SlidingWindow
from nlp_pipeline import NlpPipeline, PosTag
from sbd_config import config

classes = ["NONE", "COMMA", "PERIOD"]

WINDOW_SIZE = config.getint('windowing', 'window_size')
PUNCTUATION_POS = config.getint('windowing', 'punctuation_position')
POS_TAGGING = config.getboolean('features', 'pos_tagging')

FEATURE_LENGTH = 300 if not POS_TAGGING else 300 + len(PosTag)

class InputText(object):

    def __init__(self, text):
        self.text = text

        self.nlp_pipeline = NlpPipeline()
        self.tokens = self.nlp_pipeline.parse_text(self.text)

    def get_tokens(self):
        return self.tokens


class Classifier(object):

    def __init__(self, net, word2vec, debug = False):
        self.word2vec = word2vec
        self.net = net
        self.debug = debug

    def predict_text(self, text):
        input_text = InputText(text)
        json_data = []

        for token in input_text.tokens:
            if not token.is_punctuation():
                if self.debug:
                    token.word_vec = numpy.zeros(300)
                else:
                    token.word_vec = self.word2vec.get_vector(token.word.lower())

        slidingWindow = SlidingWindow()
        instances = slidingWindow.list_windows(input_text)

        # get caffe predictions
        punctuation_probs = []
        for instance in instances:
            probs = self.predict_caffe(instance)
            punctuation_probs.append(probs)

        # build json
        for i, token in enumerate(input_text.tokens):
            token_json = {'type': 'word', 'token': token.word}
            if POS_TAGGING:
                token_json['pos'] = token.pos_tags
            json_data.append(token_json)

            # we are at the beginning or at the end of the text and do not have any predictions for punctuations
            if i < PUNCTUATION_POS - 1 or i > len(input_text.tokens) - PUNCTUATION_POS - 1:
                json_data.append({'type': 'punctuation', 'punctuation': 'NONE', 'pos': {'NONE': 1.0, 'COMMA': 0.0, 'PERIOD': 0.0}})
            else:
                current_punctuation = classes[numpy.argmax(punctuation_probs[i - PUNCTUATION_POS + 1])]
                class_distribution = self._get_class_distribution(punctuation_probs[i - PUNCTUATION_POS + 1])
                json_data.append({'type': 'punctuation', 'punctuation': current_punctuation, 'probs': class_distribution})

        return json_data

    def predict_caffe(self, instance):
        caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})

        batchsize = 1
        self.net.blobs['data'].reshape(batchsize,1, 5, FEATURE_LENGTH)
        reshaped_array = numpy.expand_dims(instance.get_array(), axis=0)

        self.net.blobs['data'].data[...] = reshaped_array

        out = self.net.forward()
        return out['softmax']

    def _get_class_distribution(self, probs):
        json_data = {}
        for i in range (0, len(classes)):
            json_data[classes[i]] = str(probs[0][i])
        return json_data

