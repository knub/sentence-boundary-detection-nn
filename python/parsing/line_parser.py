import sys, argparse, os

from common.argparse_util import *
from common.sbd_config import config
from preprocessing.nlp_pipeline import NlpPipeline
from preprocessing.text import Text, Sentence
from preprocessing.tokens import WordToken, PunctuationToken, Punctuation

from abstract_parser import AbstractParser

reload(sys)
sys.setdefaultencoding('utf8')


class LineParser(AbstractParser):

    def __init__(self, filename):
        super(LineParser, self).__init__(filename)
        self._init_line_count_progress()

        if config.getboolean('features', 'use_question_mark'):
            raise NameError("Question marks not supported by LineParser")

        if config.getboolean('features', 'pos_tagging'):
            self.nlp_pipeline = NlpPipeline()
        else:
            self.nlp_pipeline = None

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

def main(filename):
    parser = LineParser(filename)
    texts = parser.parse()
    #for text in texts:
        # print(text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test the line text file parsing')
    parser.add_argument('file', help='file contains lines with word and period value', type=lambda arg: is_valid_file(parser, arg))
    args = parser.parse_args()

    main(args.file)



