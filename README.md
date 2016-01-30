## Sentence Boundary Detecting using Deep Neural Networks

We try to detect sentence boundaries using deep learning.
Created as part of the "Practical Applications of Multimedia Retrieval" seminar at the Hasso-Plattner-Institute, Potsdam, Germany.

### Setup Demo
We build a python-based demo using caffe.

#####Prerequirements:
1. Clone this repository
2. Install python 2.7 including the following packages from requirements.txt

  `pip install requirements.txt`

3. Use the nltk downloader to download `averaged_perceptron_tagger` and `punkt` models:

  `python -m nltk.downloader`

4. Setup caffe, like described [here](http://caffe.berkeleyvision.org/installation.html)
5. Add path to the repository to your python path: 

  `export PYTHONPATH=/path/to/sentence-boundary-detection-nn/python:$PYTHONPATH`

6. Download Google Word Vector (GoogleNews-vectors-negative300.bin.gz) from [here](https://code.google.com/p/word2vec/)  or use directly this [url](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing) and extract the result into the `sentence-boundary-detection-nn/python/demo_data` directory
7. Paste your trained models into a demo data folder, for example `sentence-boundary-detection-nn/python/demo_data` with the following structure:
  * lexical_models : containing all pretrained models you want to use in a seperate directory. Each models needs a 
    * .ini
    * .caffemodel
    * net.prototxt file.
  * text_data: containing all possible text files, which should be used as prediction input
  * audio_models: containing all pretrainied audio models, each in a seperate directory. Each needs the same files as described for lexical models
  * audio_examples: containing all audio files, which should be available during the demo. Each one in a seperate directory containing the ctm, energy and pitch files.

#####Start up

Change into the repository directory and execute, this should work right out of the box, unless you are using a custom `demo_data` folder:
```
python python/web_demo
```
Optionally you can specify the location of the word vector and the demo data. Otherwise default values are used.
For further information execute:
```
python python/web_demo -h
```
