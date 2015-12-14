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

# Abort on first error
set -e

for config_file in "$CONFIG_FOLDER"/*
do
    cd $SENTENCE_HOME/python/
    echo "#################### Running with $config_file ####################"
    echo "#################### Creating database         ####################"
    python sbd_leveldb/training_instance_generator.py $config_file
    echo "#################### Configuring net           ####################"
	python tools/netconfig.py ../net/net.prototxt -o ../net/auto.prototxt -t $SENTENCE_HOME/leveldbs/$config_file
    cd $SENTENCE_HOME/net/
    echo "#################### Starting training         ####################"
	./training.sh
    echo "#################### Deleting database         ####################"
	rm -r $SENTENCE_HOME/leveldbs/$config_file
done
