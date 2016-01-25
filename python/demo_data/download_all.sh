#!/bin/bash

user="ms2015t3"
host="172.16.23.193"
path="/home/ms2015t3/demo_data"

while IFS='' read -r folder || [[ -n "$folder" ]]; do
    echo "downloading folder: $folder..."
    mkdir "$folder" -p
    sftp -r "$user@$host:$path/$folder" .
    echo -e "*\n!.gitignore" > "$folder/.gitignore"
done < "folders.txt"
