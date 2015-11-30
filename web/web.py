from flask import Flask
from flask import render_template
from flask import request
import json

import sys
sys.path.append("../python/")
from classification import Classifier
from word2vec_file import Word2VecFile
import caffe

app = Flask(__name__)

DEBUG = True

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/classify", methods = ['POST'])
def classify():
    assert request.method == 'POST'
    text = request.form['text']
    data = classifier.predict_text(text)
    return json.dumps(data)

if __name__ == "__main__":
    caffeproto = "models/deploy.prototxt"
    caffemodel = "models/model.caffemodel"
    net = caffe.Net(caffeproto, caffemodel, caffe.TEST)

    if not DEBUG:
        vectorfile = "models/GoogleNews-vectors-negative300.bin" # vectors.bin
        vector = Word2VecFile(vectorfile)
        classifier = Classifier(net, vector)
        app.run(debug = True, use_reloader = False)
    else:
        classifier = Classifier(net, None, True)
        app.run(debug = True)
