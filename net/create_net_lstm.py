#!/usr/bin/env python
import sys
import lmdb
import random
import subprocess
import itertools
import argparse
import numpy as np
sys.path.append('python/caffe/proto'); import caffe_pb2

from caffe_pb2 import NetParameter, LayerParameter, DataParameter, SolverParameter, ParamSpec
from caffe_pb2 import Datum

def make_data(param):
    for phase in ['train', 'valid', 'test']:
        print 'Starting %s' % phase
        db_name = './examples/language_model/lm_%s_db' % phase
        subprocess.call(['rm', '-rf', db_name])
        env = lmdb.open(db_name, map_size=2147483648*8)

        def vocab_transform(target_input):
            def t_foo(x):
                return x if x < param['unknown_symbol'] else param['unknown_symbol']

            target_line = [t_foo(int(x)) for x in target_input.split(' ')[:param['maximum_length']]]

            target_line = target_line[:param['maximum_length']] + \
                          [param['zero_symbol']] * (param['maximum_length'] - len(target_line[:param['maximum_length']]))
            assert len(target_line) == param['maximum_length']
            return target_line

        allX = []
        with open('./data/language_model/%s_indices.txt' % phase, 'r') as f1:
            for en in f1.readlines():
                allX.append(vocab_transform(en))

        print 'Writing %s sentences' % len(allX)

        with env.begin(write=True) as txn:
            for i, target_line in enumerate(allX):
                datum = Datum()
                datum.channels = 2 * param['maximum_length']
                datum.width = 1
                datum.height = 1
                for j in range(param['maximum_length']):
                    if j == 0:
                        datum.float_data.append(param['start_symbol'])
                    else:
                        datum.float_data.append(target_line[j - 1])
                for j in range(param['maximum_length']):
                    datum.float_data.append(target_line[j])
                key = str(i)
                txn.put(key, datum.SerializeToString())

def get_solver(param):
    solver = SolverParameter()
    solver.net = param['file_train_val_net']
    solver.test_interval = param['solver_test_interval']
    solver.base_lr = param['solver_base_lr']
    solver.weight_decay = param['solver_weight_decay']
    solver.lr_policy = param['solver_lr_policy']
    solver.display = param['solver_display']
    solver.max_iter = param['solver_max_iter']
    solver.clip_gradients = param['solver_clip_gradients']
    solver.snapshot = param['solver_snapshot']
    solver.lr_policy = param['solver_lr_policy']
    solver.stepsize = param['solver_stepsize']
    solver.gamma = param['solver_gamma']
    solver.snapshot_prefix = param['solver_snapshot_prefix']
    solver.random_seed = param['solver_random_seed']
    solver.solver_mode = param['solver_solver_mode']
    solver.test_iter.append(param['solver_test_iter'])
    return solver


def get_net(param, deploy, batch_size):
    net = NetParameter()

    def add_weight_filler(param, max_value=param['init_range']):
        param.type = 'uniform'
        param.min = -max_value
        param.max = max_value

    if not deploy:
        train_data = net.layer.add()
        train_data.type = "Data"
        train_data.name = "data"
        train_data.top.append(train_data.name)
        train_data.data_param.source = 'examples/language_model/lm_train_db'
        train_data.data_param.backend = DataParameter.LMDB
        train_data.data_param.batch_size = batch_size

        test_data = net.layer.add()
        test_data.type = "Data"
        test_data.name = "data"
        test_data.top.append(test_data.name)
        test_data.data_param.source = 'examples/language_model/lm_valid_db'
        test_data.data_param.backend = DataParameter.LMDB
        test_data.data_param.batch_size = batch_size

        test_data_rule = test_data.include.add()
        test_data_rule.phase = caffe_pb2.TEST
        train_data_rule = train_data.include.add()
        train_data_rule.phase = caffe_pb2.TRAIN


    data_slice_layer = net.layer.add()
    data_slice_layer.name = "data_slice_layer"
    data_slice_layer.type = "Slice"
    data_slice_layer.slice_param.slice_dim = 1
    data_slice_layer.bottom.append('data')
    data_slice_layer.top.append('input_words')
    data_slice_layer.top.append('target_words')
    data_slice_layer.slice_param.slice_point.append(param['maximum_length'])

    label_slice_layer = net.layer.add()
    label_slice_layer.name = "label_slice_layer"
    label_slice_layer.type = "Slice"
    label_slice_layer.slice_param.slice_dim = 1
    label_slice_layer.bottom.append('target_words')
    for i in range(param['maximum_length']):
        label_slice_layer.top.append('label%d' % i)
        if i != 0:
            label_slice_layer.slice_param.slice_point.append(i)

    wordvec_layer = net.layer.add()
    wordvec_layer.name = "wordvec_layer"
    wordvec_layer.type = "Wordvec"
    wordvec_layer.bottom.append('input_words')
    wordvec_layer.top.append(wordvec_layer.name)
    wordvec_layer.wordvec_param.dimension = param['wordvec_length']
    wordvec_layer.wordvec_param.vocab_size = param['vocab_size']
    add_weight_filler(wordvec_layer.wordvec_param.weight_filler)

    wordvec_slice_layer = net.layer.add()
    wordvec_slice_layer.name = "wordvec_slice_layer"
    wordvec_slice_layer.type = "Slice"
    wordvec_slice_layer.slice_param.slice_dim = 2
    wordvec_slice_layer.slice_param.fast_wordvec_slice = True
    wordvec_slice_layer.bottom.append('wordvec_layer')
    for i in range(param['maximum_length']):
        wordvec_slice_layer.top.append('target_wordvec%d' % i)
        if i != 0:
            wordvec_slice_layer.slice_param.slice_point.append(i)


    for i in range(param['maximum_length']):
        if i == 0:
            dummy_layer = net.layer.add()
            dummy_layer.name = 'dummy_layer'
            dummy_layer.top.append(dummy_layer.name)
            dummy_layer.type = "DummyData"
            dummy_layer.dummy_data_param.num.append(batch_size)
            dummy_layer.dummy_data_param.channels.append(param['lstm_num_cells'])
            dummy_layer.dummy_data_param.height.append(1)
            dummy_layer.dummy_data_param.width.append(1)

            dummy_mem_cell = net.layer.add()
            dummy_mem_cell.name = 'dummy_mem_cell'
            dummy_mem_cell.top.append(dummy_mem_cell.name)
            dummy_mem_cell.type = "DummyData"
            dummy_mem_cell.dummy_data_param.num.append(batch_size)
            dummy_mem_cell.dummy_data_param.channels.append(param['lstm_num_cells'])
            dummy_mem_cell.dummy_data_param.height.append(1)
            dummy_mem_cell.dummy_data_param.width.append(1)


        for j in range(param['num_lstm_stacks']):
            concat_layer = net.layer.add()
            concat_layer.name = 'concat%d_layer%d' % (j, i)

            concat_layer.top.append(concat_layer.name)
            concat_layer.type = "Concat"
            concat_layer.concat_param.fast_lstm_concat = True
            if j == 0:
                concat_layer.bottom.append('target_wordvec%d' % i)
            if j >= 1:
                concat_layer.bottom.append('dropout%d_%d' % (j - 1, i))
            if i == 0:
                concat_layer.bottom.append(dummy_layer.name)
            else:
                concat_layer.bottom.append('lstm%d_hidden%d' % (j, i - 1))

            lstm_layer = net.layer.add()
            lstm_layer.name = 'lstm%d_layer%d' % (j, i)
            lstm_layer.type = "Lstm"
            lstm_layer.lstm_param.num_cells = param['lstm_num_cells']

            add_weight_filler(lstm_layer.lstm_param.input_weight_filler)
            add_weight_filler(lstm_layer.lstm_param.input_gate_weight_filler)
            add_weight_filler(lstm_layer.lstm_param.forget_gate_weight_filler)
            add_weight_filler(lstm_layer.lstm_param.output_gate_weight_filler)

            for k in range(4):
                param_spec = lstm_layer.param.add()
                param_spec.name = 'lstm%d_param_%d' % (j, k)
            lstm_layer.top.append('lstm%d_hidden%d' % (j, i))
            lstm_layer.top.append('lstm%d_mem_cell%d' % (j, i))
            lstm_layer.bottom.append('concat%d_layer%d' % (j, i))
            if i == 0:
                lstm_layer.bottom.append('dummy_mem_cell')
            else:
                lstm_layer.bottom.append('lstm%d_mem_cell%d' % (j, i - 1))

            dropout_layer = net.layer.add()
            dropout_layer.name = 'dropout%d_%d' % (j, i)
            dropout_layer.type = "Dropout"
            dropout_layer.top.append(dropout_layer.name)
            dropout_layer.bottom.append('lstm%d_hidden%d' % (j, i))
            dropout_layer.dropout_param.dropout_ratio = param['dropout_ratio']

    hidden_concat_layer = net.layer.add()
    hidden_concat_layer.type = "Concat"
    hidden_concat_layer.name = 'hidden_concat'
    hidden_concat_layer.top.append(hidden_concat_layer.name)
    hidden_concat_layer.concat_param.concat_dim = 0
    for i in range(param['maximum_length']):
        hidden_concat_layer.bottom.append('dropout%d_%d' % (param['num_lstm_stacks'] - 1, i))

    inner_product_layer = net.layer.add()
    inner_product_layer.name = "inner_product"
    inner_product_layer.top.append(inner_product_layer.name)
    inner_product_layer.bottom.append('hidden_concat')
    inner_product_layer.type = "InnerProduct"
    inner_product_layer.inner_product_param.bias_term = False
    inner_product_layer.inner_product_param.num_output = param['vocab_size']
    add_weight_filler(inner_product_layer.inner_product_param.weight_filler)

    label_concat_layer = net.layer.add()
    label_concat_layer.name = "label_concat"
    label_concat_layer.type = "Concat"
    label_concat_layer.concat_param.concat_dim = 0
    label_concat_layer.top.append(label_concat_layer.name)
    for i in range(param['maximum_length']):
        label_concat_layer.bottom.append('label%d' % i)

    if deploy:
        word_prob_layer = net.layer.add()
        word_prob_layer.name = "word_probs"
        word_prob_layer.top.append(word_prob_layer.name)
        word_prob_layer.type = "Softmax"
        word_prob_layer.bottom.append("inner_product")

    else:
        word_loss_layer = net.layer.add()
        word_loss_layer.name = "word_loss"
        word_loss_layer.type = "SoftmaxWithLoss"
        word_loss_layer.bottom.append("inner_product")
        word_loss_layer.bottom.append("label_concat")
        word_loss_layer.top.append(word_loss_layer.name)
        word_loss_layer.loss_param.ignore_label = param['zero_symbol']

    silence_layer = net.layer.add()
    silence_layer.name = "silence"
    silence_layer.type = "Silence"
    for j in range(param['num_lstm_stacks']):
        silence_layer.bottom.append("lstm%d_mem_cell%d" % (j, param['maximum_length'] - 1))
    for j in range(param['num_lstm_stacks'] - 1):
        silence_layer.bottom.append("dropout%d_%d" % (j, param['maximum_length'] - 1))

    return net

def write_solver(param):
    with open(param['file_solver'], 'w') as f:
        f.write(str(get_solver(param)))

def write_net(param):
    with open(param['file_train_val_net'], 'w') as f:
        f.write('name: "%s"\n' % param['net_name'])
        f.write(str(get_net(param, deploy=False, batch_size = param['train_batch_size'])))

    with open(param['file_deploy_net'], 'w') as f:
        f.write('name: "%s"\n' % param['net_name'])
        f.write('''
input: "data"
input_dim: %s
input_dim: %s
input_dim: 1
input_dim: 1
''' % (param['deploy_batch_size'], 2 * param['maximum_length']))
        f.write(str(get_net(param, deploy=True, batch_size = param['deploy_batch_size'])))


def get_base_param():
    param = {}
    param['net_name'] = "ManningNet"
    param['maximum_length'] = 30
    param['vocab_size'] = 10003
    param['num_lstm_stacks'] = 2

    param['unknown_symbol'] = param['vocab_size'] - 3
    param['start_symbol'] = param['vocab_size'] - 2
    param['zero_symbol'] = param['vocab_size'] - 1

    param['train_batch_size'] = 128
    param['deploy_batch_size'] = 128
    param['lstm_num_cells'] = 250
    param['wordvec_length'] = 250
    param['dropout_ratio'] = 0.16
    param['init_range'] = 0.14

    param['file_solver'] = "auto_solver.prototxt"
    param['file_train_val_net'] = "auto_net.prototxt"
    param['file_deploy_net'] = "auto_deploy.prototxt"
    param['solver_base_lr'] = 29.13
    param['solver_weight_decay'] = 1.6 * 10 ** (-6)
    param['solver_lr_policy'] = "fixed"
    param['solver_display'] = 100
    param['solver_max_iter'] = 20000
    param['solver_clip_gradients'] = 0.24
    param['solver_snapshot'] = 1000
    param['solver_lr_policy'] = 'step'
    param['solver_stepsize'] = 2500
    param['solver_gamma'] = 0.792
    param['solver_snapshot_prefix'] = "examples/language_model/lm"
    param['solver_random_seed'] = 22
    param['solver_solver_mode'] = SolverParameter.GPU
    param['solver_test_interval'] = 1000
    param['solver_test_iter'] = 200
    return param

def prepare(param):
    write_solver(param)
    write_net(param)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--make_data', action='store_true')
    args = parser.parse_args()
    if args.make_data:
        make_data(get_base_param())
    prepare(get_base_param())

if __name__ == '__main__':
    main()
