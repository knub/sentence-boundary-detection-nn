import sys
import talk_parsing
import sliding_window



class TrainingSampleGenerator():


    def generate(training_data):

        for trainingpaths in training_data:
            talk_parser = talk_parsing.TalkParser(trainingpaths[0], trainingpaths[1])
            talks = talk_parser.list_talks()

            window_slider = sliding_window.SlidingWindow()

            for talk in talks:
                for sentence in talk.sentences:
                    
                    training_sample = window_slider.list_windows(sentence)
                    # print (training_sample)

if __name__=='__main__':

    training_data = [
       # ("/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/dev2010-w",
       #     "/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/dev2010/word-level transcript/dev2010.en.talkid<id>_sorted.txt")

        ("/home/rice/Windows/uni/master4/paomr/Dataset/dev2010-w/IWSLT15.TED.dev2010.en-zh.en.xml", None)
    ]

    TrainingSampleGenerator.generate(training_data)
    