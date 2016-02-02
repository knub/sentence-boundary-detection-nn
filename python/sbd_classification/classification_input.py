import common.sbd_config as sbd
from preprocessing.nlp_pipeline import NlpPipeline, PosTag
from preprocessing.audio import Audio
from preprocessing.tokens import WordToken

class InputText(object):

    def __init__(self, obj):
        self.tokens = None

        if isinstance(obj, str) or isinstance(obj, unicode):
            self._initialize_with_text(obj)
        elif isinstance(obj, list):
            if obj:
                el = obj[0]
                if isinstance(el, Audio):
                    self._initialize_with_talks(obj)
                elif isinstance(el, str):
                    self._initialize_with_tokens(obj)
                else:
                    print("ERROR: Could not initialize input text!")
        else:
            print("ERROR: Could not initialize input text!")


    def _initialize_with_text(self, text):
        nlp_pipeline = NlpPipeline()
        self.tokens = nlp_pipeline.parse_text(text)

    def _initialize_with_talks(self, talks):
        nlp_pipeline = NlpPipeline()
        word_tokens = []

        for talk in talks:
            for sentence in talk.sentences:
                sentence_tokens = []
                # get all word tokens
                for token in sentence.tokens:
                    if not token.is_punctuation():
                        sentence_tokens.append(WordToken(token.word))
                # do pos_tagging if needed on sentence level
                if sbd.config.getboolean('features', 'pos_tagging'):
                    nlp_pipeline.pos_tag(sentence_tokens)
                for t in sentence_tokens:
                    t.word = t.word.lower()
                word_tokens += sentence_tokens

        self.tokens = word_tokens

    def _initialize_with_tokens(self, tokens):
        # convert tokens to WordTokens
        word_tokens = [ WordToken(token) for token in tokens ]

        # do pos_tagging if needed
        if sbd.config.getboolean('features', 'pos_tagging'):
            nlp_pipeline = NlpPipeline()
            nlp_pipeline.pos_tag(wordTokens)

        self.tokens = word_tokens

    def get_tokens(self):
        return self.tokens


class InputAudio(object):

    def __init__(self, talks):
        self.tokens = []

        for talk in talks:
            for token in talk.get_tokens():
                if not token.is_punctuation():
                    self.tokens.append(token)

    def get_tokens(self):
        return self.tokens
