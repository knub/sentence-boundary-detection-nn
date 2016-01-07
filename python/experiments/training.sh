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

source $SENTENCE_HOME/use_python p2

for CONFIG_FILE in "$CONFIG_FOLDER"/2_databased/*
do
    cd $SENTENCE_HOME/python/
    CONFIG=$(basename ${CONFIG_FILE})
    CONFIG="${CONFIG%.*}"
    echo "#################### Training with $CONFIG          ####################"
    echo "#################### Configuring net                ####################"
    python tools/netconfig.py ../net/net.prototxt -o ../net/auto.prototxt -t $SENTENCE_HOME/leveldbs/$CONFIG
    echo "#################### Starting training              ####################"
    date
    cd $SENTENCE_HOME/net/
    ./training.sh $CONFIG

    if [ $? -eq 0 ]; then
        echo "#################### Moving to 3_trained            ####################"
        cd $SENTENCE_HOME/python/
        mv $CONFIG_FOLDER/2_databased/$CONFIG.ini $CONFIG_FOLDER/3_trained
    else
        echo "#################### Moving to 5_training_failed    ####################"
        cd $SENTENCE_HOME/python/
        mv $CONFIG_FOLDER/2_databased/$CONFIG.ini $CONFIG_FOLDER/5_training_failed
    fi
    echo "#################### Removing net definition   ####################"
    rm auto.prototxt
done
