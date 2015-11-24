import sys, argparse, os
from argparse_util import *
from abstract_parser import AbstractParser
from nlp_pipeline import NlpPipeline
from text import Text, Sentence
from tokens import WordToken, PunctuationToken, Punctuation
from sbd_config import config

reload(sys)
sys.setdefaultencoding('utf8')


###exception when config use questionmark true

class LineParser(AbstractParser):

    def __init__(self, file):

        if config.getboolean('features', 'use_question_mark'):
            raise NameError("Question marks not supported by LineParser")

        if config.getboolean('features', 'pos_tagging'):
            self.nlp_pipeline = NlpPipeline()
        else:
            self.nlp_pipeline = None
        
        self.file = file

    def parse(self):
        with open(self.file, "r") as file_:
            text = Text()
            sentence = Sentence()
            sentence.tokens = []

            i = 0
            for line_unenc in file_:
                line = unicode(line_unenc.encode('utf8'))
                i += 1
                line = line.encode('utf8')
                line = line.rstrip() 
                splittedLine = line.split('\t')
                word = unicode(splittedLine[0])
                period = unicode(splittedLine[1])
                sentence.tokens.extend(self.__createToken(word,period))
                if period == 'PERIOD':
                    if self.nlp_pipeline != None:
                        self.nlp_pipeline.pos_tag(sentence.tokens)
                    text.add_sentence(sentence)
                    sentence = Sentence()
                    sentence.tokens = []
        return [text]
    
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
    for text in texts:
        print(text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test the line text file parsing')
    parser.add_argument('file', help='file contains lines with word and period value', type=lambda arg: is_valid_file(parser, arg))
    args = parser.parse_args()

    main(args.file)



