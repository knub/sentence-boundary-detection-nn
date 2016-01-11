import sys, argparse, os

import re
from common.argparse_util import *
import common.sbd_config as sbd
from preprocessing.nlp_pipeline import NlpPipeline, PosTag
from preprocessing.audio import Audio, AudioSentence
from preprocessing.tokens import AudioToken, PunctuationToken, Punctuation

from abstract_parser import AbstractParser, main, parse_command_line_arguments

reload(sys)
sys.setdefaultencoding('utf8')


class CtmParser(AbstractParser):

    def __init__(self, filename):
        super(CtmParser, self).__init__(filename)
        if not self.wants_this_file():
            return

        self._init_line_count_progress()

    def _wanted_file_endings(self):
        return (".ctm",)

    def parse(self):
        current_talk_id = 0
        audio = Audio()
        sentence = AudioSentence()
        sentence.tokens = []

        group_name = self._extract_group_name()

        with open(self.filename, "r") as file_:
            for line_unenc in file_:
                self._progress += 1

                # parse line
                line = unicode(line_unenc, errors='ignore')
                line = line.rstrip()

                if line.startswith("#"):
                    talk_id = self._extract_talk_id(line)
                    token_count = len(sentence.tokens)

                    # end of talk reached
                    if talk_id != current_talk_id:
                        if token_count > 0:
                            audio.talk_id = current_talk_id
                            audio.group_name = group_name
                            audio = self._prepare_audio(audio)
                            yield audio
                            audio = Audio()
                            current_talk_id = talk_id
                            continue
                        else:
                            current_talk_id = talk_id

                    # we are still in the same talk, a new sentence is starting
                    else:
                        # save old sentence
                        if token_count > 0:
                            sentence.begin = sentence.tokens[0].begin
                            sentence.end = sentence.tokens[-1].begin + sentence.tokens[-1].duration
                            sentence.append_token(PunctuationToken(".", Punctuation.PERIOD))
                            audio.add_sentence(sentence)
                        sentence = AudioSentence()
                        sentence.tokens = []

                else:
                    # parse line
                    line_parts = re.split(" +", line)
                    begin = float(line_parts[2])
                    duration = float(line_parts[3])
                    word = line_parts[4]

                    # add token to sentence
                    token = AudioToken(word.lower())
                    token.begin = begin
                    token.duration = duration

                    sentence.append_token(token)

        if len(audio.sentences) > 0:
            audio.talk_id = current_talk_id
            audio.group_name = group_name
            audio = self._prepare_audio(audio)
            yield audio

    def _extract_group_name(self):
        return self.filename.split("_")[0].split("/")[-1]

    def _prepare_audio(self, audio):
        # sort sentences by begin
        sorted_sentences = sorted(audio.sentences, key=lambda x: x.begin)
        audio.sentences = sorted_sentences

        # calculate pause before and pause after
        return self._calculate_pause(audio)

    def _calculate_pause(self, audio):
        last_end = 0.0
        last_token = None

        for token in audio.get_tokens():
            if token.is_punctuation():
                continue

            pause = float(format(token.begin - last_end, '.4f'))

            if pause < 0.0 or pause == -0.0:
                pause = 0.0

            token.set_pause_before(pause)
            if last_token is not None:
                last_token.set_pause_after(pause)

            last_end = token.begin + token.duration
            last_token = token

        return audio

    def _extract_talk_id(self, line):
        line = line[2:]
        line_parts = line.split("_")
        for p in line_parts:
            if p.startswith("talkid"):
                return p[6:]
        return 0

    def progress(self):
        return self._line_count_progress()


################
# Example call #
################

if __name__ == '__main__':
    parse_command_line_arguments(CtmParser)
