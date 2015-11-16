import argparse
from word2vec_file import Word2VecFile
import sliding_window
import caffe

class Demo():
    """parses demo data, feeds to a trained model and returns predictions"""

    def __init__(self, vector_file, caffe_proto, caffe_model):
        self.word2vec = Word2VecFile(vector_file)
        self.nlp_pipeline = NlpPipeline()
        self.__caffe_proto = caffe_proto
        self.__caffe_model = caffe_model        
        net = caffe.Net(self.__caffe_proto, self.__caffe_model, caffe.TEST)
        caffe.set_mode_cpu()

    def get_not_covered_words(self):
        return self.word2vec.not_covered_words

    def predict_text(self, text):
        sentence = Sentence(1, text)
        # sentence.set_time_start(12.95)
        # sentence.set_time_end(29.50)
        # sentence.set_speech_text("You know one of the {$(<BREATH>)} intense pleasures of travel in one of the delights of ethnographic research {$(<BREATH>)} is the opportunity to live amongst those who have not forgotten the old ways {$(<BREATH>)} to {$(<BREATH>)} still feel their past and the wind {$(<SBREATH>)} touch and stones pause by rain {$(<SBREATH>)} I tasted in the bitter leaves of plants")
        # sentence.set_enriched_speech_text("You know one of the intense pleasures of travel in one of the delights of ethnographic research is the opportunity to live amongst those who have not forgotten the old ways to still feel their past and the wind touch and stones pause by rain I tasted in the bitter leaves of plants")
        sentence.set_gold_tokens(self.nlp_pipeline.parse_text(text))

        for token in sentence.gold_tokens:
            if not token.is_punctuation():
                token.word_vec = self.word2vec.get_vector(token.word.lower())

        slidingWindow = SlidingWindow()
        instances = slidingWindow.list_windows(sentence)

        for instance in instances:
            print(instance)

        for instance in instances:
            print(predict_caffe(instance))

    def predict_caffe(self, instance):
        transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

        batchsize = 1
        net.blobs['data'].reshape(batchsize,1,5,300)

        net.blobs['data'].data[...] = transformer.preprocess('data', instance.get_array())

        out = net.forward()
        return out['accuracy'], out['recall_per_class'], out['precision_per_class']

def main():
    demo = Demo()
    demo.predict_text("You know one of the intense pleasures of travel in one of the delights of ethnographic research is the opportunity to live amongst those who have not forgotten the old ways to still feel their past and the wind touch and stones pause by rain I tasted in the bitter leaves of plants")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get word vector from binary data.')
    parser.add_argument('--datafile', help='path to file with text, if not present text can be entered interactively')
    parser.add_argument('vectorfile', help='path to word vector binary')
    parser.add_argument('caffemodel', help='path to caffe model file')
    parser.add_argument('caffeproto', help='path to caffe proto file')
    args = parser.parse_args()
    main(args)
