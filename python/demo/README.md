## Demo

For a one-time live interactive command line demo please run `python demo.py` and use the correct parameters (use `python demo.py -h` for help).

To avoid long loading times, you can preload the word vector and the model:
Open a python shell with `python` and import the word vector and model manually with the following code: 

```
>>> import caffe, demo
>>> vector = Word2VecFile('../../ms-2015-t3/GoogleNews-vectors-negative300.bin')
>>> net = caffe.Net('/home/ms2015t3/sentence-boundary-detection-nn-joseph/net/net.prototxt', '/home/ms2015t3/sentence-boundary-detection-nn/net/experiments/20151115-171451_basic_features/_iter_100000.caffemodel', caffe.TEST)
```

This code is also bundled in the `demo_preparation.py` file, so on the server you can alternative simply call:
```
>>> import demo_preparation
```

Now you can classify multiple files or run the interactive demo:
```
>>> demo.main_no_loading(net, vector, "file1.txt")
>>> demo.main_no_loading(net, vector, "file2.txt")
>>> demo.main_no_loading(net, vector)
```
