import numpy, caffe, argparse
import common.sbd_config as sbd
from preprocessing.nlp_pipeline import NlpPipeline, PosTag
from preprocessing.sliding_window import SlidingWindow
from preprocessing.word2vec_file import Word2VecFile
from parsing.audio_parser import AudioParser
from classification_input import InputAudio
from abstract_classification import AbstractClassifier


class AudioClassifier(AbstractClassifier):

    def __init__(self, net, debug = False):
        self.classes = ["NONE", "PERIOD"]

        self.WINDOW_SIZE = sbd.config.getint('windowing', 'window_size')
        self.PUNCTUATION_POS = sbd.config.getint('windowing', 'punctuation_position')

        self.net = net
        self.debug = debug

    def predict(self, input_audio):
        sliding_window = SlidingWindow()
        instances = sliding_window.list_windows(input_audio)

        return self._predict_caffe(instances)

    def get_audio_parameter(self):
        return (self.WINDOW_SIZE, self.PUNCTUATION_POS)

################
# Example call #
################

def main(model_folder, example_folder):
    config_file, caffemodel_file, net_proto = get_filenames(model_folder)
    sbd.SbdConfig(config_file)
    ctm_file, pitch_file, energy_file = get_audio_files(example_folder)

    # parse ctm_file, pitch_file and energy_file
    parser = AudioParser(ctm_file, pitch_file, energy_file)
    parser.parse()

    classifier = load_audio_classifier(model_folder)

    data = classifier.predict_audio(parser)
    print(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run the web demo')
    parser.add_argument('model_folder', help='the trained caffemodel', default='demo_data/audio_models/audio_window-1-1/', nargs='?')
    parser.add_argument('example_folder', help='folder containing the ctm, pitch and energy files', default='demo_data/audio_examples/tst2011_talkid1169/', nargs='?')
    args = parser.parse_args()

    main(args.model_folder, args.example_folder)
