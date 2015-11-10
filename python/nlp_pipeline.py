import nltk
from tokens import Punctuation, PunctuationToken, WordToken

class NlpPipeline(object):

    def __init__(self):
         self.punctuation_mapping = {
            ";": Punctuation.PERIOD,
            ".": Punctuation.PERIOD,
            "!": Punctuation.PERIOD,
            ",": Punctuation.COMMA,
            ":": Punctuation.COMMA,
            "-": Punctuation.COMMA,
            "?": Punctuation.QUESTION
        }


    def parse_text(self, text):
        raw_tokens = nltk.word_tokenize(text)
        # pos_tags = nltk.pos_tag(raw_tokens)
        tokens = []

        for i in range(0, len(raw_tokens)):
            if raw_tokens[i] in self.punctuation_mapping:
                tokens.append(PunctuationToken(raw_tokens[i], self.punctuation_mapping[raw_tokens[i]]))
            else:
                word_token = WordToken(raw_tokens[i])
                # word_token.set_pos_tag(pos_tags[i][1])
                tokens.append(word_token)

        return tokens


