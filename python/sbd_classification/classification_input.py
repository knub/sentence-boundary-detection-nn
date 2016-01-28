from preprocessing.nlp_pipeline import NlpPipeline, PosTag


class InputText(object):

    def __init__(self, text):
        self.text = text

        self.nlp_pipeline = NlpPipeline()
        self.tokens = self.nlp_pipeline.parse_text(self.text)

    def get_tokens(self):
        return self.tokens

class InputAudio(object):

    def __init__(self, audio_tokens):
        self.tokens = audio_tokens

    def get_tokens(self):
        return self.tokens
