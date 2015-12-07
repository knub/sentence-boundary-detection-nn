import sys, argparse, struct, numpy
from common.sbd_config import config

ENCODING = 'UTF-8'
KEY_ERROR_VECTOR = config.get('word_vector', 'key_error_vector')


class GloveFile(object):
    """reads a binary word vector file, returns vectors for single words"""

    def __init__(self, filename):
        # the following variable counts word, that are not covered in the given vector
        # see get_vector for details
        self.not_covered_words = dict()
        # and some bare numbers
        self.nr_covered_words = 0
        self.nr_uncovered_words = 0
        # read vector file
        self.__filename = filename

        try:
            self.__file = open(filename, 'rb')
        except IOError:
            print ('The file %s can not be read!' % self.__filename)
            return

        self.words = 400000
        self.vector_size = 50

        self.vector_array = numpy.zeros((self.words, self.vector_size), float)
        self.word2index = {}
        self.average_vector = numpy.zeros((self.vector_size,), float)

        index = 0
        with open(filename) as f:
            for line in f:
                if index % 100000 == 0:
                    print("Parsed %d/%d lines." % (index, self.words))
                parts = line.split(" ")
                word = parts[0]
                vector = parts[1:]

                self.word2index[word] = index
                for i in range (len(vector)):
                    self.vector_array[index][i] = float(vector[i])

                index += 1

        self.__file.close()
        print('Parsing finished!')

    def __del__(self):
        self.vector_array = None
        self.word2index = None

    def get_vector(self, word):
        try:
            idx = self.word2index[word]
            self.nr_covered_words += 1
            return self.vector_array[idx]
        except KeyError:
            self.not_covered_words[word] = self.not_covered_words.get(word, 0) + 1
            self.nr_uncovered_words += 1
            if KEY_ERROR_VECTOR != 'avg':
                idx = self.word2index[KEY_ERROR_VECTOR]
                return self.vector_array[idx]
            else:
                return self.average_vector
