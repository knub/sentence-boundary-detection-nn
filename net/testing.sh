#!/usr/bin/env bash

PROJECT="sentence"
TESTING_LOG_NAME="${PROJECT}.tstlog"

# Check if called with name
if [ $# -ne 1 ]; then
    echo "Usage: $0 [experiment_name]"
	echo "       experiment_name: Name of the subfolder in ./experiments/ for the current experiment."
	echo "Exiting."
	exit 1
fi

$CAFFE_ROOT/build/tools/caffe test -model net.prototxt -weights experiments/$1/*.caffemodel -iterations 1 2> $TESTING_LOG_NAME

