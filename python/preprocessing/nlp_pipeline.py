import nltk, nltk.data
from enum import Enum
import regex as re
import common.sbd_config as sbd
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


class NlpPipeline(object):

    def __init__(self):
        self.POS_TAGGING = sbd.config.getboolean('features', 'pos_tagging')
        self.NUMBER_REPLACEMENT = sbd.config.getboolean('features', 'number_replacement')

        self.punkt = None
        self.punctuation_regex = re.compile("^\p{posix_punct}+$")
        self.punctuation_mapping = {
            ";": Punctuation.PERIOD,
            ".": Punctuation.PERIOD,
            "!": Punctuation.PERIOD,
            ",": Punctuation.COMMA,
            ":": Punctuation.COMMA,
            "-": Punctuation.COMMA,
            "--": Punctuation.COMMA,
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

        for raw_token in raw_tokens:
            if raw_token in self.punctuation_mapping:
                punctuation_type = self.punctuation_mapping[raw_token]
                tokens.append(PunctuationToken(raw_token, punctuation_type))
            else:
                word_token = self.process_word(raw_token)
                if word_token is None:
                    continue
                tokens.append(WordToken(word_token))

        if self.POS_TAGGING:
            self.pos_tag(tokens)

        return tokens

    def process_word(self, raw_token):
        if re.match(self.punctuation_regex, raw_token):
            return None
        if self.NUMBER_REPLACEMENT:
            return self._replace_number(raw_token)
        return raw_token


    def pos_tag(self, tokens):
        word_tokens = map(lambda x: x.word, tokens)
        pos_tags = nltk.pos_tag(word_tokens)

        for i, token in enumerate(tokens):
            if isinstance(token, WordToken):
                pos_tag_str = pos_tags[i][1]
                token.set_pos_tags(self._parse_pos_tag(pos_tag_str))

    def _parse_pos_tag(self, pos_tag_str):
        pos_tags = pos_tag_str.split("/")
        pos_tag_set = set()

        for pos_tag in pos_tags:
            pos_tag_set.add(self.pos_tag_mapping.get(pos_tag, PosTag.OTHER))

        return pos_tag_set

    def sentence_segmentation(self, text):
        if not self.punkt:
            self.punkt = nltk.data.load('tokenizers/punkt/english.pickle')
        return self.punkt.tokenize(text.strip())

    def _replace_number(self, word):
        if word[:-2].isdigit() and (word.endswith("st") or word.endswith("nd") or word.endswith("rd") or word.endswith("th")):
            return "1st"
        try:
            float(word)
            return "1"
        except ValueError:
            return word

