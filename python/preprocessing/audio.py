import common.sbd_config as sbd

class Audio(object):

    def __init__(self):
        self.sentences = []

    def get_tokens(self):
        tokens = []
        for sentence in self.sentences:
            tokens.extend(sentence.tokens)
        return tokens

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def __str__(self):
        sentences_str = ''.join(map(str, self.sentences))
        return sentences_str


class AudioSentence(object):

    def __init__(self):
        self.tokens = None
        self.begin = 0
        self.end = 0

    def append_token(self, token):
        self.tokens.append(token)

    def set_tokens(self, tokens):
        self.tokens = tokens

    def get_tokens(self):
        return self.tokens

    def __str__(self):
        tokens_str = ', '.join(map(str, self.tokens))

        return "begin: %s tokens: %s \n" % (self.begin, tokens_str)
