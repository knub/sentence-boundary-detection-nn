import numpy
from nlp_pipeline import Punctuation, NlpPipeline
from tokens import PunctuationToken
from talk_parser import Sentence, Talk
from training_instance import TrainingInstance

WINDOW_SIZE = 5
PUNCTUATION_POS = 3

class SlidingWindow(object):

    def list_windows(self, talk):
        tokens = talk.get_gold_tokens()

        index = 0
        training_instances = []

        while index < len(tokens) - WINDOW_SIZE:
            window_tokens = []
            instance_label = Punctuation.NONE

            i = index
            word_count = 0
            while word_count < WINDOW_SIZE and i < len(tokens):
                current_token = tokens[i]
                is_punctuation = current_token.is_punctuation()

                # check if the next token is also a punctuation token, error if yes
#                if is_punctuation and i + 1 < len(tokens) and tokens[i + 1].is_punctuation():
#                    # TODO: Double-check again, whether this is an issue or not
#                    raise Exception("Two Punctuations in a row:\nSentence: " + talk.gold_text + "\n" + str(current_token) + " and " + str(tokens[i + 1]))

                if not is_punctuation:
                    word_count += 1
                    window_tokens.append(current_token)
                elif i == index:
                    index += 1  ##dont parse windows with punctuations at the beginning twice

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

   # sentence = Sentence(1, "You know, one of the intense pleasures of travel and one of the delights of ethnographic research is the opportunity to live amongst those who have not forgotten the old ways, who still feel their past in the wind, touch it in stones polished by rain, taste it in the bitter leaves of plants.")
    sentence = Sentence(1, unicode("I'm a savant, or more precisly, a high-functioning autisitic savant. It"))
    sentence.set_time_start(12.95)
    sentence.set_time_end(29.50)
    sentence.set_gold_tokens(nlp_pipeline.parse_text(sentence.gold_text))

    talk = Talk(123, "title")
    talk.add_sentence(sentence)

    slidingWindow = SlidingWindow()
    windows = slidingWindow.list_windows(talk)

    for window in windows:
        print(window)


if __name__ == '__main__':
    main()
