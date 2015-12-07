import argparse, sys, os

from common.argparse_util import *
from preprocessing.nlp_pipeline import NlpPipeline
from preprocessing.text import Sentence, Text

from abstract_parser import AbstractParser

TEXT_SEPARATOR = "################################################################################"

reload(sys)
sys.setdefaultencoding('utf8')

class PlaintextParser(AbstractParser):
    def __init__(self, filename):
        super(PlaintextParser, self).__init__(filename)
        self._init_line_count_progress()
        self.nlp_pipeline = NlpPipeline()

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

def main(filename):
    parser = PlaintextParser(filename)
    texts = parser.parse()
    for i, text in enumerate(texts):
        print "progress %f, text %d:" % (parser.progress(), i)
        print text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test the plain text file parsing')
    parser.add_argument('filename', help='the plain text file you want to parse', type=lambda arg: is_valid_file(parser, arg))
    args = parser.parse_args()

    main(args.filename)
