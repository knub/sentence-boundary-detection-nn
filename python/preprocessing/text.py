import common.sbd_config as sbd

END_OF_TEXT_MARKER = "###END###"

class Text(object):

    def __init__(self):
        self.sentences = []
        self.POS_TAGGING = sbd.config.getboolean('features', 'pos_tagging')

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def get_tokens(self):
        tokens = []
        for sentence in self.sentences:
            tokens.extend(sentence.tokens)
        return tokens

    def write_to_file(self, filename, append = False):
        if append:
            file = open(filename, "a")
        else:
            file = open(filename)

        for sentence in self.sentences:
            tokens = sentence.get_tokens()
            # get the word vectors for all tokens in the sentence
            for i, token in enumerate(tokens):
                if not token.is_punctuation():
                    if i == len(tokens) - 1:
                        punctuation_string = "PERIOD"
                    else:
                        next_token = tokens[i + 1]
                        if next_token.is_punctuation():
                            punctuation_string = str(next_token.punctuation_type)
                            punctuation_string = punctuation_string[12:]
                        else:
                            punctuation_string = "O"

                    if self.POS_TAGGING:
                        line_str = u"%s\t%s\t%s\n" % (token.word.lower(), " ".join(map(unicode, token.pos_tags)), punctuation_string)
                    else:
                        line_str = u"%s\t%s\n" % (token.word.lower(), punctuation_string)

                    file.write(line_str)

        file.write("%s\n" % END_OF_TEXT_MARKER)
        file.close()

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

        return "sentence: %s \n tokens: %s \n" % (self.sentence_text, tokens_str)
