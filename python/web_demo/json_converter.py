
class JsonConverter(object):

    def ___init__(self):
        pass

    def convert_lexical(self):
        # build json
        for i, token in enumerate(input_text.tokens):
            token_json = {'type': 'word', 'token': token.word}
            if self.POS_TAGGING:
                token_json['pos'] = [str(tag).replace("PosTag.", "") for tag in token.pos_tags]
            json_data.append(token_json)

            # we are at the beginning or at the end of the text and do not have any predictions for punctuations
            current_prediction_position = i - self.PUNCTUATION_POS + 1
            if 0 <= current_prediction_position and current_prediction_position < len(punctuation_probs):
                current_punctuation = self.classes[numpy.argmax(punctuation_probs[current_prediction_position])]
                class_distribution = self._get_class_distribution(punctuation_probs[current_prediction_position])
                json_data.append({'type': 'punctuation', 'punctuation': current_punctuation, 'probs': class_distribution})
            else:
                json_data.append({'type': 'punctuation', 'punctuation': 'NONE', 'probs': {'NONE': 1.0, 'COMMA': 0.0, 'PERIOD': 0.0}})

        return json_data

