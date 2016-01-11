import sys, argparse, os

from common.argparse_util import *
from line_parser import LineParser
from plaintext_parser import PlaintextParser
from xml_parser import XMLParser
from ctm_parser import CtmParser


def get_parser(filename):
    parsers = []
    parsers.append(PlaintextParser(filename))
    try:
        parsers.append(LineParser(filename))
    except ValueError:
        pass
    parsers.append(XMLParser(filename))
    parsers.append(CtmParser(filename))

    for parser in parsers:
        if parser.wants_this_file():
            return parser

    return None

def main(filename):
    parser = get_parser(filename)
    if parser:
        texts = parser.parse()
        for i, text in enumerate(texts):
            print "progress %f, text %d:" % (parser.progress(), i)
            print text
    else:
        print "#error: no suitable parser for %s found, sorry." % filename

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test the file parsing')
    parser.add_argument('filename', help='the file you want to parse', type=lambda arg: is_valid_file(parser, arg))
    args = parser.parse_args()

    main(args.filename)
