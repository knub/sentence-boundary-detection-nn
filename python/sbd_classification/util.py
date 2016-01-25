import common.sbd_config as sbd
import caffe
from tools.netconfig import NetConfig
from os import listdir
from sbd_classification.lexical_classification import LexicalClassifier
from preprocessing.nlp_pipeline import PosTag

def settings(route_folder, folder, vector):
    print 'Loading config folder: ' + folder

    config_file, caffemodel_file, net_proto = get_filenames(route_folder + folder)

    config_file = sbd.SbdConfig(config_file)
    WINDOW_SIZE = sbd.config.getint('windowing', 'window_size')
    POS_TAGGING = sbd.config.getboolean('features', 'pos_tagging')
    FEATURE_LENGTH = 300 if not POS_TAGGING else 300 + len(PosTag)

    with file(net_proto, "r") as input_:
        nc = NetConfig(input_)
    nc.transform_deploy([1, 1, WINDOW_SIZE, FEATURE_LENGTH])
    temp_proto = "%s/%s/temp_deploy.prototxt" % (route_folder, folder)
    with file(temp_proto, "w") as output:
        nc.write_to(output)

    net = caffe.Net(temp_proto, caffemodel_file, caffe.TEST)

    if vector:
        classifier = LexicalClassifier(net, vector, False)
    else:
        classifier = LexicalClassifier(net, vector, True)

    return classifier

def get_filenames(folder):
    for file_ in listdir(folder):
        if file_.endswith(".ini"):
            config_file = folder + "/" + file_
        elif file_.endswith(".caffemodel"):
            caffemodel_file = folder + "/" + file_
        elif file_ == "net.prototxt":
            net_proto = folder + "/" + file_
    return config_file, caffemodel_file, net_proto
