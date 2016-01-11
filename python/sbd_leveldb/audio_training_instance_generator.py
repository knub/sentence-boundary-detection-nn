import operator, os, shutil, sys, time, argparse

from common.argparse_util import *
import common.sbd_config as sbd
from preprocessing.sliding_window import SlidingWindow
from preprocessing.tokens import Punctuation
from preprocessing.word2vec_file import Word2VecFile
from preprocessing.glove_file import GloveFile
from parsing.get_parser import *
from level_db_creator import LevelDBCreator


class TrainingInstanceGenerator(object):
    """reads the original data, process them and writes them to a level-db"""

    def __init__(self):
        self.test_talks = set()

    def generate(self, parsers, database, is_test):
        level_db = LevelDBCreator(database)
        window_slider = SlidingWindow()

        nr_instances = 0

        if is_test:
            plain_text_instances_file = open(database + "/../test_instances.txt", "w")
        else:
            plain_text_instances_file = open(database + "/../train_instances.txt", "w")

        for i, talk_parser in enumerate(parsers):
            talks = talk_parser.parse()

            prev_progress = 0
            print("")
            print("Processing file %s ..." % talk_parser.get_file_name())

            for talk in talks:
                progress = int(talk_parser.progress() * 100)
                if progress > prev_progress:
                    sys.stdout.write(str(progress) + "% ")
                    sys.stdout.flush()
                    prev_progress = progress

                # get pitch feature values
                pitch_level_file = talk_parser.get_file_name().replace(".ctm", ".pitch")
                talk.parse_pith_feature(pitch_level_file)

                # get the training instances
                training_instances = window_slider.list_windows(talk)

                # write training instances to level db
                for training_instance in training_instances:
                    nr_instances += 1

                    # write instance to file
                    s = unicode(training_instance) + "\n"
                    s += "\n"
                    plain_text_instances_file.write(s.encode('utf8'))

                    # write to level db
                    level_db.write_training_instance(training_instance)

        plain_text_instances_file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create test and train datasets as a lmdb.')
    parser.add_argument('config_file', help="path to config file")
    args = parser.parse_args()

    # initialize config
    sbd.SbdConfig(args.config_file)

    # create proper name for the database
    SENTENCE_HOME = os.environ['SENTENCE_HOME']
    data_folder = "/mnt/naruto/sentence/data/"
    LEVEL_DB_DIR = "leveldbs"

    database = SENTENCE_HOME + "/" + LEVEL_DB_DIR + "/" + sbd.SbdConfig.get_db_name_from_config(sbd.config)

    # check if database already exists
    if os.path.isdir(database):
        print("Deleting " + database + ". y/N?")
        sys.stdout.flush()
        s = raw_input()
        if s != "Y" and s != "y":
            print("Not deleting. Exiting ..")
            sys.exit(3)
        shutil.rmtree(database)

    # create database folder and copy config file
    os.mkdir(database)
    shutil.copy(args.config_file, database)

    # get training and test data
    training_data = sbd.config.get('data', 'train_files').split(",")
    test_data = sbd.config.get('data', 'test_files').split(",")

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

    # generate data
    generator = TrainingInstanceGenerator()

    print("Generating test data .. ")
    start = time.time()
    generator.generate(test_parsers, database + "/test", is_test = True)
    duration = int(time.time() - start) / 60
    print("Done in " + str(duration) + " min.")

    print("Generating training data .. ")
    start = time.time()
    generator.generate(training_parsers, database + "/train", is_test = False)
    duration = int(time.time() - start) / 60
    print("Done in " + str(duration) + " min.")
