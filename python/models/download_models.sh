#!/bin/bash

user="ms2015t3"
host="172.16.23.193"
path="/home/ms2015t3/sentence-boundary-detection-nn/net/experiments"

while IFS='' read -r model || [[ -n "$model" ]]; do
    echo "downloading model: $model..."
    mkdir $model -p
    sftp -r "$user@$host:$path/$model/net.prototxt" "$model/"
    sftp -r "$user@$host:$path/$model/*.ini" "$model/"
    sftp -r "$user@$host:$path/$model/*.caffemodel" "$model/"
done < "models.txt"
