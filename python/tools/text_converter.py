import operator, os, shutil, sys, time, argparse

from common.argparse_util import *
import common.sbd_config as sbd
from parsing.get_parser import *


class TextConverter(object):

    def convert(self, parsers):
        prev_progress = 0

        for i, text_parser in enumerate(parsers):
            texts = text_parser.parse()
            file_path = text_parser.get_file_name() + ".line"

            if os.path.isfile(file_path):
                print("Deleting " + file_path + ".")
                os.remove(file_path)
            print("Writing file %s ..." % file_path)

            for text in texts:
                progress = int(text_parser.progress() * 100)
                if progress > prev_progress:
                    sys.stdout.write(str(progress) + "% ")
                    sys.stdout.flush()
                    prev_progress = progress

                text.append_to_file(file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='converts files into line format.')
    parser.add_argument('config_file', help="path to config file")
    args = parser.parse_args()

    # initialize config
    sbd.SbdConfig(args.config_file)

    # get training and test data
    training_data = sbd.config.get('data', 'train_files').split(",")
    test_data = sbd.config.get('data', 'test_files').split(",")

    data_folder = "/mnt/naruto/sentence/data/"

    # get training parsers
    training_parsers = []
    for f in training_data:
        parser = get_parser(data_folder + f)
        if parser is None:
            print("WARNING: Could not find training parser for file %s!" % f)
        else:
            training_parsers.append(parser)

    # get test parsers
    test_parsers = []
    for f in test_data:
        parser = get_parser(data_folder + f)
        if parser is None:
            print("WARNING: Could not find test parser for file %s!" % f)
        else:
            test_parsers.append(parser)

    # convert data
    converter = TextConverter()
    print("Converting data .. ")
    start = time.time()
    converter.convert(test_parsers)
    duration = int(time.time() - start) / 60
    print("Done in " + str(duration) + " min.")
    start = time.time()
    converter.convert(training_parsers)
    duration = int(time.time() - start) / 60
    print("Done in " + str(duration) + " min.")
