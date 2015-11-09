import talk_parsing
import inspect
import sbd_token
import numpy

WINDOW_SIZE = 5
PUNCTUATION_POS = 3

class TrainingInstance(object):

    def __init__(self, tokens, is_comma, is_period, is_question):
        self.tokens = tokens
        self.comma = is_comma         # , : -
        self.period = is_period       # ! ; .
        self.question = is_question   # ?

    def __str__(self):
        return "TOKENS: %s \nHAS_COMMA: %s \nHAS_PERIOD: %s \nHAS_QUESTION: %s \n" % (" ".join(map(str, self.tokens)), str(self.comma), str(self.period), str(self.question))

    def get_array(self):
        dimensions = (1, WINDOW_SIZE, len(self.tokens[0].word_vec))
        arr = numpy.zeros(dimensions, numpy.float32)
        for i in range(0, WINDOW_SIZE):
            arr[i] = self.tokens[i].word_vec
        return arr

    def get_label(self):
        if self.comma:
            return 1
        if self.period:
            return 2
        if self.question:
            return 3
        return 0

class SlidingWindow(object):

    def list_windows(self, sentence):
        tokens = sentence.gold_text

        index = 0
        training_instance = []

        while index < len(tokens) - WINDOW_SIZE:
            word_count = 0
            has_comma = False
            has_period = False
            has_question = False
            window_tokens = []

            i = index
            while word_count < WINDOW_SIZE and i < len(tokens):

                is_punctuation = isinstance(tokens[i], sbd_token.PunctuationToken)

                if not is_punctuation:
                    word_count += 1
                    window_tokens.append(tokens[i])

                if word_count == PUNCTUATION_POS and is_punctuation:
                    if tokens[i].type == talk_parsing.Punctuation.COMMA:
                        has_comma = True
                    if tokens[i].type == talk_parsing.Punctuation.PERIOD:
                        has_period = True
                    if tokens[i].type == talk_parsing.Punctuation.QUESTION:
                        has_question = True

                i += 1

            training_instance.append(TrainingInstance(window_tokens, has_comma, has_period, has_question))
            index += 1

        return training_instance

def main():
    print("TODO")
    # sentence = Sentence(1, "You know, one of the intense pleasures of travel and one of the delights of ethnographic research is the opportunity to live amongst those who have not forgotten the old ways, who still feel their past in the wind, touch it in stones polished by rain, taste it in the bitter leaves of plants.")
    # sentence.set_time_start(12.95)
    # sentence.set_time_end(29.50)
    # sentence.set_speech_text("You know one of the {$(<BREATH>)} intense pleasures of travel in one of the delights of ethnographic research {$(<BREATH>)} is the opportunity to live amongst those who have not forgotten the old ways {$(<BREATH>)} to {$(<BREATH>)} still feel their past and the wind {$(<SBREATH>)} touch and stones pause by rain {$(<SBREATH>)} I tasted in the bitter leaves of plants")
    # sentence.set_enriched_speech_text("You know one of the intense pleasures of travel in one of the delights of ethnographic research is the opportunity to live amongst those who have not forgotten the old ways to still feel their past and the wind touch and stones pause by rain I tasted in the bitter leaves of plants")
    #
    # slidingWindow = SlidingWindow()
    # windows = slidingWindow.list_windows(sentence)
    #
    # for window in windows:
    #     print(window)

if __name__=='__main__':
    main()
