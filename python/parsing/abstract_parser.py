import os, argparse

from common.argparse_util import *

class AbstractParser(object):
    """AbstractParser with standard filename methods, parse method has to be implemented by subclass"""
    def __init__(self, filename):
        self.filename = filename

    def _wanted_file_endings(self):
        """returns a list of file endings, that can be parsed by this parser"""
        raise NotImplementedError("to be implemented by subclass")

    def wants_this_file(self):
        basepath, extension = os.path.splitext(self.filename)
        return extension in self._wanted_file_endings()

    def get_file_name(self):
        return os.path.basename(self.filename)

    def parse(self):
        """returns a list of talks, it is recommended to use the python generator for less memory usage"""
        raise NotImplementedError("to be implemented by subclass")

    def progress(self):
        """progress of parsing, should be implemented for parsers with large file sizes"""
        raise NotImplementedError("to be implemented by subclass")

    def _no_progress_function(self):
        return 0.

    def _line_count_progress(self):
        return float(self._progress) / self._linenumber

    def _init_line_count_progress(self):
        i = -1
        with open(self.filename) as f:
            for i, line in enumerate(f):
                pass
        self._linenumber = i + 1
        self._progress = 0


def main(filename, class_):
    parser = class_(filename)
    texts = parser.parse()
    for i, text in enumerate(texts):
        print "progress %f, text %d:" % (parser.progress(), i)
        print text

def parse_command_line_arguments(class_):
    parser = argparse.ArgumentParser(description='Test the file parsing')
    parser.add_argument('filename', help='the file you want to parse', type=lambda arg: is_valid_file(parser, arg))
    args = parser.parse_args()

    main(args.filename, class_)
