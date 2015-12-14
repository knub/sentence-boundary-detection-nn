import ConfigParser, os
import itertools

# Set global config variable to be initialized in SbdConfig#init
config = None

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

    def get_db_name(self):
        sentence_home = os.environ['SENTENCE_HOME']
        LEVEL_DB_DIR = "leveldbs"

        # create proper name for the database
        return sentence_home + "/" + LEVEL_DB_DIR + "/" + \
               config.get('word_vector', 'vector_file') + \
               "_window-" + config.get('windowing', 'window_size') + "-" + config.get('windowing', 'punctuation_position') + \
               "_pos-"  + config.get('features', 'pos_tagging') + \
               "_qm-"   + config.get('features', 'use_question_mark') + \
               "_balanced-" + config.get('data', 'normalize_class_distribution') + \
               "_nr-rep-"   + config.get('features', 'number_replacement') + \
               "_word-" + config.get('word_vector', 'key_error_vector')

    def generate_config_files(self):
        config_file = {
            'data': {}, 'word_vector': {}, 'windowing': {}, 'features': {}
        }


        option_settings = {
            ('data', 'normalize_class_distribution'): ['true', 'false'],
            ('data', 'train_files'): [
                'ted/2010-1.xml,ted/2010-2.xml,ted/2012.xml,ted/2013.xml',
                # 'wikipedia/wikipedia.txt',
                'ted/2010-1.xml,ted/2010-2.xml,ted/2012.xml,ted/2013.xml,wikipedia/wikipedia.txt'
            ],
            ('word_vector', 'vector_file'): ['glove', 'google'],
            ('features', 'pos_tagging'): ['true', 'false'],
            ('features', 'number_replacement'): ['true', 'false'],
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
            (1, 0),
            (1, 1)
        ]
        punctuation_settings = [
            [(('windowing', 'window_size'), str(window_size)), (('windowing', 'punctuation_position'), str(punctuation_pos)) ]
            for window_size, punctuation_pos in punctuation_settings
        ]
        cartesian_settings.append(punctuation_settings)

        print "Debugging: "
        for s in cartesian_settings:
            print str(s)

        configurations = list(itertools.product(*cartesian_settings))
        print "Creating " + str(len(configurations)) + " different config files."
        for c in configurations:
            print "-----------------------------------"
            c = list(itertools.chain(*c))
            c.append((('data', 'test_files'), 'ted/2011.xml'))
            c.append((('word_vector', 'key_error_vector'), 'this'))
            c.append((('features', 'use_question_mark'), 'false'))
            c = sorted(c, key = lambda x: x[0][0])
            for group, options in itertools.groupby(c, key = lambda x: x[0][0]):
                print "[" + str(group) + "]"
                for o in options:
                    print o[0][1] + " = " + o[1]
                print ""

# config = SbdConfig(None)
# config.generate_config_files()
