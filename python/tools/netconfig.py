import argparse, sys
from google.protobuf import text_format

import caffe
from caffe.proto import caffe_pb2

def get_layer_by_name(net, name):
    for layer in net.layer:
        if layer.name == name:
            return layer

def get_data_layer(net, phase):
    for layer in net.layer:
        if layer.name == "data":
            for value in layer.include:
                if value.phase == phase:
                    return layer

def get_test_data_layer(net):
    return get_data_layer(net, caffe_pb2.TEST)

def get_train_data_layer(net):
    return get_data_layer(net, caffe_pb2.TRAIN)

def replace_loss_with_softmax(net):
    losslayer = get_layer_by_name(net, "loss")
    losslayer.name = "softmax"
    losslayer.type = "Softmax"
    losslayer.bottom.remove("label")
    losslayer.top.remove("loss")
    losslayer.top.append("softmax")
    return losslayer

def main(args):
    # read template net
    net = caffe_pb2.NetParameter()
    text_format.Merge(args.prototxt.read(), net)

    # make deploy version of net
    if args.deploy:
        # remove data layers
        net.layer.remove(get_train_data_layer(net))
        net.layer.remove(get_test_data_layer(net))

        # remove accuracy layer
        net.layer.remove(get_layer_by_name(net, "accuracy"))

        # add input
        net.input.append("data")
        net.input_dim.append(1)
        net.input_dim.append(1)
        net.input_dim.append(5)
        net.input_dim.append(300)

        # use softmax instead of loss layer
        replace_loss_with_softmax(net)

    if args.train:
        db_pair_dir = args.train

        # modify path to leveldb for test and train data layer
        test_data_layer = get_test_data_layer(net)
        test_data_layer.data_param.source = db_pair_dir + "/test"

        train_data_layer = get_train_data_layer(net)
        train_data_layer.data_param.source = db_pair_dir + "/train"

    if args.print_database:
        test_data_layer = get_test_data_layer(net)
        print test_data_layer.data_param.source.replace("/test", "")
        return

    # write changed net to output
    args.output.write(str(net))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Configure your net')
    parser.add_argument('prototxt', help='the original net prototxt', type=argparse.FileType('r'))
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d','--deploy', help='preset: deploy; remove data layers, add softmax', action='store_true')
    group.add_argument('-p','--print_database', help='Whether to print the database folder or not', action='store_true')
    group.add_argument('-t','--train', help='preset: make training net on test/train leveldb in directory', metavar='directory')
    parser.add_argument('-o','--output', help='output of the modified net', type=argparse.FileType('w'), default=sys.stdout, metavar='output')
    # parser.add_argument('-v','--verbose', help='be verbose', action='store_true')
    args = parser.parse_args()

    main(args)
