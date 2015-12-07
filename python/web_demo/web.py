from flask import Flask, render_template, request
import json, caffe, argparse
from preprocessing.word2vec_file import Word2VecFile
from classification import Classifier

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
    parser = argparse.ArgumentParser(description='run the web demo')
    parser.add_argument('caffeproto', help='the deploy prototxt of your trained model', default='web_demo/models/deploy.prototxt', nargs='?')
    parser.add_argument('caffemodel', help='the trained caffemodel', default='web_demo/models/model.caffemodel', nargs='?')
    parser.add_argument('vectorfile', help='the google news word vector', default='web_demo/models/GoogleNews-vectors-negative300.bin', nargs='?')
    args = parser.parse_args()

    net = caffe.Net(args.caffeproto, args.caffemodel, caffe.TEST)
    if not DEBUG:
        vector = Word2VecFile(args.vectorfile)
        classifier = Classifier(net, vector)
        app.run(debug = True, use_reloader = False)
    else:
        classifier = Classifier(net, None, True)
        app.run(debug = True)
