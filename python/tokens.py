from enum import Enum

class Punctuation(Enum):
    COMMA = 1
    PERIOD = 2
    QUESTION = 3

class WordToken(object):
    def __init__(self, word):
        self.word = word
        self.word_vec = None
        self.pos_tag = ""

    def is_punctuation(self):
        return False

    def set_word_vec(self, word_vec):
        self.word_vec = word_vec

    def set_pos_tag(self, pos_tag):
        self.pos_tag = pos_tag

    def __str__(self):
        return self.word


class PunctuationToken(object):
    def __init__(self, original, punctuationType):
        self.orginal = original
        self.punctuation_type = punctuationType

    def is_punctuation(self):
        return True

    def __str__(self):
        return str(self.punctuation_type)

    def __repr__(self):
        return str(self.punctuation_type)
