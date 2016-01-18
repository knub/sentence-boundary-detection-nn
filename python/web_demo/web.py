from flask import Flask, render_template, request
import json, caffe, argparse
from preprocessing.word2vec_file import Word2VecFile
from classification import Classifier
import common.sbd_config as sbd
from os import walk, listdir

app = Flask(__name__)

route_folder = ''
config_file = None
caffeeproto_name = ''
caffemodel_file = None
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
def getSettingOptions():
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
    print 'Loading config folder: ' + folder

    config_folder = route_folder + folder + "/"
    config_file, caffemodel_file = getFilenames(folder)

    config_file = sbd.SbdConfig(config_folder + config_file)
    net = caffe.Net(config_folder + caffeeproto_name, config_folder + caffemodel_file, caffe.TEST)

    if vector:
        classifier = Classifier(net, vector, False)
    else:
        classifier = Classifier(net, vector, True)

    return classifier

def getFilenames(folder):

    for file_ in listdir(route_folder + folder):
        if file_.endswith(".ini"):
            config_file = file_
        elif file_.endswith(".caffemodel"):
            caffemodel_file = file_
    return config_file, caffemodel_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run the web demo')
    parser.add_argument('routefolder', help='the main directory containing all possible configurations', default='models/', nargs='?')
    parser.add_argument('standardConfig', help='the subdirectory of routes folder containing the standart model', default='testsettings', nargs='?') 
    parser.add_argument('caffeproto', help='the deploy prototxt template name of your trained model', default='deploy.prototxt', nargs='?')
    parser.add_argument('vectorfile', help='the google news word vector', default='models/GoogleNews-vectors-negative300.bin', nargs='?')
    parser.add_argument('-nd','--no-debug', help='do not use debug mode, google vector is read', action='store_false', dest='debug', default=DEBUG)
    args = parser.parse_args()

    route_folder = args.routefolder
    folder = args.standardConfig
    caffeeproto_name = args.caffeproto

    config_file, caffemodel_file = getFilenames(folder)

    config_file = sbd.SbdConfig(route_folder + folder + '/' + config_file)

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
