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

for config_file in "$CONFIG_FOLDER"/*
do
    echo "$config_file"
    # Copy?
    # cp $config_file config.ini
    # python sbd_leveldb/training_instance_generator.py
    # Call script to adapt net.prototxt
    # Call training.sh script
done
