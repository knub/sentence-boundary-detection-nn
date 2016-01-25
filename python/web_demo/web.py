import common.sbd_config as sbd
import json, caffe, argparse, os
from sbd_classification.util import *
from sbd_classification.lexical_classification import LexicalClassifier
from json_converter import JsonConverter
from file_io import ResultWriter
from flask import Flask, render_template, request
from os import walk, listdir
from preprocessing.word2vec_file import Word2VecFile
from preprocessing.nlp_pipeline import PosTag

app = Flask(__name__)

route_folder = ''
config_file = None
text_folder = ''

LEXICAL_MODEL_FOLDER = "lexical_models"
AUDIO_MODEL_FOLDER = "audio_models"
AUDIO_EXAMPLE_FOLDER = "audio_examples"
TEXT_DATA = "text_data"

DEBUG = True

def get_options(route_folder, sub_folder):
    dir = os.path.join(route_folder, sub_folder)
    f = []
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend(dirnames)
        break
    return f

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/audio_lexical")
def audio_lexical():
    return render_template('audio_lexical.html')

@app.route("/classify", methods = ['POST'])
def classify():
    assert request.method == 'POST'
    text_file = request.form['textfile']
    text = ""
    if text_file == 'None':
        text = request.form['text']
    else:
        file_name = "%s/%s" % (text_folder, text_file)
        with open(file_name) as f:
            text = f.read()

    (tokens, punctuations_probs) = classifier.predict_text(text)
    jsonConverter = JsonConverter()
    data = jsonConverter.convert_lexical(tokens, punctuations_probs)

    resultWriter = ResultWriter()
    resultWriter.writeToFile(route_folder + "result.txt", tokens, punctuations_probs)

    return json.dumps(data)

@app.route("/files", methods = ['GET'])
def getTextFiles():
    assert request.method == 'GET'
    f = []
    for (dirpath, dirnames, filenames) in walk(text_folder):
        for filename in filenames:
            if not (filename.endswith(".result") or filename.startswith(".")):
                f.append(filename)
    return json.dumps(f)

@app.route("/audio_models", methods = ['GET'])
def getAudioModels():
    assert request.method == 'GET'
    f = get_options(route_folder, AUDIO_MODEL_FOLDER)
    response = {"selected": f[0], "options":f}
    return json.dumps(response)

@app.route("/audio_models", methods = ['POST'])
def changeAudioModel():
    global classifier
    assert request.method == 'POST'
    pass

@app.route("/lexical_models", methods = ['GET'])
def getLexicalModels():
    assert request.method == 'GET'
    f = get_options(route_folder, LEXICAL_MODEL_FOLDER)
    response = {"selected": f[0], "options":f}
    return json.dumps(response)

@app.route("/lexical_models", methods = ['POST'])
def changeLexicalModel():
    global classifier
    assert request.method == 'POST'
    model_file = os.path.join(route_folder, LEXICAL_MODEL_FOLDER, str(request.form['folder']))
    classifier = load_lexical_classifier(model_file , vector)
    return ('', 200)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run the web demo', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('routefolder', help='the main directory containing all possible configurations', default='demo_data/', nargs='?')
    parser.add_argument('vectorfile', help='the google news word vector', default='models/GoogleNews-vectors-negative300.bin', nargs='?')
    parser.add_argument('-nd','--no-debug', help='do not use debug mode, google vector is read', action='store_false', dest='debug', default=DEBUG)
    args = parser.parse_args()

    route_folder = args.routefolder

    # get text folder
    text_folder = os.path.join(route_folder, TEXT_DATA)

    # load lexial models
    lexical_models = get_options(route_folder, LEXICAL_MODEL_FOLDER)
    default_model = os.path.join(route_folder, LEXICAL_MODEL_FOLDER, lexical_models[0])

    # get the caffe files
    config_file, caffemodel_file, net_proto = get_filenames(default_model)

    # read the config file
    config_file = sbd.SbdConfig(config_file)

    # net = caffe.Net(args.caffeproto, args.caffemodel, caffe.TEST)
    if not args.debug:
        vector = Word2VecFile(args.vectorfile)
       # classifier = Classifier(net, vector, False)
        classifier = load_lexical_classifier(default_model, vector)
        app.run(debug = True, use_reloader = False)
    else:
        vector = None
        classifier = load_lexical_classifier(default_model, vector)
        app.run(debug = True)
