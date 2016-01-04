import sys, os, csv, re, argparse, ConfigParser



def read_test_results(logPath):
    test_results = {}

    for line in file(logPath):
        if "Test net output" in line:
            search_terms = re.search('Test net output #([0-9]): (.*?) = (-?(0|1)\\.?[0-9]*)', line)
            if search_terms:
                key = str(search_terms.group(2)) + "_" + search_terms.group(1)
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
            feature_map ["_" + f[0]] = f[1]
    return feature_map


def main(experiments_path, result_file):
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
                print "#Warning: Skipped %s, log or config file was not found!" % full_d_path
                continue
            features = read_config(configFile)
            test_results = read_test_results(logFile)
            features.update(test_results)

            all_values.append(features)

    with open(result_file, 'w') as csvfile:
        fieldnames = []
        for row in all_values:
            dict_keys = row.keys()
            dict_keys.sort()
            for key in dict_keys:
                if not key in fieldnames:
                    fieldnames.append(key)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in all_values:
            writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create overview csv file of training results.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('experimentfolder', help='path to experiment folder', default='../net/experiments', nargs='?')
    parser.add_argument('output', help='path of result file', default='../net/experiments/experiments.csv', nargs='?')
    args = parser.parse_args()
    main(args.experimentfolder, args.output)
