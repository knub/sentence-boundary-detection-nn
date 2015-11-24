## Working Directory

To execute all python scripts in this folder, please use this folder as the working directory. For example:
```
python word2vec_file.py -h
python parser/plaintext_parser.py -h
python demo/demo.py -h
```

## Demo

For a one-time live interactive command line demo please run `python demo/demo.py` and use the correct parameters (use `python demo/demo.py -h` for help).

To avoid long loading times, you can preload the word vector and the model. Open a python shell with `python` and import the word vector and model manually with the following code (adapt your local paths if neccesary): 

```
>>> import caffe
>>> import demo.demo as d
>>> from word2vec_file import Word2VecFile
>>> vector = Word2VecFile('../../ms-2015-t3/GoogleNews-vectors-negative300.bin')
>>> net = caffe.Net('/home/ms2015t3/sentence-boundary-detection-nn-joseph/net/net.prototxt', '/home/ms2015t3/sentence-boundary-detection-nn/net/experiments/20151115-171451_basic_features/_iter_100000.caffemodel', caffe.TEST)
```
If you get an error on importing caffe, try using your virtual environment, or add the neccesary paths to your `PYTHONPATH`.

This code is also bundled in the `demo_preparation.py` file, so on the server you can alternative simply call:
```
>>> from demo.demo_preparation import *
```

Now you can classify multiple files or run the interactive demo:
```
>>> d.main_no_loading(net, vector, "file1.txt")
>>> d.main_no_loading(net, vector, "file2.txt")
>>> d.main_no_loading(net, vector)
```
