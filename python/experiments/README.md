If you want to train multiple configurations on multiple databases you can use the convenience scripts in this folder.

First you will need to create a root folder, where all databases and experiment data is going to be saved, e.g. `/some/path`.
Then create a `1_open`, a `2_databased`, a `3_trained`, a `4_database_failed` and a `5_training_failed` folder inside that path (e.g. `/some/path/1_open`).
Insert all config files you want to test into the `1_open` folder.
Note that you should give these config files **meaningful filenames**, as their filenames are used for identification purposes later on.

# Creating Multiple Databases

For lexical data use `databases.sh` and for acoustic data use `audio_databases.sh`.

* Pass the original root folder (e.g. `/some/path`) to either of these scripts.
* All config files for which a database was created successfully, will be moved to the subfolder `2_databased`.
* If any fail, they will be moved to a subfolder `4_database_failed`.

# Training on Multiple Databases

For lexical data use `training.sh` and for acoustic data use `audio_training.sh`.

* Pass the original root folder (e.g. `/some/path`) to either of these scripts.
* This script will access all config files in the subfolder `2_databased`, and automatically move successful trained files to a subfolder `3_trained`
* If any fail, they will be moved to a subfolder `5_training_failed`.

The final experiment names will be taken from the basename of the config file.
