import sys, os, csv
import re
import ConfigParser
from sets import Set



# for all experiments in folder do this
#fieldnames = ['recall_per_class_1', 'loss', 'recall_per_class_3', 'recall_per_class_2', 'precision_per_class_1', 'precision_per_class_3', 'precision_per_class_2', 'accuracy', 'use_question_mark', 'punctuation_position', 'window_size', 'wikipedia', 'number_replacement', 'normalize_class_distribution', 'pos_tagging', 'key_error_vector', 'vector_file']
experiments_path = "/home/rice/Windows/uni/master4/paomr/experiments"

def read_test_results(logPath):
    test_results = {}

    for line in file(logPath):
        if "Test net output" in line:
            search_terms = re.search('Test net output #([0-9]): (.*?) = (-?(0|1)\\.?[0-9]*)', line)
            key = str(search_terms.group(1)) + "_" + search_terms.group(2)
            test_results[key] = search_terms.group(3)
    return test_results

###config
def read_config(config_path):
    sections = ['data', 'word_vector', 'windowing', 'features']

    current_config = ConfigParser.ConfigParser()
    current_config.read(config_path)
    feature_map = {}

    for section in sections: 
        for f in current_config.items(section):
            feature_map [f[0]] =  f[1]

    return feature_map

all_values = []

for d in os.listdir(experiments_path):
    full_d_path = os.path.join(experiments_path,d)
    if os.path.isdir(full_d_path):
        print full_d_path
        logFile = None
        configFile = None

        files = os.listdir(full_d_path)
        for f in files:
            if f.endswith(".tlog"):
                print f
                logFile = os.path.join(full_d_path , f)
            elif f.endswith(".ini"):
                print f
                configFile = os.path.join(full_d_path, f)

        if logFile == None or configFile == None:
            print "log or config file not found for experiment %s. So was skipped in result file!!!" % full_d_path
            continue
        features = read_config(configFile)
        test_results = read_test_results(logFile)
        features.update(test_results)

        all_values.append(features)

with open('testresults.csv', 'w') as csvfile:
    fieldnames = Set()
    for e in all_values:
        fieldnames.update(e.keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for e in all_values:
        writer.writerow(e)

