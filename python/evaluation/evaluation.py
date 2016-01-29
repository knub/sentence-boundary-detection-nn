import common.sbd_config as sbd
import argparse, os
from parsing.audio_parser import AudioParser
from sbd_classification.util import *
from sbd_classification.classification_input import InputText, InputAudio
from sbd_classification.fusion import ThresholdFusion

class Evaluation(object):

    def __init__(self, talks):
        self.talks = talks

    def evaluate(self, lexical_model_folder, audio_model_folder, vector):
        print("Evaluating %s and %s ..." % (lexical_model_folder, audio_model_folder))

        lexical_classifier = load_lexical_classifier(lexical_model_folder, vector)
        audio_classifier = load_audio_classifier(audio_model_folder)

        # get audio probabilities
        self._load_config(audio_model_folder)
        input_audio = InputAudio(self.talks)
        audio_probs = audio_classifier.predict(input_audio)

        # get lexical probabilities
        self._load_config(lexical_model_folder)
        input_text = InputText(self.talks)
        lexical_probs = lexical_classifier.predict(input_text)

        # get config parameter
        (lexical_window_size, lexical_punctuation_pos, pos_tagging) = lexical_classifier.get_lexical_parameter()
        (audio_window_size, audio_punctuation_pos) = audio_classifier.get_audio_parameter()

        # fusion
        fusion = ThresholdFusion(lexical_punctuation_pos, lexical_window_size, audio_punctuation_pos, audio_window_size)
        fusion_probs = fusion.fuse(len(input_text.tokens), lexical_probs, audio_probs)

        # evaluate
        print("Results:")

        print("Done.")

    def _load_config(self, model_folder):
        config_file, caffemodel_file, net_proto = get_filenames(model_folder)
        sbd.SbdConfig(config_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='evaluates the fusion.')
    parser.add_argument('ctm_file', help="path to ctm_file", default="evaluation_data/data/tst2011_0.ctm", nargs='?')
    parser.add_argument('audio_model_folder', help="path to audio models", default="evaluation_data/audio_models", nargs='?')
    parser.add_argument('vectorfile', help='the google news word vector', default='demo_data/GoogleNews-vectors-negative300.bin', nargs='?')
    parser.add_argument('lexical_model_folder', help="path to lexical models", default="evaluation_data/lexical_models", nargs='?')
    args = parser.parse_args()

    # get all talks
    print("Reading all talks ...")
    audio_parser = AudioParser()
    talks = audio_parser.parse(args.ctm_file)

    # get all lexical models
    lexical_models = []
    for dirname, dirnames, filenames in os.walk(args.lexical_model_folder):
        for subdirname in dirnames:
            lexical_models.append(os.path.join(dirname, subdirname))

    # get all audio models
    audio_models = []
    for dirname, dirnames, filenames in os.walk(args.audio_model_folder):
        for subdirname in dirnames:
            audio_models.append(os.path.join(dirname, subdirname))

    # evaluate all combination of models
    evaluation = Evaluation(talks)
    for lexical_model in lexical_models:
        for audio_model in audio_models:
            evaluation.evaluate(lexical_model, audio_model, None)

