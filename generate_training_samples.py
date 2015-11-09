import sys
import talk_parsing
import sliding_window
import word2vec_file
import create_level_db


WORD_VECTOR_FILE = "/home/fb10dl01/workspace/ms-2015-t3/GoogleNews-vectors-negative300.bin"
LEVEL_DB_DIR = "/home/ms2015t3/sentence-boundary-detection-nn/leveldbs"

class TrainingSampleGenerator():

    def generate(self, training_data):

        for training_paths in training_data:
            talk_parser = talk_parsing.TalkParser(training_paths[0], training_paths[1])
            talks = talk_parser.list_talks()

            window_slider = sliding_window.SlidingWindow()
            word2Vec = word2vec_file.Word2VecFile(WORD_VECTOR_FILE)
            level_db = create_level_db.CreateLevelDB(LEVEL_DB_DIR)

            for talk in talks:
                for sentence in talk.sentences:
                    # get the word vectors for all token in the sentence
                    for token in sentence.gold_text:
                        token.word_vec = word2Vec.get_vector(token)

                    # get the training instances
                    training_instance = window_slider.list_windows(sentence)

                    # write training instances to level db
                    level_db.write_training_instance(training_instance)

                    # print (training_instance)


if __name__=='__main__':

    training_data = [
       # ("/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/dev2010-w",
       #     "/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/dev2010/word-level transcript/dev2010.en.talkid<id>_sorted.txt")

        ("/home/rice/Windows/uni/master4/paomr/Dataset/dev2010-w/IWSLT15.TED.dev2010.en-zh.en.xml", None)
    ]

    TrainingSampleGenerator.generate(training_data)
