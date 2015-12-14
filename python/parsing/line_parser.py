import sys, argparse, os

from common.argparse_util import *
from common.sbd_config import config
from preprocessing.nlp_pipeline import NlpPipeline
from preprocessing.text import Text, Sentence
from preprocessing.tokens import WordToken, PunctuationToken, Punctuation

from abstract_parser import AbstractParser, main, parse_command_line_arguments

reload(sys)
sys.setdefaultencoding('utf8')


class LineParser(AbstractParser):

    def __init__(self, filename):
        super(LineParser, self).__init__(filename)
        if not self.wants_this_file():
            return
            
        self._init_line_count_progress()
        if config.getboolean('features', 'use_question_mark'):
            raise ValueError("Question marks not supported by LineParser")
        if config.getboolean('features', 'pos_tagging'):
            self.nlp_pipeline = NlpPipeline()
        else:
            self.nlp_pipeline = None

    def _wanted_file_endings(self):
        return (".line", )

    def parse(self):
        with open(self.filename, "r") as file_:
            text = Text()
            sentence = Sentence()
            sentence.tokens = []

            for line_unenc in file_:
                self._progress += 1

                # parse line
                line = unicode(line_unenc, errors='ignore')
                line = line.rstrip()

                # split line into word and type
                splitted_line= line.split('\t')
                word = unicode(splitted_line[0])
                if "?" in word and len(word) > 0:
                    word = word.replace("?", "")
                period = unicode(splitted_line[1])

                sentence.tokens.extend(self.__createToken(word,period))
                if period == 'PERIOD':
                    if self.nlp_pipeline != None:
                        self.nlp_pipeline.pos_tag(sentence.tokens)
                    text.add_sentence(sentence)
                    sentence = Sentence()
                    sentence.tokens = []
        return [text]

    def progress(self):
        return self._line_count_progress()
 
    def __createToken(self, word, period):
        wordToken = WordToken(word)
        punctuationToken = None
        if period == 'PERIOD':
            punctuationToken = PunctuationToken(period, Punctuation.PERIOD)
        elif period == 'COMMA':
            punctuationToken = PunctuationToken(period, Punctuation.COMMA)

        if punctuationToken != None:
            return [wordToken, punctuationToken]
        else:
         return [wordToken]




################
# Example call #
################

if __name__ == '__main__':
    parse_command_line_arguments(LineParser)
