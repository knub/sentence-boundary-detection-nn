from parsing.get_parser import *
from sbd_classification.classification_input import InputText
from sbd_classification.classification_input import InputAudio
from preprocessing.tokens import WordToken
from preprocessing.nlp_pipeline import NlpPipeline

class AudioParser(object):

    def parse(self, ctm_file):
        parser = get_parser(ctm_file)
        base_dir = os.path.dirname(parser.get_file_name())
        raw_talks = parser.parse()

        talks = []
        for i, talk in enumerate(raw_talks):
            # build range map from second intervals to tokens
            talk.build_interval_tree()

            # get pitch feature values
            pitch_file = base_dir + "/" + talk.group_name + "_talkid" + str(talk.talk_id) + ".pitch"
            talk.parse_pitch_feature(pitch_file)

            # get energy feature values
            energy_file = base_dir + "/" + talk.group_name + "_talkid" + str(talk.talk_id) + ".energy"
            talk.parse_energy_feature(energy_file)

            # get pitch feature values
            talk.parse_pitch_feature(pitch_file)
            # get energy feature values
            talk.parse_energy_feature(energy_file)
            # normalize features
            talk.normalize()

            talks.append(talk)

        return talks

