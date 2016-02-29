# Training

For training the acoustic neural network, you have to execute the following steps:

1. Adapt the `net.prototxt`: Change the network layout and make sure, you enter the correct path to the level db.
2. Adapt the `solver.prototxt`.
3. Make sure there exists an `experiments` and `snapshots` folder in this folder.
4. Execute `training.sh <experiment_name>`.

The `training.sh` script does several things:
* Creates a folder in the `experiment` folder with the name you gave your experiment
* The following files are copied to that folder:
 * `config.ini`, which is located in your database folder
 * `net.prototxt`
 * `solver.prototxt`
 * log files from the training
* Starts the training of the nerual network
* The latest `.solverstate` and `.caffemodel` are copied to the `experiment` folder after the training is finished
* After training, different graphs are created and put into the `experiment` folder.
