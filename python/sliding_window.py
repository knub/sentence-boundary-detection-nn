import numpy
from nlp_pipeline import Punctuation, NlpPipeline
from tokens import PunctuationToken
from talk_parser import Sentence


WINDOW_SIZE = 5
PUNCTUATION_POS = 3


class TrainingInstance(object):

    def __init__(self, tokens, label):
        self.tokens = tokens
        self.label = label

    def __str__(self):
        return "TOKENS: %s \nLABEL: %s \n" % (
        " ".join(map(str, self.tokens)), str(self.label))

    def get_array(self):
        dimensions = (1, WINDOW_SIZE, len(self.tokens[0].word_vec))
        arr = numpy.zeros(dimensions, float)
        for i in range(0, WINDOW_SIZE):
            arr[0][i] = self.tokens[i].word_vec
        return arr

    def get_label(self):
        return self.label.value

class SlidingWindow(object):

    def list_windows(self, sentence):
        tokens = sentence.gold_tokens

        index = 0
        training_instances = []

        while index < len(tokens) - WINDOW_SIZE:
            window_tokens = []

            i = index
            while word_count < WINDOW_SIZE and i < len(tokens):
                current_token = tokens[i]

                is_punctuation = current_token.is_punctuation()

                if is_punctuation and i + 1 < len(tokens) and tokens[i + 1].is_punctuation():
                    raise NameError("Two Punctuations in a row: " + current_token + ", " + tokens[i + 1])

                if not is_punctuation:
                    word_count += 1
                    window_tokens.append(current_token)

                if word_count == PUNCTUATION_POS and is_punctuation:
                    instance_label = current_token.punctuation_type

                i += 1

            if len(window_tokens) == WINDOW_SIZE:
                training_instances.append(TrainingInstance(window_tokens, instance_label))
            index += 1

        return training_instances



################
# Example call #
################

def main():
    nlp_pipeline = NlpPipeline()

    sentence = Sentence(1, "You know, one of the intense pleasures of travel and one of the delights of ethnographic research is the opportunity to live amongst those who have not forgotten the old ways, who still feel their past in the wind, touch it in stones polished by rain, taste it in the bitter leaves of plants.")
    sentence.set_time_start(12.95)
    sentence.set_time_end(29.50)
    sentence.set_speech_text("You know one of the {$(<BREATH>)} intense pleasures of travel in one of the delights of ethnographic research {$(<BREATH>)} is the opportunity to live amongst those who have not forgotten the old ways {$(<BREATH>)} to {$(<BREATH>)} still feel their past and the wind {$(<SBREATH>)} touch and stones pause by rain {$(<SBREATH>)} I tasted in the bitter leaves of plants")
    sentence.set_enriched_speech_text("You know one of the intense pleasures of travel in one of the delights of ethnographic research is the opportunity to live amongst those who have not forgotten the old ways to still feel their past and the wind touch and stones pause by rain I tasted in the bitter leaves of plants")
    sentence.set_gold_tokens(nlp_pipeline.parse_text(sentence.original_gold))

    slidingWindow = SlidingWindow()
    windows = slidingWindow.list_windows(sentence)

    for window in windows:
        print(window)


if __name__ == '__main__':
    main()
