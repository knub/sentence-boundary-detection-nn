import sys,argparse,numpy


class Word2VecFile():
  """reads a binary word vector file, returns vectors for single words"""
  def __init__(self, filename):
    # einlesen
    self.__filename = filename
    try:
      self.__file = open(filename, 'br')
    except IOError:
      parser.error('The file %s can not be read!' % self.__filename)

  def __del__(self):
    self.__file.close()
    # clean up memory
    print ("Cleaned up Word2VecFile class.")

  def get_vector(self, word):
    pass

def main(args):
  try:
    wordfile = open(args.wordfile, 'br')
  except IOError:
    parser.error('The file %s can not be read!' % self.__filename)
  word2VecFile = Word2VecFile(args.datafile)
  for word in wordfile.readlines():
    print (word, word2VecFile.get_vector(word))
  wordfile.close()

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
  parser.add_argument('wordfile', help='path to word data file, one word per line', type=lambda x: is_valid_file(parser, x, 'r'))
  args = parser.parse_args()
  main(args)
