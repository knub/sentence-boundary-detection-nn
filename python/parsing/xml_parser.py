import xml.etree.ElementTree, sys, os.path, re

from common.argparse_util import *
from preprocessing.nlp_pipeline import NlpPipeline
from preprocessing.text import *

from abstract_parser import AbstractParser, main, parse_command_line_arguments

class XMLParser(AbstractParser):
    def __init__(self, filename):
        super(XMLParser, self).__init__(filename)
        if not self.wants_this_file():
            return
        self.nlp_pipeline = NlpPipeline()
        self._linenumber = self._count_docs()
        self._progress = 0

    def _wanted_file_endings(self):
        return (".xml",)

    def parse(self):
        mteval = xml.etree.ElementTree.parse(self.filename).getroot()
        srcset = mteval.find("srcset")
        for doc in srcset.findall('doc'):
            self._progress += 1
            talk = Text()

            for sentence in doc.findall("seg"):
                sentence_text = unicode(sentence.text)

                sentence = Sentence()
                sentence.set_sentence_text(sentence_text)
                sentence.set_tokens(self.nlp_pipeline.parse_text(sentence_text))
                talk.add_sentence(sentence)

            yield talk

    def progress(self):
        return self._line_count_progress()

    def _count_docs(self):
        mteval = xml.etree.ElementTree.parse(self.filename).getroot()
        srcset = mteval.find("srcset")
        i = 0
        for doc in srcset.findall('doc'):
            i += 1
        return i

################
# Example call #
################

if __name__ == '__main__':
    parse_command_line_arguments(XMLParser)
