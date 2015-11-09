import sys,argparse,numpy,struct


ENCODING = 'UTF-8'

class Word2VecFile():
  """reads a binary word vector file, returns vectors for single words"""
  def __init__(self, filename):
    # einlesen
    self.__filename = filename
    try:
      self.__file = open(filename, 'br')
    except IOError:
      parser.error('The file %s can not be read!' % self.__filename)
    first_line = self.__file.readline().decode(ENCODING).split(' ')
    self.words = int(first_line[0])
    self.vector_size = int(first_line[1])
    print ('File has %d words with %d vectors. Parsing ...' % (self.words, self.vector_size))
    self.vector_array = numpy.zeros((self.words, self.vector_size), numpy.float32)
    self.word2index = {}

    chars = []
    for w_index in range(0, self.words):
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
    self.__file.close()
    print ('Parsing finished!')

  def __del__(self):
    self.vector_array = None
    self.word2index = None

  def get_vector(self, word):
    return self.vector_array[self.word2index[word]]

def main(args):
  word2VecFile = Word2VecFile(args.datafile)
  for word in args.word:
    try:
      print (word, word2VecFile.get_vector(word))
    except KeyError:
      print (word, "not found!")

def is_valid_file(parser, arg, mode):
  try:
    f = open(arg, mode)
    f.close()
    return arg
  except IOError:
    parser.error('The file %s can not be opened!' % arg)

if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Get word vector from binary data.')
  parser.add_argument('datafile', help='path to binary data file', type=lambda x: is_valid_file(parser, x, 'br'))
  parser.add_argument('word', help='word to find in data file', nargs='+')
  args = parser.parse_args()
  main(args)
