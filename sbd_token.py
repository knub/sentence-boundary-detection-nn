
class Token(object):

    def __init__(self, word):
        self.word = word
        self.POS = ""

    def __str__(self):
        return self.word
