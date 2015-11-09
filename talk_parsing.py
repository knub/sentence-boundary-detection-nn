import xml.etree.ElementTree
import sys
import os.path
import re


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

    def __init__(self, id, punctuated):
        self.id = id
        self.punctuated = punctuated
        self.time_start = 0
        self.time_end = 0
        self.non_punctuated = ""
        self.annotated = ""

    def set_time_start(self, time_start):
        self.time_start = time_start

    def set_time_end(self, time_end):
        self.time_end = time_end

    def set_punctuated(self, punctuated):
        self.punctuated = punctuated

    def set_non_punctuated(self, non_punctuated):
        self.non_punctuated = non_punctuated

    def set_annotated(self, annotated):
        self.annotated = annotated

    def __str__(self):
        return " ID: %s \n TIME_START: %s \n TIME_END: %s \n PUNCTUATED: %s \n NUN_PUNCTUATED: %s \n ANNOTATED: %s \n" % (self.id, self.time_start, self.time_end, self.punctuated, self.non_punctuated, self.annotated)


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
            (non_punctuated, annotated) = self.__clean_sentence(" ".join(parts[3:]))

            talk.sentences[i].set_time_start(time_start)
            talk.sentences[i].set_time_end(time_end)
            talk.sentences[i].set_non_punctuated(non_punctuated)
            talk.sentences[i].set_annotated(annotated)

        return talk

    def __clean_sentence(self, unclean_sentence):
        unclean_sentence = unclean_sentence.replace("\n", "")
        annotated = re.sub(r'\(\d\)', "", unclean_sentence)
        non_punctuated = re.sub(r'{\$\(.*?\)} ', "", annotated)

        return (non_punctuated, annotated)


def main(xml_file, template_file):
    parser = TalkParser(xml_file, template_file)
    talks = parser.list_talks()
    for talk in talks:
        print(talk)


if __name__=='__main__':
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
