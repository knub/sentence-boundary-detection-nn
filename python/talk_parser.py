import xml.etree.ElementTree
import sys
import os.path
import re
from nlp_pipeline import NlpPipeline


class XMLParser(object):
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.nlp_pipeline = NlpPipeline()

    def parse(self):
        talks = []

        mteval = xml.etree.ElementTree.parse(self.xml_file).getroot()
        srcset = mteval.find("srcset")
        for doc in srcset.findall('doc'):
            talk = Text()

            for sentence in doc.findall("seg"):
                sentence_text = unicode(sentence.text)

                sentence = Sentence()
                sentence.set_sentence_text(sentence_text)
                sentence.set_tokens(self.nlp_pipeline.parse_text(sentence_text))
                talk.add_sentence(sentence)

            talks.append(talk)

        return talks


################
# Example call #
################

def main(xml_file, template_file = None):
    parser = TalkParser(xml_file, template_file)
    talks = parser.list_talks()
    for talk in talks:
        print(talk)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python talk_parser.py <xml_file> <template_file>")
        print("   xml_file:      XML file containing talks.")
        print("   template_file: Template file path to sorted_txt transcript file. Contains <id> for talk id, which will be replaced.")
        sys.exit(0)

    xml_file = sys.argv[1]
    
    template_file = None
    if len(sys.argv) == 3:
        template_file = sys.argv[2]

    if not (os.path.isfile(xml_file)):
        print("No valid input xml file!")
        sys.exit(0)

    main(xml_file, template_file)
