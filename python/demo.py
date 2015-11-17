import argparse, numpy, caffe
from word2vec_file import Word2VecFile
from sliding_window import SlidingWindow, PUNCTUATION_POS
from nlp_pipeline import NlpPipeline
from talk_parser import Sentence

classes = ["NONE", "COMMA", "PERIOD", "QUESTION"]
classes_as_string = ["", ",", ".", "?"]

class InputText(object):

    def __init__(self, text):
        self.text = text

        self.nlp_pipeline = NlpPipeline()
        self.gold_tokens = self.nlp_pipeline.parse_text(self.text)

    def get_gold_tokens(self):
        return self.gold_tokens


class Demo(object):
    """parses demo data, feeds to a trained model and returns predictions"""

    def __init__(self, net, word2vec):
        self.word2vec = word2vec
        self.net = net

    def get_not_covered_words(self):
        return self.word2vec.not_covered_words

    def predict_text(self, text):
        input_text = InputText(text)

        for token in input_text.gold_tokens:
            if not token.is_punctuation():
                token.word_vec = self.word2vec.get_vector(token.word.lower())

        slidingWindow = SlidingWindow()
        instances = slidingWindow.list_windows(input_text)

        punctuations = []
        for instance in instances:
            probs = self.predict_caffe(instance)
            #print instance
            #self.show_probs(probs)
            punctuations.append(numpy.argmax(probs))
        #print punctuations

        print(">>> Sentence with boundaries:")
        for i in range(len(punctuations) - 1, -1, -1):
            input_text.gold_tokens.insert(i + PUNCTUATION_POS, classes_as_string[punctuations[i]])
        print "{",
        for t in input_text.gold_tokens:
            print t,
        print "}"

    def predict_caffe(self, instance):
        transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})

        batchsize = 1
        self.net.blobs['data'].reshape(batchsize,1,5,300)
        reshaped_array = numpy.expand_dims(instance.get_array(), axis=0)

        self.net.blobs['data'].data[...] = reshaped_array

        out = self.net.forward()
        return out['softmax']

    def show_probs(self, probs):
        for i in range (0, len(classes)):
            print classes[i], ":", probs[0][i]


def main_no_loading(net, vector, datafile, show):
    if show:
        classes_as_string[0] = "_"
    caffe.set_mode_cpu()
    d = Demo(net, vector)
    if datafile:
        f = open(datafile)
        text = f.read()
        f.close()
        d.predict_text(text)
    else:
        while (1):
            text = raw_input("Please enter some text without punctuation for prediction (enter q to quit):")
            if text == "q":
                return
            d.predict_text(text)    

def main(vectorfile, caffeproto, caffemodel, datafile=None, show=False):
    vector = Word2VecFile(vectorfile)
    net = caffe.Net(caffeproto, caffemodel, caffe.TEST)
    main_no_loading(net, vector, datafile, show)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get word vector from binary data.')
    parser.add_argument('-d','--datafile', help='path to file with text, if not present text can be entered interactively', dest=datafile)
    parser.add_argument('vectorfile', help='path to word vector binary')
    parser.add_argument('caffeproto', help='path to caffe proto file')
    parser.add_argument('caffemodel', help='path to caffe model file')
    parser.add_argument('-s','--show', help='show the non-existing punctuation with and underscore', action=store_true, dest=show)
    args = parser.parse_args()
    main(show=args.show, vectorfile=args.vectorfile, caffeproto=args.caffeproto, caffemodel=args.caffemodel, datafile=args.datafile)
