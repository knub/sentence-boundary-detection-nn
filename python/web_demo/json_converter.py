import common.sbd_config as sbd
import numpy
from sbd_classification.util import get_index

class JsonConverter(object):

    def __init__(self, punctuation_pos = None, pos_tagging = None):
        self.classes_lexical_audio = ["NONE", "COMMA", "PERIOD"]
        self.classes_audio = ["NONE", "PERIOD"]

    def read_lexical_config(self, punctuation_pos = None, pos_tagging = None):
        self.LEXICAL_PUNCTUATION_POS = sbd.config.getint('windowing', 'punctuation_position') if punctuation_pos == None else punctuation_pos
        self.LEXICAL_WINDOW_SIZE = sbd.config.getint('windowing', 'window_size')
        self.POS_TAGGING = sbd.config.getboolean('features', 'pos_tagging') if pos_tagging == None else pos_tagging

    def read_audio_config(self, punctuation_pos = None):
        self.AUDIO_PUNCTUATION_POS = sbd.config.getint('windowing', 'punctuation_position') if punctuation_pos == None else punctuation_pos
        self.AUDIO_WINDOW_SIZE = sbd.config.getint('windowing', 'window_size')

    def convert_fusion(self, tokens, fusion_probs, lexical_probs, audio_probs):
        json_data = []

        # build json
        for i, token in enumerate(tokens):
            token_json = {'type': 'word', 'token': token.word}
            if self.POS_TAGGING:
                token_json['pos'] = [str(tag).replace("PosTag.", "") for tag in token.pos_tags]
            json_data.append(token_json)

            probs_json = {'type': 'punctuation'}

            # FUSION
            # we have probabilities for all tokens
            current_punctuation = self.classes_lexical_audio[numpy.argmax(fusion_probs[i])]
            class_distribution = self._get_class_distribution(fusion_probs[i], self.classes_lexical_audio)
            probs_json['fusion'] = {'punctuation': current_punctuation, 'probs': class_distribution}

            # AUDIO
            current_prediction_position = get_index(i, len(audio_probs), self.AUDIO_PUNCTUATION_POS)
            if current_prediction_position < 0:
                probs_json['audio'] = {'punctuation': 'NONE', 'probs': {'NONE': 1.0, 'PERIOD': 0.0}}
            else:
                current_punctuation = self.classes_audio[numpy.argmax(audio_probs[i])]
                class_distribution = self._get_class_distribution(audio_probs[i], self.classes_audio)
                probs_json['audio'] = { 'punctuation': current_punctuation, 'probs': class_distribution}

            # LEXICAL
            current_prediction_position = get_index(i, len(lexical_probs), self.LEXICAL_PUNCTUATION_POS)
            if current_prediction_position < 0:
                probs_json['lexical'] = {'punctuation': 'NONE', 'probs': {'NONE': 1.0, 'COMMA': 0.0, 'PERIOD': 0.0}}
            else:
                current_punctuation = self.classes_lexical_audio[numpy.argmax(lexical_probs[current_prediction_position])]
                class_distribution = self._get_class_distribution(lexical_probs[current_prediction_position], self.classes_lexical_audio)
                probs_json['lexical'] = {'punctuation': current_punctuation, 'probs': class_distribution}

            json_data.append(probs_json)

        return json_data

    def convert_lexical(self, tokens, punctuation_probs):
        json_data = []
        # build json
        for i, token in enumerate(tokens):
            token_json = {'type': 'word', 'token': token.word}
            if self.POS_TAGGING:
                token_json['pos'] = [str(tag).replace("PosTag.", "") for tag in token.pos_tags]
            json_data.append(token_json)

            # we are at the beginning or at the end of the text and do not have any predictions for punctuations
            current_prediction_position = get_index(i, len(punctuation_probs), self.LEXICAL_PUNCTUATION_POS)
            if current_prediction_position < 0:
                json_data.append({'type': 'punctuation', 'punctuation': 'NONE', 'probs': {'NONE': 1.0, 'COMMA': 0.0, 'PERIOD': 0.0}})
            else:
                current_punctuation = self.classes_lexical_audio[numpy.argmax(punctuation_probs[current_prediction_position])]
                class_distribution = self._get_class_distribution(punctuation_probs[current_prediction_position], self.classes_lexical_audio)
                json_data.append({'type': 'punctuation', 'punctuation': current_punctuation, 'probs': class_distribution})

        return json_data

    def _get_class_distribution(self, probs, classes):
        json_data = {}
        for i in range (0, len(classes)):
            json_data[classes[i]] = str(probs[i])
        return json_data



