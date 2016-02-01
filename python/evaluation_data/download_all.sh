#!/bin/bash

user="ms2015t3"
host="172.16.23.193"

mkdir -p data
scp "$user@$host:/mnt/naruto/sentence/data/audio/tst2011_*.{ctm,energy,pitch}" data/

mkdir -p audio_models
scp -r "$user@$host:/home/ms2015t3/sentence-boundary-detection-nn/net-audio/experiments/20160126-053506_audio_window-8-4" audio_models/

mkdir -p lexical_models
scp -r "$user@$host:/home/ms2015t3/sentence-boundary-detection-nn/net/experiments/20160111-131832_google_ted_window-8-4_pos-true_qm-false_balanced-false_nr-rep-true_word-this" lexical_models/
