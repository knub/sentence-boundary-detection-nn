import sys
sys.path.append("..")

import caffe, demo
from word2vec_file import Word2VecFile

vector = Word2VecFile('../../ms-2015-t3/GoogleNews-vectors-negative300.bin')
net = caffe.Net('/home/ms2015t3/sentence-boundary-detection-nn-joseph/net/net.prototxt', '/home/ms2015t3/sentence-boundary-detection-nn/net/experiments/20151115-171451_basic_features/_iter_100000.caffemodel', caffe.TEST)

print ("use 'demo.main_no_loading(net, vector)' to interactively explore the demo")
print ("use 'demo.main_no_loading(net, vector, \"path/to/file\")' to analyze the contents of 'path/to/file'")
print ("to reload changes to the demo code, use 'reload(demo)'")
