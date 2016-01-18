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

# We need the output/error redirection, because caffe outputs to standard error, and we want to pipe to grep's standard in
# See http://stackoverflow.com/questions/1507816/with-bash-how-can-i-pipe-standard-error-into-another-process
($CAFFE_ROOT/build/tools/caffe test -model net.prototxt -weights experiments/$1/*.caffemodel -iterations 1 3>&1 1>&2- 2>&3-) | grep --invert-match "Waiting for data" > $TESTING_LOG_NAME

