
class Evaluation(object):

    def __init__(self, talks):
        self.talks = talks

    def evaluate(lexical_model_file, audio_model_file, vector):
        lexical_classifier = load_lexical_classifier(lexical_model_file, vector)
        audio_classifier = load_audio_classifier(audio_model_file)

        # get lexical probabilities
        (lexical_token, lexical_probs) = lexical_classifier.predict(InputText(self.talks))

        # get audio probabilities
        (audio_token, audio_probs) = audio_classifier.predict(InputAudio(self.talks))

        # fusion
        fusion = Fusion()
        fusion_probs = fusion.fuse(tokens, lexical_probs, audio_probs)

        # evaluate


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='evaluates the fusion.')
    parser.add_argument('data_root_folder', help="path to data")
    parser.add_argument('audio_model_root_folder', help="path to audio models")
    parser.add_argument('lexical_model_root_folder', help="path to lexical models")
    args = parser.parse_args()




