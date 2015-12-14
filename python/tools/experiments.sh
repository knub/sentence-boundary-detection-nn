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

for CONFIG_FILE in "$CONFIG_FOLDER"/*
do
    cd $SENTENCE_HOME/python/
    CONFIG=$(basename ${CONFIG_FILE})
    CONFIG="${CONFIG%.*}"
    echo "#################### Running with $CONFIG ####################"
    echo "#################### Creating database         ####################"
    python sbd_leveldb/training_instance_generator.py $CONFIG_FILE
    echo "#################### Configuring net           ####################"
    python tools/netconfig.py ../net/net.prototxt -o ../net/auto.prototxt -t $SENTENCE_HOME/leveldbs/$CONFIG
    echo "#################### Starting training         ####################"
    cd $SENTENCE_HOME/net/
    ./training.sh $CONFIG
    echo "#################### Removing net definition   ####################"
    rm auto.prototxt
    # echo "#################### Deleting database         ####################"
    # rm -r $SENTENCE_HOME/leveldbs/$CONFIG
done
