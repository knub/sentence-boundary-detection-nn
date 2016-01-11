from intervaltree import IntervalTree

class Audio(object):

    def __init__(self):
        self.sentences = []
        self.pitch_interval = IntervalTree()

    def get_tokens(self):
        tokens = []
        for sentence in self.sentences:
            tokens.extend(sentence.tokens)
        return tokens

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def _build_interval_tree(self):
        for token in self.get_tokens():
            if not token.is_punctutaion:
                self.pitch_interval.addi(token.begin, token.begin + token.duration, [])

    def parse_pith_feature(self, filename):
        self._build_interval_tree()

        with open(filename, "r") as file_:
            for line_unenc in file_:
                # parse line
                line = unicode(line_unenc, errors='ignore')
                line = line.rstrip()

                line_parts = line.split("\t")
                second = line_parts[0]
                pitch_level = line_parts[1]

                next(iter(self.pitch_interval[second])).data.append(pitch_level)

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
