import caffe
import demo.demo as d
from word2vec_file import Word2VecFile

vector = Word2VecFile('../../ms-2015-t3/GoogleNews-vectors-negative300.bin')
net = caffe.Net('/home/ms2015t3/sentence-boundary-detection-nn-joseph/net/net.prototxt', '/home/ms2015t3/sentence-boundary-detection-nn/net/experiments/20151115-171451_basic_features/_iter_100000.caffemodel', caffe.TEST)

