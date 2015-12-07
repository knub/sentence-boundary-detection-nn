import caffe

import demo.demo as d
from preprocessing.word2vec_file import Word2VecFile

vector = Word2VecFile('models/GoogleNews-vectors-negative300.bin')
net = caffe.Net('models/deploy.prototxt', 'models/model.caffemodel', caffe.TEST)

