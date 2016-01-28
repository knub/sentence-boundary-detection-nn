
class Evaluation(object):

    def __init__(self, talks):
        self.talks = talks

    def evaluate(lexical_model_folder, audio_model_folder, vector):
        lexical_classifier = load_lexical_classifier(lexical_model_folder, vector)
        audio_classifier = load_audio_classifier(audio_model_folder)

        # get audio probabilities
        self._load_config(audio_model_folder)
        (tokens, audio_probs) = audio_classifier.predict(InputAudio(self.talks))

        # get lexical probabilities
        self._load_config(lexical_model_folder)
        (tokens, lexical_probs) = lexical_classifier.predict(InputText(self.talks))

        # get config parameter
        (lexical_window_size, lexical_punctuation_pos, pos_tagging) = lexical_classifier.get_lexical_parameter()
        (audio_window_size, audio_punctuation_pos) = audio_classifier.get_audio_parameter()

        # fusion
        fusion = Fusion(lexical_punctuation_pos, lexical_window_size, audio_punctuation_pos, audio_window_size)
        fusion_probs = fusion.fuse(tokens, lexical_probs, audio_probs)

        # evaluate
        # TODO

    def _load_config(model_folder):
        config_folder, caffemodel_file, net_proto = get_filenames(model_folder)
        sbd.SbdConfig(config_file)


def get_talks(data_folder):
    # TODO
    # read all test talks in folder and put them into a list
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='evaluates the fusion.')
    parser.add_argument('data_root_folder', help="path to data")
    parser.add_argument('audio_model_root_folder', help="path to audio models")
    parser.add_argument('lexical_model_root_folder', help="path to lexical models")
    args = parser.parse_args()

    # TODO



