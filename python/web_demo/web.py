from flask import Flask, render_template, request
import json, caffe, argparse
from preprocessing.word2vec_file import Word2VecFile
from classification import Classifier
import common.sbd_config as sbd
from os import walk

app = Flask(__name__)

route_folder = ''
config_file_name = ''
caffeeproto_name = ''
caffemodel_name = ''
folder = ''

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

@app.route("/settings", methods = ['GET'])
def getSettinOptions():
    assert request.method == 'GET'
    f = []
    for (dirpath, dirnames, filenames) in walk(route_folder):
        f.extend(dirnames)
        break
    response = {"selected": folder, "options":f}
    return json.dumps(response)

@app.route("/settings", methods = ['POST'])
def changeSettings():
    global classifier
    assert request.method == 'POST'
    classifier = settings(str(request.form['folder']), vector)
    return ('', 200)


def settings(folder, vector):
    print 'loading config folder: ' + folder

    config_folder = route_folder + folder + "/"

    config_file = sbd.SbdConfig(config_folder + config_file_name)
    net = caffe.Net(config_folder + caffeeproto_name, config_folder + caffemodel_name, caffe.TEST)

    if vector:
        classifier = Classifier(net, vector, False)
    else:
        classifier = Classifier(net, vector, True)

    return classifier


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run the web demo')
    parser.add_argument('routefolder', help='the main directory containing all possible configurations', default='models/', nargs='?')
    parser.add_argument('standardConfig', help='the subdirectory of routes folder containing the standart model', default='testsettings', nargs='?') 
    parser.add_argument('caffeproto', help='the deploy prototxt template name of your trained model', default='deploy.prototxt', nargs='?')
    parser.add_argument('caffemodel', help='the trained caffemodel template name', default='model.caffemodel', nargs='?')
    parser.add_argument('vectorfile', help='the google news word vector', default='models/GoogleNews-vectors-negative300.bin', nargs='?')
    parser.add_argument('configfile', help='the config file template name', default='config.ini', nargs='?')
    parser.add_argument('-nd','--no-debug', help='do not use debug mode, google vector is read', action='store_false', dest='debug', default=DEBUG)
    args = parser.parse_args()

    route_folder = args.routefolder
    config_file_name = args.configfile
    caffeeproto_name = args.caffeproto
    caffemodel_name = args.caffemodel

    folder = args.standardConfig

    config_file = sbd.SbdConfig(route_folder + folder + "/" + config_file_name)

   # net = caffe.Net(args.caffeproto, args.caffemodel, caffe.TEST)
    if not args.debug:
        vector = Word2VecFile(args.vectorfile)
       # classifier = Classifier(net, vector, False)
        classifier = settings(folder, vector)
        app.run(debug = True, use_reloader = False)
    else:
        vector = None
        classifier = settings(folder, vector)
        app.run(debug = True)
