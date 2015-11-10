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
        """
        Parses a text and create tokens.

        Args:
            text (str): A string representing a sentence.

        Returns:
            [token]: List of word and punctuation tokens.
        """

        raw_tokens = nltk.word_tokenize(text)
        # pos_tags = nltk.pos_tag(raw_tokens)
        tokens = []

        for i in range(0, len(raw_tokens)):
            raw_token = raw_tokens[i]
            if raw_token in self.punctuation_mapping:
                token = self.punctuation_mapping[raw_token]
                tokens.append(PunctuationToken(raw_token, token))
            else:
                word_token = WordToken(raw_token)
                # word_token.set_pos_tag(pos_tags[i][1])
                tokens.append(word_token)

        return tokens


