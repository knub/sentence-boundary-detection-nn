from flask import Flask
from classification import Classifier
import sys
sys.path.append("../python/")
from word2vec_file import Word2VecFile
import caffe
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/classify")
def classify():
    text = "The sun is shining Let's go outside"
    json_data = classifier.predict_text(text)
    return "punctuated text as json"

if __name__ == "__main__":

    vectorfile = ""
    caffeproto = ""
    caffemodel = ""

    vector = Word2VecFile(vectorfile)
    net = caffe.Net(caffeproto, caffemodel, caffe.TEST)
    classifier = Classifier(net, vector)

    app.run()
