import argparse, sys, os

from common.argparse_util import *
from preprocessing.nlp_pipeline import NlpPipeline
from preprocessing.text import Sentence, Text

from abstract_parser import AbstractParser, main, parse_command_line_arguments

TEXT_SEPARATOR = "################################################################################"

reload(sys)
sys.setdefaultencoding('utf8')

class PlaintextParser(AbstractParser):
    def __init__(self, filename):
        super(PlaintextParser, self).__init__(filename)
        if not self.wants_this_file():
            return
        self._init_line_count_progress()
        self.nlp_pipeline = NlpPipeline()

    def _wanted_file_endings(self):
        return (".txt",)

    def parse(self):
        text = Text()

        with open(self.filename, "r") as file_:
            for line_unenc in file_:
                self._progress += 1
                line = unicode(line_unenc.encode('utf8'))
                if line.startswith(TEXT_SEPARATOR):
                    if (len(text.sentences) > 0):
                        yield text
                        text = Text()
                        continue
                sentences = self.nlp_pipeline.sentence_segmentation(line)
                for sentence in sentences:
                    s = Sentence()
                    s.set_sentence_text(sentence)
                    s.set_tokens(self.nlp_pipeline.parse_text(sentence))
                    text.add_sentence(s)
        if (len(text.sentences) > 0):
            yield text

    def progress(self):
        return self._line_count_progress()


################
# Example call #
################

if __name__ == '__main__':
    parse_command_line_arguments(PlaintextParser)
