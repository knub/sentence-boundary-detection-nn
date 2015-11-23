import sys
import os
from abstract_parser import AbstractParser
from nlp_pipeline import NlpPipeline
from text import Text, Sentence
from tokens import WordToken, PunctuationToken, Punctuation

reload(sys)
sys.setdefaultencoding('utf8')


###exception when config use questionmark true

class LineParser(AbstractParser):

    def __init__(self, file):
       self.file = file

    def parse(self):
        f = open(self.file, 'r')
        text = Text()
        sentence = Sentence()
        sentence.tokens = []

        i = 0
        for line in f:
            i += 1
            line = line.encode('utf8')
            line = line.rstrip() 
           # if line.startswith("\t"): 
            #    line = "dsjak" + line
             #   print line
            splittedLine = line.split('\t')
            word = unicode(splittedLine[0])
            period = unicode(splittedLine[1])
            sentence.tokens.extend(self.__createToken(word,period))
            if period == 'PERIOD':
                text.add_sentence(sentence)
                #print i, sentence
                sentence = Sentence()
                sentence.tokens = []

        f.close()
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

def main(file):
    parser = LineParser(file)
    texts = parser.parse()
    for text in texts:
        print(text)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python line_parser.py <file>")
        print("   file:      file contains lines with word and period value")
        sys.exit(0)

    file = sys.argv[1]

    if not (os.path.isfile(file)):
        print("No valid input file!")
        sys.exit(0)

    main(file)



