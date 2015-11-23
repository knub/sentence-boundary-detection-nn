import sys
import os
import time

from talk_parser import TalkParser
import sliding_window
from word2vec_file import Word2VecFile
from level_db_creator import LevelDBCreator


GOOGLE_VECTOR_FILE = "/home/fb10dl01/workspace/ms-2015-t3/GoogleNews-vectors-negative300.bin"
SMALL_VECTOR_FILE = "/home/ms2015t3/vectors.bin"
LEVEL_DB_DIR = "/home/ms2015t3/sentence-boundary-detection-nn/leveldbs/"


class TrainingInstanceGenerator():
    """reads the original data, process them and writes them to a level-db"""

    def __init__(self, vector_file):
        self.word2vec = Word2VecFile(vector_file)
        self.test_talks = set()

    def generate(self, training_data, database, test):
        level_db = LevelDBCreator(LEVEL_DB_DIR + database)
        window_slider = sliding_window.SlidingWindow()
        # count how often each type (COMMA, PERIOD etc.) is in the instances
        class_distribution = dict()

        count = len(training_data)

        nr_instances = 0

        if test:
            plain_text_instances_file = open("../test_instances.txt", "w")
        else:
            plain_text_instances_file = open("../train_instances.txt", "w")

        for i, training_paths in enumerate(training_data):
            progress = int(i * 100.0 / count)
            sys.stdout.write(str(progress) + "% ")
            sys.stdout.flush()

            talk_parser = TalkParser(training_paths[0], training_paths[1])
            talks = talk_parser.list_talks()

            for talk in talks:
                if test:
                    self.test_talks.add(talk.id)
                if not test and talk.id in self.test_talks:
                    print("Skip talk %s for training! Talk is already in test set." % talk.id)
                    continue

                for sentence in talk.sentences:
                    # get the word vectors for all token in the sentence
                    for token in sentence.gold_tokens:
                        if not token.is_punctuation():
                            token.word_vec = self.word2vec.get_vector(token.word.lower())

                # get the training instances
                training_instances = window_slider.list_windows(talk)

                # write training instances to level db
                for training_instance in training_instances:
                    s = unicode(training_instance) + "\n"
                    s = s + unicode(training_instance.get_array()) + "\n\n"
                    plain_text_instances_file.write(s.encode('utf8'))
                    nr_instances += 1
                    class_distribution[training_instance.label] = class_distribution.get(training_instance.label, 0) + 1
                    level_db.write_training_instance(training_instance)

        plain_text_instances_file.close()
        print

        print("Created " + str(nr_instances) + " instances.")
        print("Class distribution:")
        print(class_distribution)

    def get_not_covered_words(self):
        return self.word2vec.not_covered_words


if __name__ == '__main__':

    argc = len(sys.argv)
    if argc != 3:
        print("Usage: " + sys.argv[0] + " [vector file - either 'small' or 'google'] [data_folder]")
        sys.exit(1)

    vector_file = sys.argv[1]

    training_data = []
    test_data = []

    if vector_file == "google":
        vector_file = GOOGLE_VECTOR_FILE

        training_data = [
            ("/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/dev2010-w/IWSLT15.TED.dev2010.en-zh.en.xml",
             "/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/dev2010-w/word-level transcript/dev2010.en.talkid<id>_sorted.txt"),
            ("/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/tst2010-w/IWSLT15.TED.tst2010.en-zh.en.xml",
             None),
            ("/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/tst2012-w/IWSLT12.TED.MT.tst2012.en-fr.en.xml",
             None),
            ("/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/tst2013-w/IWSLT15.TED.tst2013.en-zh.en.xml",
             None)
        ]
        test_data = [
            ("/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/tst2011/IWSLT12.TED.MT.tst2011.en-fr.en.xml",
             None)
        ]
    elif vector_file == "small":
        vector_file = SMALL_VECTOR_FILE

        training_data = [("/home/ms2015t3/data/train-talk.xml", None)]
        test_data = [("/home/ms2015t3/data/test-talk.xml", None)]
    else:
        print("Invalid vector file")
        sys.exit(2)

    data_folder = sys.argv[2]
    sentence_home = os.environ['SENTENCE_HOME']

    database = sentence_home + "/leveldbs/" + data_folder
    if os.path.isdir(database):
        print("Deleting " + sentence_home + "/leveldbs/" + data_folder + ". y/N?")
        s = raw_input()
        if s != "Y" and s != "y":
            print("Not deleting. Exiting ..")
            sys.exit(3)
        import shutil
        shutil.rmtree(database)

    os.mkdir(database)

    generator = TrainingInstanceGenerator(vector_file)
    print("Generating test data .. ")
    start = time.time()
    generator.generate(test_data, data_folder + "/test", test = True)
    duration = int(time.time() - start) / 60
    print("Done in " + str(duration) + " min.")
    print("Generating training data .. ")
    start = time.time()
    generator.generate(training_data, data_folder + "/train", test = False)
    duration = int(time.time() - start) / 60
    print("Done in " + str(duration) + " min.")
    print("")
    uncovered = generator.get_not_covered_words()
    print(sorted(uncovered.items(), key = operator.itemgetter(1)))
    print("Nr covered tokens: " + str(generator.word2vec.nr_covered_words))
    print("Nr uncovered tokens: " + str(generator.word2vec.nr_uncovered_words))
