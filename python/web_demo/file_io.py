import common.sbd_config as sbd
from sbd_classification.util import convert_probabilities

class ResultWriter (object):

    def __init__(self, classes = ["NONE", "COMMA", "PERIOD"]):
       self.PUNCTUATION_POS = sbd.config.getint('windowing', 'punctuation_position')
       self.classes = classes
       self.separator = " "

    def writeToFile(self, file_name, tokens, punctuation_probs):
        with open(file_name, "w") as f:
            header = "%s\n" % (self.separator.join(["TOKEN"] + self.classes))
            f.write(header)

            for i, token in enumerate(tokens):
                f.write("%s\n" % self.separator.join(str(prob) for prob in ([token] + punctuation_probs[i])))


class InputTextReader (object):

    def __init__(self):
        pass

    def readFile(self, file_name):
        text = ""
        with open(file_name, "r") as f:
            for line in f.readlines():
                word = line.split("\t")[0]
                text += " " + word

        return text
