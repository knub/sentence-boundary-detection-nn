import common.sbd_config as sbd
import numpy

class JsonConverter(object):

    def __init__(self, punctuation_pos = None, pos_tagging = None):
        self.classes_lexical_audio = ["NONE", "COMMA", "PERIOD"]
        self.classes_audio = ["NONE", "PERIOD"]
        self.PUNCTUATION_POS = sbd.config.getint('windowing', 'punctuation_position') if punctuation_pos == None else punctuation_pos
        self.POS_TAGGING = sbd.config.getboolean('features', 'pos_tagging') if pos_tagging == None else pos_tagging

    def convert_fusion(self, tokens, fusion_probs, lexical_probs, audio_probs):
        json_data = []

        # TODO:
        # Die Window-Size und Punctuation-Position vom Audio Model berücksichtigen

        # build json
        for i, token in enumerate(tokens):
            token_json = {'type': 'word', 'token': token.word}
            if self.POS_TAGGING:
                token_json['pos'] = [str(tag).replace("PosTag.", "") for tag in token.pos_tags]
            json_data.append(token_json)

            probs_json = {'type': 'punctuation'}

            # FUSION
            if i < len(fusion_probs):
                current_punctuation = self.classes_lexical_audio[numpy.argmax(fusion_probs[i])]
                class_distribution = self._get_class_distribution(fusion_probs[i], self.classes_lexical_audio)
                probs_json['fusion'] = {'punctuation': current_punctuation, 'probs': class_distribution}
            else:
                probs_json['fusion'] = {'punctuation': 'NONE', 'probs': {'NONE': 1.0, 'COMMA': 0.0, 'PERIOD': 0.0}}

            # AUDIO
            if i < len(audio_probs):
                current_punctuation = self.classes_audio[numpy.argmax(audio_probs[i])]
                class_distribution = self._get_class_distribution(audio_probs[i], self.classes_audio)
                probs_json['audio'] = { 'punctuation': current_punctuation, 'probs': class_distribution}
            else:
                probs_json['audio'] = {'punctuation': 'NONE', 'probs': {'NONE': 1.0, 'PERIOD': 0.0}}

            # LEXICAL
            current_prediction_position = i - self.PUNCTUATION_POS + 1
            if 0 <= current_prediction_position < len(lexical_probs):
                current_punctuation = self.classes_lexical_audio[numpy.argmax(lexical_probs[current_prediction_position])]
                class_distribution = self._get_class_distribution(lexical_probs[current_prediction_position], self.classes_lexical_audio)
                probs_json['lexical'] = {'punctuation': current_punctuation, 'probs': class_distribution}
            else:
                probs_json['lexical'] = {'punctuation': 'NONE', 'probs': {'NONE': 1.0, 'COMMA': 0.0, 'PERIOD': 0.0}}

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
            current_prediction_position = i - self.PUNCTUATION_POS + 1
            if 0 <= current_prediction_position and current_prediction_position < len(punctuation_probs):
                current_punctuation = self.classes_lexical_audio[numpy.argmax(punctuation_probs[current_prediction_position])]
                class_distribution = self._get_class_distribution(punctuation_probs[current_prediction_position], self.classes_lexical_audio)
                json_data.append({'type': 'punctuation', 'punctuation': current_punctuation, 'probs': class_distribution})
            else:
                json_data.append({'type': 'punctuation', 'punctuation': 'NONE', 'probs': {'NONE': 1.0, 'COMMA': 0.0, 'PERIOD': 0.0}})

        return json_data

    def _get_class_distribution(self, probs, classes):
        json_data = {}
        for i in range (0, len(classes)):
            json_data[classes[i]] = str(probs[i])
        return json_data



