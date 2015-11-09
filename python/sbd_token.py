
class WordToken(object):

    def __init__(self, word):
        self.word = word
        self.word_vec = None
        self.POS = ""

    def set_word_vec(self, word_vec):
        self.word_vec = word_vec

    def __str__(self):
        return self.word



class PunctuationToken(object):

    def __init__(self, original, punctuationType):
        self.type = punctuationType
        self.orginal = original

    def __str__(self):
         return self.type
