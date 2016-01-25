import common.sbd_config as sbd

class ResultWriter (object):

    def __init__(self):
       self.PUNCTUATION_POS = sbd.config.getint('windowing', 'punctuation_position')
       self.classes = ["NONE", "COMMA", "PERIOD"]
       self.separator = " "

    def writeToFile(self, file_name, tokens, punctuation_probs):
       with open(file_name, "w") as f:

         header = "TOKEN NONE COMMA PERIOD \n"
         f.write(header)

         for i, token in enumerate(tokens):
                current_prediction_position = i - self.PUNCTUATION_POS + 1
                content = ""
                if 0 <= current_prediction_position and current_prediction_position < len(punctuation_probs):
                    current_probs = punctuation_probs[current_prediction_position]
                    content = "%s%s%s%s%s%s%s\n" % (token, self.separator, current_probs[0], self.separator, current_probs[1], self.separator, current_probs[2])
                else:
                    content = "%s%s%s%s%s%s%s\n" % (token, self.separator, 1.0, self.separator, 0.0, self.separator, 0.0)

                f.write(content)


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