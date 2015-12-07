## Working Directory

To execute all python scripts in this folder, please use this folder as the working directory. For example:
```
python leveldb/level_db_creator.py -h
python preprocessing/word2vec_file.py -h
python parsing/plaintext_parser.py -h
python console_demo/demo.py -h
python web_demo/web.py -h
```

## Demo

For a one-time live interactive command line demo please run `python console_demo/demo.py` and use the correct parameters (use `python console_demo/demo.py -h` for help).

To avoid long loading times, you can preload the word vector and the model. Open a python shell with `python` and import the word vector and model manually with the following code (adapt your paths to GoogleNewsVector.bin, net.prototxt and model.caffemodel):

```
>>> import caffe
>>> import demo.demo as d
>>> from preprocessing.word2vec_file import Word2VecFile
>>> vector = Word2VecFile('GoogleNewsVector.bin')
>>> net = caffe.Net('net.prototxt', 'model.caffemodel', caffe.TEST)
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
