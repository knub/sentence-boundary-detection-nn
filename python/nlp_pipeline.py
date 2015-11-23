import nltk
from enum import Enum
from tokens import Punctuation, PunctuationToken, WordToken

class PosTag(Enum):
    OTHER = 0
    VERB = 1
    NOUN = 2
    DETERMINER = 3
    ADJECTIVE = 4
    ADVERB = 5
    NUMERAL = 6
    CONJUNCTION = 7
    PARTICLE = 8
    EXISTENTIAL_THERE = 9
    MARKER = 10
    PRONOUN = 11
    INTERJECTION = 12
    QUESTION_WORDS = 13

POS_TAGGING = False

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
        self.inv_pos_tag_mapping = {
            PosTag.ADJECTIVE: {
                "JJ", "JJR", "JJS"
            },
            PosTag.ADVERB: {
                "RB", "RBR", "RBS"
            },
            PosTag.PARTICLE: {
                "RP"
            },
            PosTag.CONJUNCTION: {
                "CC", "IN"
            },
            PosTag.NUMERAL: {
                "CD", "LS"
            },
            PosTag.DETERMINER: {
                "DT", "PDT"
            },
            PosTag.EXISTENTIAL_THERE: {
                "EX"
            },
            PosTag.NOUN: {
                "FW", "NN", "NNP", "NNPS", "NNS"
            },
            PosTag.VERB: {
                "MD", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"
            },
            PosTag.MARKER: {
                "POS", "TO"
            },
            PosTag.PRONOUN: {
                "PRP", "PRP$"
            },
            PosTag.INTERJECTION: {
                "UH"
            },
            PosTag.QUESTION_WORDS: {
                "WDT", "WP", "WP$", "WRB"
            }
        }
        self.pos_tag_mapping = {
            v2: k for k, v1 in self.inv_pos_tag_mapping.items() for v2 in v1
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
        tokens = []

        for i in range(0, len(raw_tokens)):
            raw_token = raw_tokens[i]

            if raw_token in self.punctuation_mapping:
                token = self.punctuation_mapping[raw_token]
                tokens.append(PunctuationToken(raw_token, token))
            else:
                word_token = WordToken(raw_token)
                tokens.append(word_token)

        if POS_TAGGING:
            self._pos_tag(tokens)

        return tokens

    def _pos_tag(self, tokens):
        word_tokens = map(lambda x: x.word, tokens)
        pos_tags = nltk.pos_tag(word_tokens)

        for i, token in enumerate(tokens):
            pos_tag_str = pos_tags[i][1]
            token.set_pos_tags(self._parse_pos_tag(pos_tag_str))

    def _parse_pos_tag(self, pos_tag_str):
        pos_tags = pos_tag_str.split("/")
        pos_tag_set = set()

        for pos_tag in pos_tags:
            pos_tag_set.add(self.pos_tag_mapping.get(pos_tag, PosTag.OTHER))

        return pos_tag_set

