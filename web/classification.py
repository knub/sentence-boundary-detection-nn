import sys
sys.path.append("../python/")
import numpy, caffe
import json
from word2vec_file import Word2VecFile
from sliding_window import SlidingWindow, PUNCTUATION_POS
from nlp_pipeline import NlpPipeline

classes = ["NONE", "COMMA", "PERIOD"]
classes_as_string = ["", ",", "."]

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

        punctuations = []
        for instance in instances:
            probs = self.predict_caffe(instance)
            punctuations.append(numpy.argmax(probs))

        for i in range(len(punctuations) - 1, -1, -1):
            input_text.tokens.insert(i + PUNCTUATION_POS, classes_as_string[punctuations[i]])

        punctuated_text = ""
        for t in input_text.tokens:
            punctuated_text += t

        self.json_data[0]['text'] = punctuated_text

        return json.dumps(self.json_data)

    def predict_caffe(self, instance):
        caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})

        batchsize = 1
        self.net.blobs['data'].reshape(batchsize,1,5,300)
        reshaped_array = numpy.expand_dims(instance.get_array(), axis=0)

        self.net.blobs['data'].data[...] = reshaped_array

        out = self.net.forward()
        return out['softmax']

