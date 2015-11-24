import argparse, sys
from abstract_parser import AbstractParser
from nlp_pipeline import NlpPipeline
from text import Sentence, Text


TEXT_SEPARATOR = "################################################################################"

reload(sys)
sys.setdefaultencoding('utf8')

class PlaintextParser(AbstractParser):
    def __init__(self, filename):
        self.filename = filename
        self.nlp_pipeline = NlpPipeline()

    def parse(self):
        texts = []

        text = Text()

        with open(self.filename, "r") as file_:
            for line_unenc in file_:
                line = unicode(line_unenc.encode('utf8'))
                if line.startswith(TEXT_SEPARATOR):
                    if (len(text.sentences) > 0):
                        texts.append(text)
                        text = Text()
                    continue
                print "line", line
                sentences = self.nlp_pipeline.sentence_segmentation(line)
                for sentence in sentences:
                    print "sentence", sentence
                    s = Sentence()
                    s.set_sentence_text(sentence)
                    s.set_tokens(self.nlp_pipeline.parse_text(sentence))
                    text.add_sentence(s)

        texts.append(text)

        return texts


################
# Example call #
################

def main(filename):
    parser = PlaintextParser(filename)
    texts = parser.parse()
    for text in texts:
        print "text:"
        print(text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test the plain text file parsing')
    parser.add_argument('filename', help='the plain text file you want to parse')
    args = parser.parse_args()

    main(args.filename)
