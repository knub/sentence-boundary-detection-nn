import sys, argparse, os

from common.argparse_util import *
import common.sbd_config as sbd
from preprocessing.nlp_pipeline import NlpPipeline, PosTag
from preprocessing.text import Text, Sentence, END_OF_TEXT_MARKER
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
        # if sbd.config.getboolean('features', 'use_question_mark'):
        #     raise ValueError("Question marks not supported by LineParser")

        self.POS_TAGGING = sbd.config.getboolean('features', 'pos_tagging')
        self.nlp_pipeline = NlpPipeline()

    def _wanted_file_endings(self):
        return (".line", )

    def parse(self):
        with open(self.filename, "r") as file_:
            text = Text()
            sentence = Sentence()
            sentence.tokens = []

            for line_unenc in file_:
                # end of a text reached
                if line_unenc == END_OF_TEXT_MARKER:
                    yield text
                    text = Text()

                self._progress += 1

                # parse line
                line = unicode(line_unenc, errors='ignore')
                line = line.rstrip()

                # split line into word, pos_tags and type
                line_parts = line.split('\t')
                word = self._get_word(line_parts)
                if word is None:
                    continue
                pos_tags = self._get_pos_tags(line_parts)
                punctuation = self._get_punctuation(line_parts)

                sentence.tokens.extend(self._create_tokens(word, pos_tags, punctuation))

                # we are at the end of a sentence
                if punctuation == 'PERIOD':
                    if self.POS_TAGGING and not pos_tags:
                        self.nlp_pipeline.pos_tag(sentence.tokens)
                    text.add_sentence(sentence)
                    sentence = Sentence()
                    sentence.tokens = []

        # if we do not have any end-of-text-marker
        # return everything as one text
        if len(text.sentences) > 0:
            yield text

    def _get_word(self, line_parts):
        word = unicode(line_parts[0])
        word = self.nlp_pipeline.process_word(word)
        # check if needed
        # if "?" in word and len(word) > 0:
        #     word = word.replace("?", "")
        return word

    def _get_punctuation(self, line_parts):
        if len(line_parts) == 2:
            return unicode(line_parts[2])
        else:
            return unicode(line_parts[2])

    def _get_pos_tags(self, line_parts):
        if len(line_parts) == 2:
            return set()
        else:
            pos_tag_str = line_parts[1].split(",")
            pos_tag_types = map(lambda x: x.split(".")[1], pos_tag_str)
            return set(map(lambda x: PosTag[x], pos_tag_types))

    def progress(self):
        return self._line_count_progress()
 
    def _create_tokens(self, word, pos_tags, punctuation):
        word_token = WordToken(word)
        word_token.set_pos_tags(pos_tags)
        
        punctuation_token = None
        if punctuation == 'PERIOD':
            punctuation_token = PunctuationToken(punctuation, Punctuation.PERIOD)
        elif punctuation == 'COMMA':
            punctuation_token = PunctuationToken(punctuation, Punctuation.COMMA)

        if punctuation_token is not None:
            return [word_token, punctuation_token]
        return [word_token]



################
# Example call #
################

if __name__ == '__main__':
    parse_command_line_arguments(LineParser)
