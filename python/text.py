class Text(object):
    def __init__(self):
        self.sentences = []

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def get_tokens(self):
        tokens = []
        for sentence in self.sentences:
            tokens.extend(sentence.tokens)
        return tokens

    def __str__(self):
        sentences_str = ''.join(map(str, self.sentences))
        return sentences_str


class Sentence(object):

    def __init__(self):
        self.tokens = None
        self.sentence_text = None

    def set_sentence_text(self, sentence_text):
        self.sentence_text = sentence_text

    def set_tokens(self, tokens):
        self.tokens = tokens

    def get_tokens(self):
        return self.tokens

    def __str__(self):
        tokens_str = ', '.join(map(str, self.tokens))
        return "text: %s \n tokens: %s \n" % (self.sentence_text, tokens_str)

