import numpy, caffe, argparse
import common.sbd_config as sbd
from preprocessing.nlp_pipeline import NlpPipeline, PosTag
from preprocessing.sliding_window import SlidingWindow
from preprocessing.word2vec_file import Word2VecFile


class InputAudio(object):

    def __init__(self, audio_tokens):
        self.audio_tokens = audio_tokens

    def get_tokens(self):
        return self.audio_tokens


class AudioClassifier(object):

    def __init__(self, net, debug = False):
        self.classes = ["NONE", "PERIOD"]

        self.WINDOW_SIZE = sbd.config.getint('windowing', 'window_size')
        self.PUNCTUATION_POS = sbd.config.getint('windowing', 'punctuation_position')

        self.net = net
        self.debug = debug

    def predict_audio(self, audio_parser):
        audio = audio_parser.get_input_audio()

        sliding_window = SlidingWindow()
        instances = sliding_window.list_windows(audio)

        # get caffe predictions
        punctuation_probs = []
        for instance in instances:
            probs = self.predict_caffe(instance)
            punctuation_probs.extend(numpy.copy(probs))

        # build json
        for i, token in enumerate(input_text.tokens):
            token_json = {'type': 'word', 'token': token.word}
            if self.POS_TAGGING:
                token_json['pos'] = [str(tag).replace("PosTag.", "") for tag in token.pos_tags]
            json_data.append(token_json)

            # we are at the beginning or at the end of the text and do not have any predictions for punctuations
            current_prediction_position = i - self.PUNCTUATION_POS + 1
            if 0 <= current_prediction_position and current_prediction_position < len(punctuation_probs):
                current_punctuation = self.classes[numpy.argmax(punctuation_probs[current_prediction_position])]
                class_distribution = self._get_class_distribution(punctuation_probs[current_prediction_position])
                json_data.append({'type': 'punctuation', 'punctuation': current_punctuation, 'probs': class_distribution})
            else:
                json_data.append({'type': 'punctuation', 'punctuation': 'NONE', 'probs': {'NONE': 1.0, 'COMMA': 0.0, 'PERIOD': 0.0}})

        return json_data

    def predict_caffe(self, instance):
        caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})

        # batchsize = 1
        # self.net.blobs['data'].reshape(batchsize, 1, self.WINDOW_SIZE, self.FEATURE_LENGTH)
        reshaped_array = numpy.expand_dims(instance.get_array(), axis=0)

        self.net.blobs['data'].data[...] = reshaped_array

        out = self.net.forward()
        return out['softmax']

    def _get_class_distribution(self, probs):
        json_data = {}
        for i in range (0, len(self.classes)):
            json_data[self.classes[i]] = str(probs[i])
        return json_data



################
# Example call #
################

def main(caffeproto, caffemodel):
    net = caffe.Net(caffeproto, caffemodel, caffe.TEST)
    classifier = AudioClassifier(net, None, True)

    text = "This is a very long text This text has two sentences"
    data = classifier.predict_text(text)
    print(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run the web demo')
    parser.add_argument('caffeproto', help='the deploy prototxt of your trained model', default='models/deploy.prototxt', nargs='?')
    parser.add_argument('caffemodel', help='the trained caffemodel', default='models/model.caffemodel', nargs='?')
    args = parser.parse_args()

    main(args.caffeproto, args.caffemodel)
