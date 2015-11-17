## Demo

For a one-time live interactive command line demo please run `python demo.py` and use the correct parameters (use `python demo.py -h` for help).

To avoid long loading times, you can preload the word vector and the model. Open a python shell with `python` and import the word vector and model manually with the following code (adapt your local paths if neccesary): 

```
>>> import caffe, demo
>>> vector = Word2VecFile('path/to/GoogleNews-vectors-negative300.bin')
>>> net = caffe.Net('../net/deploy.prototxt', 'path/to/trained_model.caffemodel', caffe.TEST)
```
If you get an error on importing caffe, try using your virtual environment, or add the neccesary paths to your `PYTHONPATH`.

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
