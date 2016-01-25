#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters!"
    echo "./experiments.sh <CONFIG_FOLDER>"
    exit
fi

CONFIG_FOLDER=$1

if ! [[ -d $CONFIG_FOLDER ]]; then
    echo "$CONFIG_FOLDER is not a directory!"
    exit
fi

# Abort on first error
set -e

source $SENTENCE_HOME/use_python p2

for CONFIG_FILE in "$CONFIG_FOLDER"/1_open/*
do
    cd $SENTENCE_HOME/python/
    CONFIG=$(basename ${CONFIG_FILE})
    CONFIG="${CONFIG%.*}"
    echo "#################### Creating database with $CONFIG ####################"
    python sbd_leveldb/audio_training_instance_generator.py $CONFIG_FILE

    if [ $? -eq 0 ]; then
        echo "#################### Moving to 2_databased          ####################"
        mv $CONFIG_FOLDER/1_open/$CONFIG.ini $CONFIG_FOLDER/2_databased/
    else
        echo "#################### Moving to 4_database_failed    ####################"
        mv $CONFIG_FOLDER/1_open/$CONFIG.ini $CONFIG_FOLDER/4_database_failed/
    fi

done
