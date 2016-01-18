from intervaltree import IntervalTree

class Audio(object):

    def __init__(self):
        self.sentences = []
        self.pitch_interval = IntervalTree()
        self.talk_id = 0
        self.group_name = None

        self.PITCH_FILTER = 700.0

    def get_tokens(self):
        tokens = []
        for sentence in self.sentences:
            tokens.extend(sentence.tokens)
        return tokens

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def _build_interval_tree(self):
        for token in self.get_tokens():
            if not token.is_punctuation():
                self.pitch_interval.addi(token.begin, token.begin + token.duration, token)

    def parse_pith_feature(self, filename):
        self._build_interval_tree()

        with open(filename, "r") as file_:
            for line_unenc in file_:
                # parse line
                line = unicode(line_unenc, errors='ignore')
                line = line.rstrip()

                line_parts = line.split(" ")
                second = float(line_parts[0])
                pitch_level = float(line_parts[1])

                if pitch_level < self.PITCH_FILTER:
                    try:
                        token = next(iter(self.pitch_interval[second])).data
                        token.append_pitch_level(pitch_level)
                    except:
                        continue

        for sentence in self.sentences:
            avg_pitch = sentence.get_avg_pitch_level()
            for token in sentence.get_tokens():
                if not token.is_punctuation():
                    try:
                        token.pitch = (reduce(lambda x, y: x + y, token.pitch_levels) / len(token.pitch_levels)) - avg_pitch
                    except:
                        print("Token has no pitch levels. Setting pitch to avg_pitch.")
                        token.pitch = avg_pitch

    def __str__(self):
        sentences_str = ''.join(map(str, self.sentences))
        return sentences_str


class AudioSentence(object):

    def __init__(self):
        self.tokens = []
        self.begin = 0
        self.end = 0

    def get_avg_pitch_level(self):
        audio_tokens = []
        for token in self.tokens:
            if not token.is_punctuation():
                audio_tokens.append(token)
        l = [item for token in audio_tokens for item in token.pitch_levels]
        try:
            return reduce(lambda x, y: x + y, l) / len(l)
        except:
            print("Sentence has no pitch levels. Setting avg_pitch to 0.0.")
            return 0.0

    def append_token(self, token):
        self.tokens.append(token)

    def set_tokens(self, tokens):
        self.tokens = tokens

    def get_tokens(self):
        return self.tokens

    def __str__(self):
        tokens_str = ', '.join(map(str, self.tokens))

        return "begin: %s tokens: %s \n" % (self.begin, tokens_str)
