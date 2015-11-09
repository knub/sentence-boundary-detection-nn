import xml.etree.ElementTree
import sys
import os.path
import re
from enum import Enum

import nltk

import sbd_token


class Punctuation(Enum):
    COMMA = 1
    PERIOD = 2
    QUESTION = 3


class Talk(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.sentences = []

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def __str__(self):
        sentences_str = ''.join(map(str, self.sentences))
        return " ID: %s \n TITLE: %s \n \n %s" % (self.id, self.title, sentences_str)


class Sentence(object):
    punctuation_mapping = {
        ";": Punctuation.PERIOD,
        ".": Punctuation.PERIOD,
        "!": Punctuation.PERIOD,
        ",": Punctuation.COMMA,
        ":": Punctuation.COMMA,
        "-": Punctuation.COMMA,
        "?": Punctuation.QUESTION
    }

    def __init__(self, id, original_gold_text):

        self.id = id
        self.gold_text = self.parse_text(original_gold_text)
        self.original_gold = original_gold_text
        self.time_start = 0
        self.time_end = 0
        self.speech_text = ""
        self.enriched_speech_text = ""

    def set_time_start(self, time_start):
        self.time_start = time_start

    def set_time_end(self, time_end):
        self.time_end = time_end

    def set_gold_text(self, gold_text):
        self.gold_text = gold_text

    def set_speech_text(self, speech_text):
        self.speech_text = speech_text

    def set_enriched_speech_text(self, enriched_speech_text):
        self.enriched_speech_text = enriched_speech_text

    def __str__(self):
        return " ID: %s \n TIME_START: %s \n TIME_END: %s \n gold_text: %s \n speech_text: %s \n enriched_speech_text: %s \n" % (
        self.id, self.time_start, self.time_end, self.gold_text, self.speech_text,
        self.enriched_speech_text)

    def parse_text(self, text):
        raw_tokens = nltk.word_tokenize(text)
        # pos_tags = nltk.pos_tag(raw_tokens)
        tokens = []

        for i in range(0, len(raw_tokens)):
            if raw_tokens[i] in self.punctuation_mapping:
                tokens.append(sbd_token.PunctuationToken(raw_tokens[i],
                                                         self.punctuation_mapping[raw_tokens[i]]))
            else:
                word_token = sbd_token.WordToken(raw_tokens[i])
                #                word_token.set_pos_tag(pos_tags[i][1])
                tokens.append(word_token)
        return tokens


class TalkParser(object):
    def __init__(self, xml_file, template_file):
        self.xml_file = xml_file
        self.template_file = template_file

    def list_talks(self):
        talks = self.__parse_xml_file()

        for talk in talks:
            if self.template_file != None:
                file_name = self.template_file.replace("<id>", talk.id)
                self.__parse_txt_file(talk, file_name)

        return talks


    def __parse_xml_file(self):
        talks = []

        mteval = xml.etree.ElementTree.parse(self.xml_file).getroot()
        srcset = mteval.find("srcset")
        for doc in srcset.findall('doc'):
            talk_id = doc.find("talkid").text
            talk_title = doc.find("title").text

            talk = Talk(talk_id, talk_title)

            for sentence in doc.findall("seg"):
                sentence_id = sentence.attrib["id"]
                sentence_text = sentence.text

                talk.add_sentence(Sentence(sentence_id, sentence_text))

            talks.append(talk)

        return talks

    def __parse_txt_file(self, talk, txt_file):
        f = open(txt_file)
        for i, line in enumerate(f):
            parts = line.split(" ")
            time_start = parts[1]
            time_end = parts[2]
            (speech_text, enriched_speech_text) = self.__clean_sentence(" ".join(parts[3:]))

            talk.sentences[i].set_time_start(time_start)
            talk.sentences[i].set_time_end(time_end)
            talk.sentences[i].set_speech_text(speech_text)
            talk.sentences[i].set_enriched_speech_text(enriched_speech_text)

        return talk

    def __clean_sentence(self, unclean_sentence):
        unclean_sentence = unclean_sentence.replace("\n", "")
        enriched_speech_text = re.sub(r'\(\d\)', "", unclean_sentence)
        speech_text = re.sub(r'{\$\(.*?\)} ', "", enriched_speech_text)

        return (speech_text, enriched_speech_text)


def main(xml_file, template_file):
    parser = TalkParser(xml_file, template_file)
    talks = parser.list_talks()
    for talk in talks:
        print(talk)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python talk_parsing.py <xml_file> <template_file>")
        print("   xml_file:      XML file containing talks.")
        print("   template_file: Template file path to sorted_txt transcript file. Contains <id> for talk id, which will be replaced.")
        sys.exit(0)

    xml_file = sys.argv[1]
    template_file = sys.argv[2]

    if not (os.path.isfile(xml_file)):
        print("No valid input xml file!")
        sys.exit(0)

    main(xml_file, template_file)
