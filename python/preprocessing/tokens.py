from enum import Enum

class Punctuation(Enum):
    NONE = 0
    COMMA = 1
    PERIOD = 2
    QUESTION = 3

class WordToken(object):
    def __init__(self, word):
        self.word = word
        self.word_vec = None
        self.pos_tags = set()

    def is_punctuation(self):
        return False

    def set_word_vec(self, word_vec):
        self.word_vec = word_vec

    def set_pos_tags(self, pos_tag):
        self.pos_tags = pos_tag

    def __str__(self):
        pos_str = ""
        if len(self.pos_tags) > 0:
            pos_str = " (" + " ".join(map(unicode, self.pos_tags)) + ")"
        return self.word + pos_str

    def __repr__(self):
        return self.word

    def __eq__(self, other):
        if other.is_punctuation():
            return False
        return self.word == other.word

    def __hash__(self):
        return hash(self.word) ^ hash(self.is_punctuation())


class PunctuationToken(object):
    def __init__(self, word, punctuation_type):
        self.word = word
        self.punctuation_type = punctuation_type

    def is_punctuation(self):
        return True

    def __str__(self):
        return str(self.punctuation_type)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not other.is_punctuation():
            return False
        return self.punctuation_type == other.punctuation_type

    def __hash__(self):
        return hash(self.punctuation_type) ^ hash(self.is_punctuation())

