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

    def __init__(self, net, word2vec):
        self.word2vec = word2vec
        self.net = net
        self.json_data = []

    def predict_text(self, text):
        input_text = InputText(text)

        for token in input_text.tokens:
            if not token.is_punctuation():
                token.word_vec = self.word2vec.get_vector(token.word.lower())

        slidingWindow = SlidingWindow()
        instances = slidingWindow.list_windows(input_text)

        index = 1
        for instance in instances:
            probs = self.predict_caffe(instance)
            instance_tokens = instance.get_tokens()

            for i in range(len(instance_tokens)):
                token_json = {'type': 'word', 'token': instance_tokens[i].word}
                if POS_TAGGING:
                    token_json['pos'] = instance_tokens[i].pos_tags
                self.json_data[0].append(token_json)

                # we are at the beginning or at the end of the text and do not have any predictions for punctuations
                if index < PUNCTUATION_POS or index > len(input_text.tokens) - (WINDOW_SIZE - PUNCTUATION_POS):
                    self.json_data[0].append({'type': 'punctuation', 'punctuation': 'NONE', 'pos': {'NONE': 1.0, 'COMMA': 0.0, 'PERIOD': 0.0}})
                else:
                    current_punctuation = classes[numpy.argmax(probs)]
                    class_distribution = self._get_class_distribution(probs)
                    self.json_data[0].append({'type': 'punctuation', 'punctuation': current_punctuation, 'probs': class_distribution})

            index += 1

        return json.dumps(self.json_data)

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
            json_data[classes[i]] = probs[0][i]
        return json_data

