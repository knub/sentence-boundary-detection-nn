from parsing.get_parser import *
from sbd_classification.lexical_clasification import InputText
from sbd_classification.audio_clasification import InputAudio


class AudioClassifier(object):

    def __init__(self, ctm_file, pith_file, energy_file):
        self.ctm_file = ctm_file
        self.pitch_file = pith_file
        self.energy_file = energy_file
        self.talk = None

    def parse(self):
        parser = get_parser(self.ctm_file)
        talks = parser.parse()

        if len(talks) > 1:
            print("WARNING: More than one talk in CTM file. Take only the first one.")

        for i, talk in enumerate(talks):
            if i >= 1:
                break

            talk.build_interval_tree()

            # get pitch feature values
            talk.parse_pith_feature(self.pitch_file)
            # get energy feature values
            talk.parse_energy_feature(self.energy_file)
            # normalize features
            talk.normalize()

            self.talk = talk

    def get_input_text(self):
        text = ""
        for token in self.talk.get_tokens():
            if not token.is_punctuation():
                text += token.word + " "
        return InputText(text)

    def get_input_audio(self):
        tokens = []
        for token in self.talk.get_tokens():
            if not token.is_punctuation():
                tokens.append(token)
        return InputAudio(tokens)
