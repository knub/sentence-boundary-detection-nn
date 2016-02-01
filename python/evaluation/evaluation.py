import common.sbd_config as sbd
import argparse, os
from parsing.audio_parser import AudioParser
from sbd_classification.util import *
from sbd_classification.classification_input import InputText, InputAudio
from sbd_classification.fusion import get_evaluation_fusion_list
from preprocessing.word2vec_file import Word2VecFile

from sklearn.metrics import precision_recall_fscore_support

class Evaluation(object):

    def __init__(self, talks):
        self.talks = talks
        self.tokens = [token for talk in self.talks for token in talk.get_tokens()]

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

        fusions = get_evaluation_fusion_list(lexical_punctuation_pos, lexical_window_size, audio_punctuation_pos, audio_window_size)

        assert(len(input_audio.tokens) == len(input_text.tokens))
        for fusion in fusions:
            print str(fusion)
            fusion_probs = fusion.fuse(len(input_audio.tokens), lexical_probs, audio_probs)

            exp_actual = self.get_expected_actual(fusion_probs, self.tokens)
            self.calculate_evaluation_metrics(exp_actual)

    def get_expected_actual(self, fusion_probs, tokens):
        expected_actual = []
        word_tokens = [token for token in tokens if not token.is_punctuation()]

        assert(len(word_tokens) == len(fusion_probs))
        tokens_idx = 1
        for i in range(len(fusion_probs)):
            actual = fusion_probs[i].index(max(fusion_probs[i]))
            is_punctuation = tokens[tokens_idx].is_punctuation()
            expected = tokens[tokens_idx].punctuation_type.value if is_punctuation else 0
            if is_punctuation:
                tokens_idx += 1
            tokens_idx += 1
            expected_actual.append((expected, actual))

        return expected_actual

    def calculate_evaluation_metrics(self, expected_actual):
        expected = map(lambda x: x[0], expected_actual)
        actual = map(lambda x: x[1], expected_actual)
        results = precision_recall_fscore_support(expected, actual)
        print results


    def _load_config(self, model_folder):
        config_file, caffemodel_file, net_proto = get_filenames(model_folder)
        sbd.SbdConfig(config_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='evaluates the fusion.')
    parser.add_argument('ctm_file', help="path to ctm_file", default="evaluation_data/data/tst2011_0.ctm", nargs='?')
    parser.add_argument('vectorfile', help='the google news word vector', default='evaluation_data/GoogleNews-vectors-negative300.bin', nargs='?')
    parser.add_argument('lexical_model_folder', help="path to lexical models", default="evaluation_data/lexical_models", nargs='?')
    parser.add_argument('audio_model_folder', help="path to audio models", default="evaluation_data/audio_models", nargs='?')
    parser.add_argument('--release', help="whether to test in release mode", action='store_true')
    args = parser.parse_args()

    if args.release:
        vector = Word2VecFile(args.vectorfile)
    else:
        vector = None

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
            evaluation.evaluate(lexical_model, audio_model, vector)

