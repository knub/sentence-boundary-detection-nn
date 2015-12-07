import operator, os, shutil, sys, time, argparse

from common.argparse_util import *
from common.sbd_config import config
from parsing.line_parser import LineParser
from parsing.plaintext_parser import PlaintextParser
from parsing.xml_parser import XMLParser
from preprocessing.sliding_window import SlidingWindow
from preprocessing.tokens import Punctuation
from preprocessing.word2vec_file import Word2VecFile

from level_db_creator import LevelDBCreator

GOOGLE_VECTOR_FILE = "/home/fb10dl01/workspace/ms-2015-t3/GoogleNews-vectors-negative300.bin"
SMALL_VECTOR_FILE = "/home/ms2015t3/vectors.bin"
LEVEL_DB_DIR = "leveldbs"
CLASS_DISTRIBUTION_NORMALIZATION = config.getboolean('data', 'normalize_class_distribution')
CLASS_DISTRIBUTION_VARIANTION = 0.05
USE_QUESTION_MARK = config.getboolean('features', 'use_question_mark')



class TrainingInstanceGenerator(object):
    """reads the original data, process them and writes them to a level-db"""

    def __init__(self, vector_file):
        self.word2vec = Word2VecFile(vector_file)
        self.test_talks = set()

    def generate(self, parsers, database, is_test):
        level_db = LevelDBCreator(database)
        window_slider = SlidingWindow()
        # count how often each type (COMMA, PERIOD etc.) is in the instances
        class_distribution = dict()
        prev_progress = 0

        count = len(parsers)

        nr_instances = 0
        nr_instances_used = 0
        label_nr =  len(Punctuation)
        if not (USE_QUESTION_MARK): 
            label_nr -=  1
        perfect_distribution = label_nr / float(10)


        if is_test:
            plain_text_instances_file = open(database + "/../test_instances.txt", "w")
        else:
            plain_text_instances_file = open(database + "/../train_instances.txt", "w")

        for i, parser in enumerate(parsers):
 
            texts = parser.parse()

            for text in texts:
                progress = int(parser.progress() * 100)
                if progress > prev_progress:
                    sys.stdout.write(str(progress) + "% ")
                    sys.stdout.flush()
                    prev_progress = progress

                for sentence in text.sentences:
                    # get the word vectors for all token in the sentence
                    for token in sentence.get_tokens():
                        if not token.is_punctuation():
                            token.word_vec = self.word2vec.get_vector(token.word.lower())

                # get the training instances
                training_instances = window_slider.list_windows(text)

                # write training instances to level db
                for training_instance in training_instances:

                    ## calc class distribution
                   # print str(class_distribution.get(training_instance.label, 0))
                    nr_instances += 1
                    if is_test or (not CLASS_DISTRIBUTION_NORMALIZATION) or ((class_distribution.get(training_instance.label, 0) / float(max(nr_instances_used, 1))) - perfect_distribution <= CLASS_DISTRIBUTION_VARIANTION):
                      #  print str(training_instance.label) + " " + str(class_distribution.get(training_instance.label, 0) / max(nr_instances_used, 1))
                        s = unicode(training_instance) + "\n"
    #                    s = s + unicode(training_instance.get_array()) + "\n\n"
                        s += "\n"
                        plain_text_instances_file.write(s.encode('utf8'))
                        nr_instances_used += 1
                        class_distribution[training_instance.label] = class_distribution.get(training_instance.label, 0) + 1
                        level_db.write_training_instance(training_instance)

        plain_text_instances_file.close()
        print

        print("Orininally " + str(nr_instances) + " instances.")
        print("Created " + str(nr_instances_used) + " instances." )
        print("Class distribution:")
        print(class_distribution)

    def get_not_covered_words(self):
        return self.word2vec.not_covered_words


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create test and train datasets as a lmdb.')
    parser.add_argument('vector_file', metavar="vector_file {'small' or 'google'}", choices=['small', 'google'])
    parser.add_argument('data_folder', help='folder for lmdb creation')
    args = parser.parse_args()

    training_data = []
    test_data = []

    if args.vector_file == "google":
        vector_file = GOOGLE_VECTOR_FILE

        training_parsers = [
#            PlaintextParser("/home/ms2015t3/data/wikipedia-plaintexts"),
            XMLParser("/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/dev2010-w/IWSLT15.TED.dev2010.en-zh.en.xml"),
            XMLParser("/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/tst2010-w/IWSLT15.TED.tst2010.en-zh.en.xml"),
            XMLParser("/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/tst2012-w/IWSLT12.TED.MT.tst2012.en-fr.en.xml"),
            XMLParser("/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/tst2013-w/IWSLT15.TED.tst2013.en-zh.en.xml")
        ]

        test_parsers = [
            XMLParser("/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/tst2011/IWSLT12.TED.MT.tst2011.en-fr.en.xml")
        ]

    elif args.vector_file == "small":
        vector_file = SMALL_VECTOR_FILE

        training_parsers = [XMLParser("/home/ms2015t3/data/train-talk.xml")]
        test_parsers = [XMLParser("/home/ms2015t3/data/test-talk.xml")]

    sentence_home = os.environ['SENTENCE_HOME']

    database = sentence_home + "/" + LEVEL_DB_DIR + "/" + args.data_folder + \
        "_"      + config.get('windowing', 'window_size') + \
        "_"      + config.get('windowing', 'punctuation_position') + \
        "_pos-"  + config.get('features', 'pos_tagging') + \
        "_qm-"   + config.get('features', 'use_question_mark') + \
        "_word-" + config.get('word_vector', 'key_error_vector')
    if os.path.isdir(database):
        print("Deleting " + database + ". y/N?")
        s = raw_input()
        if s != "Y" and s != "y":
            print("Not deleting. Exiting ..")
            sys.exit(3)
        shutil.rmtree(database)

    os.mkdir(database)
    shutil.copy(sentence_home + "/python/config.ini", database)

    generator = TrainingInstanceGenerator(vector_file)
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
    print("")
    uncovered = generator.get_not_covered_words()
    print(sorted(uncovered.items(), key = operator.itemgetter(1)))
    print("Nr covered tokens: " + str(generator.word2vec.nr_covered_words))
    print("Nr uncovered tokens: " + str(generator.word2vec.nr_uncovered_words))
