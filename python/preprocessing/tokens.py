from enum import Enum


class Punctuation(Enum):
    NONE = 0
    COMMA = 1
    PERIOD = 2
    QUESTION = 3


class AudioToken(object):
    def __init__(self, word):
        self.word = word
        self.begin = 0.0
        self.duration = 0.0
        self.pause_before = 0.0
        self.pause_after = 0.0
        self.energy = 0.0
        self.pitch = 0.0
        self.pitch_levels = []

    def is_punctuation(self):
        return False

    def append_pitch_level(self, pitch_level):
        self.pitch_levels.append(pitch_level)

    def set_pause_before(self, pause_before):
        self.pause_before = pause_before

    def set_pause_after(self, pause_after):
        self.pause_after = pause_after

    def set_energy(self, energy):
        self.energy = energy

    def set_pitch(self, pitch):
        self.pitch = pitch

    def __str__(self):
        return "(%s) %s" % (str(self.pause_before), self.word)

    def __repr__(self):
        return self.word

    def __eq__(self, other):
        if other.is_punctuation():
            return False
        return self.word == other.word

    def __hash__(self):
        return hash(self.word) ^ hash(self.is_punctuation())


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

