import ConfigParser, os
import itertools
import shutil

# Set global config variable to be initialized in SbdConfig#init
config = None

CONFIGURATIONS_DIR = "configurations"

config_file_schema = {
    'data': {
        'normalize_class_distribution': ['true', 'false'],
        'train_files': None,
        'test_files': None
    },
    'word_vector': {
        'key_error_vector': None,
        'vector_file': ['small', 'glove', 'google'],
        },
    'windowing': {
        'window_size': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'punctuation_position': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    },
    'features': {
        'use_question_mark': ['true', 'false'],
        'pos_tagging': ['true', 'false'],
        'number_replacement': ['true', 'false']
    },
    'model': {
        'lexical': ['true', 'false']
    }
}


class SbdConfig(object):

    def __init__(self, config_path):
        self.config_path = config_path

        # if config_path not set, use default config file
        if self.config_path is None:
            config_path = os.path.join(os.getcwd(), 'config.ini')
            if 'SENTENCE_HOME' in os.environ:
                # if environment variable is set, we take that directory instead
                config_path = os.path.join(os.environ['SENTENCE_HOME'], 'python/config.ini')

        self._read_config(config_path)
        self._validate()

    def _read_config(self, config_path):
        global config
        config = ConfigParser.ConfigParser()
        print("Reading config: %s" % config_path)
        config.read(config_path)

    def _validate(self):
        allowed_sections = config_file_schema.keys()
        allowed_options = [option for section in allowed_sections for option in config_file_schema[section].keys()]

        for section in config.sections():
            # Check if section is allowed
            assert section in config_file_schema.keys(), "Section " + section + " is not allowed!"
            # Remove current section, so we can later check, whether all sections have been covered
            allowed_sections.remove(section)

            for (name, value) in config.items(section):
                # Check if option is allowed
                assert name in allowed_options, "Key " + name + " is not allowed!"
                # Same as before
                allowed_options.remove(name)

                # Check allowed data range
                data_range = config_file_schema[section][name]
                if data_range is not None:
                    # stringify data range so we can compare with `value`, which is a string
                    data_range = [str(data_range_point) for data_range_point in data_range]
                    assert value in data_range, "Value " + str(value) + " is not allowed for option `" + str(name) + "` with range " + str(data_range) + "!"

        assert len(allowed_sections) == 0, "Not all sections were set in config.ini: " + str(allowed_sections)
        assert len(allowed_options) == 0,  "Not all options were set in config.ini: "  + str(allowed_options)

    @staticmethod
    def get_db_name_from_config(config):
        if config.getboolean('model', 'lexical'):
            uses_ted  = '_ted'  if 'ted'  in config.get('data', 'train_files') else ''
            uses_wiki = '_wiki' if 'wiki' in config.get('data', 'train_files') else ''
            # create proper name for the database
            return config.get('word_vector', 'vector_file') + uses_ted + uses_wiki + \
                   "_window-" + config.get('windowing', 'window_size') + "-" + config.get('windowing', 'punctuation_position') + \
                   "_pos-"  + config.get('features', 'pos_tagging') + \
                   "_qm-"   + config.get('features', 'use_question_mark') + \
                   "_balanced-" + config.get('data', 'normalize_class_distribution') + \
                   "_nr-rep-"   + config.get('features', 'number_replacement') + \
                   "_word-" + config.get('word_vector', 'key_error_vector')
        else:
            return "audio" + "_window-" + config.get('windowing', 'window_size') + "-" + config.get('windowing', 'punctuation_position')

    @staticmethod
    def generate_config_files():
        option_settings = {
            ('data', 'normalize_class_distribution'): ['true'],
            ('data', 'train_files'): [
                'ted/2010-1.xml.line,ted/2010-2.xml.line,ted/2012.xml.line,ted/2013.xml.line',
                # 'wikipedia/wikipedia.txt.line',
                'ted/2010-1.xml.line,ted/2010-2.xml.line,ted/2012.xml.line,ted/2013.xml.line,wikipedia/wikipedia.txt.line'
                # audio/dev2010_talkid129.ctm, audio/dev2010_talkid453.ctm, audio/dev2010_talkid531.ctm, audio/dev2010_talkid69.ctm, audio/dev2012_talkid1270.ctm, audio/dev2012_talkid1286.ctm, audio/dev2012_talkid1289.ctm, audio/dev2012_talkid1309.ctm, audio/dev2012_talkid1322.ctm, audio/dev2010_talkid227.ctm, audio/dev2010_talkid457.ctm, audio/dev2010_talkid535.ctm, audio/dev2010_talkid93.ctm, audio/dev2012_talkid1280.ctm, audio/dev2012_talkid1288.ctm, audio/dev2012_talkid1297.ctm, audio/dev2012_talkid1312.ctm, audio/dev2012_talkid1327.ctm, audio/tst2012_0.ctm, audio/tst2012_1.ctm, audio/tst2012_2.ctm, audio/tst2012_3.ctm
            ],
            ('word_vector', 'vector_file'): ['google'],
            ('features', 'pos_tagging'): ['true', 'false'],
            ('features', 'number_replacement'): ['true'],
        }
        # Now transform the option list from the data structure above to the following_structure
        # [
        #     [ (('data', 'normalize_class_distribution'), 'true'), (('data', 'normalize_class_distribution'), 'false') ],
        #     [ .. next option .. ],
        #     ...
        # ]
        # We can then use the cartesian product on this list to get all possible configs.
        cartesian_settings = []
        for option, values in option_settings.iteritems():
            options = [ [(option, value)] for value in values ]
            cartesian_settings.append(options)


        # Now add the possible settings for the punctuation
        # [(window_size, punctuation_pos)]
        punctuation_settings = [
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3),
            (5, 4),
            (5, 5),
            (8, 0),
            (8, 2),
            (8, 4),
            (8, 6),
            (8, 8)
        ]
        punctuation_settings = [
            [(('windowing', 'window_size'), str(window_size)), (('windowing', 'punctuation_position'), str(punctuation_pos)) ]
            for window_size, punctuation_pos in punctuation_settings
        ]
        cartesian_settings.append(punctuation_settings)

        configurations = list(itertools.product(*cartesian_settings))
        shutil.rmtree(CONFIGURATIONS_DIR, True)
        os.mkdir(CONFIGURATIONS_DIR)
        os.mkdir(CONFIGURATIONS_DIR + "/1_open")
        os.mkdir(CONFIGURATIONS_DIR + "/2_databased")
        os.mkdir(CONFIGURATIONS_DIR + "/3_trained")
        os.mkdir(CONFIGURATIONS_DIR + "/4_database_failed")
        os.mkdir(CONFIGURATIONS_DIR + "/5_training_failed")

        for c in configurations:
            # the following operation performs a flatten on the current configuration
            c = list(itertools.chain(*c))
            # now add the static option settings
            c.append((('data', 'test_files'), 'ted/2011.xml.line')) # audio/tst2011_0.ctm, audio/tst2011_1.ctm, audio/tst2011_2.ctm, audio/tst2011_3.ctm
            c.append((('word_vector', 'key_error_vector'), 'this'))
            c.append((('features', 'use_question_mark'), 'false'))
            # sort and group by to output the options in correct *.ini order
            f = open(CONFIGURATIONS_DIR + "/tmp", "w")
            c = sorted(c, key = lambda x: x[0][0])
            for group, options in itertools.groupby(c, key = lambda x: x[0][0]):
                f.write("[" + str(group) + "]\n")
                for o in options:
                    f.write(o[0][1] + " = " + o[1] + "\n")
                f.write("\n")
            f.close()

            # create the appropriate name for the current config
            current_config_parser = ConfigParser.ConfigParser()
            current_config_parser.read(CONFIGURATIONS_DIR + "/tmp")
            shutil.move(CONFIGURATIONS_DIR + "/tmp", CONFIGURATIONS_DIR + "/1_open/" + SbdConfig.get_db_name_from_config(current_config_parser) + ".ini")

        print "Created " + str(len(configurations)) + " different config files in " + CONFIGURATIONS_DIR + "/1_open"


if __name__ == '__main__':
    SbdConfig.generate_config_files()
