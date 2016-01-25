## Sentence Boundary Detecting using Deep Neural Networks

We try to detect sentence boundaries using deep learning.
Created as part of the "Practical Applications of Multimedia Retrieval" seminar at the Hasso-Plattner-Institute, Potsdam, Germany.

### Setup Demo
We build a python-based demo.

####Prerequirements:
1. Install python 2.7 including the following packages:
  * Flask==0.10.1
  * Jinja2==2.8
  * MarkupSafe==0.23
  * Pillow==3.0.0
  * Werkzeug==0.11.3
  * argparse==1.2.1
  * cycler==0.9.0
  * decorator==4.0.4
  * enum==0.4.6
  * enum34==1.0.4
  * intervaltree==2.1.0
  * itsdangerous==0.24
  * leveldb==0.193
  * lmdb==0.87
  * matplotlib==1.5.0
  * networkx==1.10
  * nltk==3.1
  * numpy==1.10.1
  * protobuf==2.6.1
  * pyparsing==2.0.5
  * python-dateutil==2.4.2
  * pytz==2015.7
  * regex==2015.11.22
  * scikit-image==0.11.3
  * scipy==0.16.1
  * six==1.10.0
  * sortedcontainers==1.4.4
  * wsgiref==0.1.2
2. Setup caffe, like described [here](http://caffe.berkeleyvision.org/installation.html)
3. Clone this repository
4. Add path to the repository to your python path: 
  ```
  export PYTHONPATH=/path/to/sentence-boundary-detection-nn:$PYTHONPATH
  ```
5. Download Google Word Vector (GoogleNews-vectors-negative300.bin.gz) from [here](https://code.google.com/p/word2vec/)  or use directly this [url](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing)
6. Create a folder with your demo data including the following directories:
  * lexical_models : containing all pretrained models you want to use in a seperate directory. Each models needs a 
    * .ini
    * .caffemodel
    * net.prototxt file.
  * text_data: containing all possible text files, which should be used as prediction input
  * audio_models: containing all pretrainied audio models, each in a seperate directory. Each needs the same files as described for lexical models
  * audio_examples: containing all audio files, which should be available during the demo. Each one in a seperate directory containing the ctm, energy and pitch files.

####Start up

Change into the repository directory and then execute
```
python python/web_demo
```
Optionally you can specify the location of the word vector, the demo data.
For further information execute:
```
python python/web_demo -h
```
