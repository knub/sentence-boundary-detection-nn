import xml.etree.ElementTree
import sys
import os.path
import re


class Talk(object):

    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.sentences = []

    def addSentence(self, sentence):
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

    def setTimeStart(self, time_start):
        self.time_start = time_start

    def setTimeEnd(self, time_end):
        self.time_end = time_end

    def setPunctuated(self, punctuated):
        self.punctuated = punctuated

    def setNonPunctuated(self, non_punctuated):
        self.non_punctuated = non_punctuated

    def setAnnotated(self, annotated):
        self.annotated = annotated

    def __str__(self):
        return " ID: %s \n TIME_START: %s \n TIME_END: %s \n PUNCTUATED: %s \n NUN_PUNCTUATED: %s \n ANNOTATED: %s \n" % (self.id, self.time_start, self.time_end, self.punctuated, self.non_punctuated, self.annotated)



def parseXMLFile(xml_file):
    talks = []

    mteval = xml.etree.ElementTree.parse(xml_file).getroot()
    srcset = mteval.find("srcset")
    for doc in srcset.findall('doc'):
        talk_id = doc.find("talkid").text
        talk_title = doc.find("title").text

        talk = Talk(talk_id, talk_title)

        for sentence in doc.findall("seg"):
            sentence_id = sentence.attrib["id"]
            sentence_text = sentence.text

            talk.addSentence(Sentence(sentence_id, sentence_text))

        talks.append(talk)

    return talks


def parseTxtFile(txt_file, talk):
    f = open(txt_file)
    for i, line in enumerate(f):
        parts = line.split(" ")
        time_start = parts[1]
        time_end = parts[2]
        (non_punctuated, annotated) = cleanSentence(" ".join(parts[3:]))

        talk.sentences[i].setTimeStart(time_start)
        talk.sentences[i].setTimeEnd(time_end)
        talk.sentences[i].setNonPunctuated(non_punctuated)
        talk.sentences[i].setAnnotated(annotated)

    return talk


def cleanSentence(uncleanSentence):
    uncleanSentence = uncleanSentence.replace("\n", "")
    annotated = re.sub(r'\(\d\)', "", uncleanSentence)
    non_punctuated = re.sub(r'{\$\(.*?\)} ', "", annotated)

    return (non_punctuated, annotated)


def main():
    talks = parseXMLFile(xml_file)

    for talk in talks:
        file_name = transcript_file.replace("<id>", talk.id)
        parseTxtFile(file_name, talk)


    for talk in talks:
        print(talk)





if len(sys.argv) != 3:
    print("Usage: python talk_parsing.py <xml_file> <sorted_uncleaned_transcript_file>")
    sys.exit(0)


xml_file = sys.argv[1]
transcript_file = sys.argv[2]

if not (os.path.isfile(xml_file)):
    print("No valid input file!")
    sys.exit(0)

main()


