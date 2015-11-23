import sys
import argparse
import struct

import numpy


ENCODING = 'UTF-8'


class Word2VecFile():
    """reads a binary word vector file, returns vectors for single words"""
    def __init__(self, filename, use_this_vector=True):
        # the following variable counts word, that are not covered in the given vector
        # see get_vector for details
        self.not_covered_words = dict()
        # and some bare numbers
        self.nr_covered_words = 0
        self.nr_uncovered_words = 0
        # if self.use_this_vector is True, we return 'this' vector for unknown words
        # otherwise the average vector is returned
        self.use_this_vector = use_this_vector
        # read vector file
        self.__filename = filename
        try:
            self.__file = open(filename, 'rb')
        except IOError:
            print ('The file %s can not be read!' % self.__filename)
            return
        first_line = self.__file.readline().decode(ENCODING).split(' ')
        self.words = int(first_line[0])
        self.vector_size = int(first_line[1])
        print('File has %d words with vectors of size %d. Parsing ..' % (self.words, self.vector_size))
        self.vector_array = numpy.zeros((self.words, self.vector_size), float)
        self.word2index = {}

        self.average_vector = numpy.zeros((self.vector_size,), float)
        progress_steps = self.words / 100

        chars = []
        for w_index in range(0, self.words):
            if w_index % progress_steps == 0:
                progress = w_index * 100 / self.words
                sys.stdout.write(str(progress) + "% ")
                sys.stdout.flush()
            byte = self.__file.read(1)
            while byte:
                if byte == b" ":
                    word = b"".join(chars)
                    self.word2index[word.decode(ENCODING)] = w_index
                    chars = []
                    break
                if byte != b"\n":
                    chars.append(byte)
                byte = self.__file.read(1)
            for f_index in range(0, self.vector_size):
                f_bytes = self.__file.read(4)
                self.vector_array[w_index][f_index] = struct.unpack('f', f_bytes)[0]
            self.average_vector += self.vector_array[w_index]
        self.__file.close()
        self.average_vector /= self.words
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
            if self.use_this_vector:            
                idx = self.word2index['this']
                return self.vector_array[idx]
            else:
                return self.average_vector


################
# Example call #
################

def main(args):
    word2VecFile = Word2VecFile(args.datafile)
    for word in args.word:
        try:
            print(word, word2VecFile.get_vector(word))
        except KeyError:
            print(word, "not found!")

def is_valid_file(parser, arg, mode):
    try:
        f = open(arg, mode)
        f.close()
        return arg
    except IOError:
        parser.error('The file %s can not be opened!' % arg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get word vector from binary data.')
    parser.add_argument('datafile', help='path to binary data file',
                        type=lambda x: is_valid_file(parser, x, 'rb'))
    parser.add_argument('word', help='word to find in data file', nargs='+')
    args = parser.parse_args()
    main(args)
