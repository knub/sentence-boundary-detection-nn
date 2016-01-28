from parsing.get_parser import *
from sbd_classification.classification_input import InputText
from sbd_classification.classification_input import InputAudio
from preprocessing.tokens import WordToken
from preprocessing.nlp_pipeline import NlpPipeline

class AudioParser(object):

    def __init__(self):
        self.talks = None

    def parse(self, ctm_file, pitch_file, energy_file):
        parser = get_parser(ctm_file)
        talks = parser.parse()

        self.talks = []
        for i, talk in enumerate(talks):
            talk.build_interval_tree()

            # get pitch feature values
            talk.parse_pitch_feature(pitch_file)
            # get energy feature values
            talk.parse_energy_feature(energy_file)
            # normalize features
            talk.normalize()

            self.talks.append(talk)

        return self.talks