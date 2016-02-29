Before executing any scripts on the server, please execute `. ./use_python p2` in `/home/ms2015t3/sentence-boundary-detection-nn`.

Also, make sure that the directory `/home/ms2015t3/sentence-boundary-detection-nn/python` is added to the python path environment variable:

```
export PYTHONPATH="${PYTHONPATH}:/home/ms2015t3/sentence-boundary-detection-nn/python"
```

Also, you have to set the environment variable `SENTENCE_HOME`, because many scripts rely on it:

```
export SENTENCE_HOME="/home/ms2015t3/sentence-boundary-detection-nn"
```

To execute all python scripts in this folder, please use **this folder as the working directory**.

## Creating LevelDB for lexical model

To build a level db for the lexical model, please execute:
```
python sbd_leveldb/training_instance_generator.py config.ini
```
The `config.ini` file contains all parameters, which are needed during the creation of the training instances. 
It also contains the training files and test files, which should be used. 
The data root directory is set to `/mnt/naruto/sentence/data`. 
All training and test files should be located in this folder.
The `config.ini.default` file contains an example of a valid `config.ini` file.

The created level db can be found under `/mnt/naruto/sentence/leveldbs`.

## Creating LevelDB for acoustic model

To build a level db for the acoustic model, please execute:
```
python sbd_leveldb/audio_training_instance_generator.py config.ini
```
The `config.ini` file contains all parameters, which are needed during the creation of the training instances. 
The parameter `lexical` needs to be set to `false`.

It also contains the training files and test files, which should be used. 
The data root directory is set to `/mnt/naruto/sentence/data`
All training and test files should be located in this folder.
The corresponding `.pitch` and `.energy` files should be in the same folder as the `.ctm` files.
Also, the `.pitch` and `.energy` files should have the following name: `<data-set>_talkid<id>.[pitch|energy]`.
The `<data-set>` parameter is extracted from the `.ctm` files.
To create the `.pitch` and `.energy` files, you can use the `pitch_and_energy.sh` script under `/mnt/naruto/sentence/data/audio`.

The created level db can be found under `/mnt/naruto/sentence/leveldbs`.
