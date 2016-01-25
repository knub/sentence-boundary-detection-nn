import common.sbd_config as sbd
import json, caffe, argparse, os
from sbd_classification.util import *
from sbd_classification.audio_parser import AudioParser
from json_converter import JsonConverter
from file_io import ResultWriter, InputTextReader
from flask import Flask, render_template, request
from os import walk
from preprocessing.word2vec_file import Word2VecFile

app = Flask(__name__)

route_folder = ''

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

def load_config(model_folder, model):
    default_model = os.path.join(route_folder, model_folder, model)
    config_file, caffemodel_file, net_proto = get_filenames(default_model)
    sbd.SbdConfig(config_file)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/audio_lexical")
def audio_lexical():
    return render_template('audio_lexical.html')

@app.route("/classify_lexical", methods = ['POST'])
def classifyLexical():
    assert request.method == 'POST'
    text_file = request.form['textfile']
    text = ""
    if text_file == 'None':
        text = request.form['text']
    else:
        file_name = os.path.join(route_folder, TEXT_DATA, text_file)
        inputTextReader = InputTextReader()
        text = inputTextReader.readFile(file_name)

    load_config(LEXICAL_MODEL_FOLDER, request.form['lexical_folder'])
    (tokens, punctuations_probs) = lexical_classifier.predict_text(text)
    jsonConverter = JsonConverter()
    data = jsonConverter.convert_lexical(tokens, punctuations_probs)

    resultWriter = ResultWriter()
    resultWriter.writeToFile(route_folder + "result.txt", tokens, punctuations_probs)

    return json.dumps(data)

@app.route("/classify_audio_lexical", methods = ['POST'])
def classifyAudioLexical():
    assert request.method == 'POST'
    # get example folder
    example_folder = os.path.join(route_folder, AUDIO_EXAMPLE_FOLDER, request.form['example'])
    ctm_file, pitch_file, energy_file = get_audio_files(example_folder)

    # parse ctm_file, pitch_file and energy_file
    parser = AudioParser(ctm_file, pitch_file, energy_file)
    parser.parse()

    load_config(LEXICAL_MODEL_FOLDER, request.form['lexical_folder'])
    (lex_tokens, lex_punctuations_probs) = lexical_classifier.predict_text_with_audio(parser)
    load_config(AUDIO_EXAMPLE_FOLDER, request.form['audio_folder'])
    (au_tokens, au_punctuations_probs) = audio_classifier.predict_text(parser)

    jsonConverter = JsonConverter()
    data = jsonConverter.convert_lexical(lex_tokens, lex_punctuations_probs)

    return json.dumps(data)

@app.route("/files", methods = ['GET'])
def getTextFiles():
    assert request.method == 'GET'
    f = []
    text_folder = os.path.join(route_folder, TEXT_DATA)
    for (dirpath, dirnames, filenames) in walk(text_folder):
        for filename in filenames:
            if not (filename.endswith(".result") or filename.startswith(".")):
                f.append(filename)
    return json.dumps(f)

@app.route("/examples", methods = ['GET'])
def getAudioExamples():
    assert request.method == 'GET'
    f = []
    example_root_folder = os.path.join(route_folder, AUDIO_EXAMPLE_FOLDER)
    for (dirpath, dirnames, filenames) in walk(example_root_folder):
        for dir in dirnames:
            f.append(dir)
    return json.dumps(f)

@app.route("/audio_models", methods = ['GET'])
def getAudioModels():
    assert request.method == 'GET'
    f = get_options(route_folder, AUDIO_MODEL_FOLDER)
    response = {"selected": f[0], "options":f}
    return json.dumps(response)

@app.route("/audio_models", methods = ['POST'])
def changeAudioModel():
    global audio_classifier
    assert request.method == 'POST'
    model_file = os.path.join(route_folder, AUDIO_MODEL_FOLDER, str(request.form['folder']))
    audio_classifier = load_audio_classifier(model_file , vector)
    return ('', 200)

@app.route("/lexical_models", methods = ['GET'])
def getLexicalModels():
    assert request.method == 'GET'
    f = get_options(route_folder, LEXICAL_MODEL_FOLDER)
    response = {"selected": f[0], "options":f}
    return json.dumps(response)

@app.route("/lexical_models", methods = ['POST'])
def changeLexicalModel():
    global lexical_classifier
    assert request.method == 'POST'
    model_file = os.path.join(route_folder, LEXICAL_MODEL_FOLDER, str(request.form['folder']))
    lexical_classifier = load_lexical_classifier(model_file, vector)
    return ('', 200)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run the web demo', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('routefolder', help='the main directory containing all possible configurations', default='demo_data/', nargs='?')
    parser.add_argument('vectorfile', help='the google news word vector', default='models/GoogleNews-vectors-negative300.bin', nargs='?')
    parser.add_argument('-nd','--no-debug', help='do not use debug mode, google vector is read', action='store_false', dest='debug', default=DEBUG)
    args = parser.parse_args()

    route_folder = args.routefolder

    #### load lexical model ####

    lexical_models = get_options(route_folder, LEXICAL_MODEL_FOLDER)
    default_lexical_model = os.path.join(route_folder, LEXICAL_MODEL_FOLDER, lexical_models[0])

    # get the caffe files
    config_file, caffemodel_file, net_proto = get_filenames(default_lexical_model)

    # read the config file
    config_file = sbd.SbdConfig(config_file)

    if not args.debug:
        vector = Word2VecFile(args.vectorfile)
        lexical_classifier = load_lexical_classifier(default_lexical_model, vector)
    else:
        vector = None
        lexical_classifier = load_lexical_classifier(default_lexical_model, vector)

    #### load lexical model ####

    audio_models = get_options(route_folder, AUDIO_MODEL_FOLDER)
    default_audio_model = os.path.join(route_folder, AUDIO_MODEL_FOLDER, audio_models[0])

    # get the caffe files
    config_file, caffemodel_file, net_proto = get_filenames(default_audio_model)

    # read the config file
    config_file = sbd.SbdConfig(config_file)

    audio_classifier = load_audio_classifier(default_audio_model)

    #### start app ####

    if not args.debug:
        app.run(debug = True, use_reloader = False)
    else:
        app.run(debug = True)
