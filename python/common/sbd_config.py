import ConfigParser, os
from sets import Set

config_file_schema = {
    'data': {
        'normalize_class_distribution': [True, False],
        'use_wikipedia': [True, False]
    },
    'word_vector': {
        'key_error_vector': None,
        'vector_file': ['small', 'glove', 'google'],
    },
    'windowing': {
        'window_size': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'punctuation_position': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    },
    'features': {
        'use_question_mark': [True, False]
        'pos_tagging': [True, False]
        'number_replacement': [True, False]
    }
}

config_path = os.path.join(os.getcwd(), 'config.ini')
if 'SENTENCE_HOME' in os.environ:
    # if environment variable is set, we take that directory instead
    config_path = os.path.join(os.environ['SENTENCE_HOME'], 'python/config.ini')

config = ConfigParser.ConfigParser()
print("Reading config: %s" % config_path)
config.read(config_path)

allowed_sections = config_file_schema.keys()
allowed_options = [option for section in allowed_sections for option in config_file_schema[section].keys()]
print "Debugging: " + str(allowed_sections)
print "Debugging: " + str(allowed_options)

#
# Check validity
#
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
            assert value in data_range, "Value " + str(value) + " is not allowed for option " + str(name) + " with range " + str(data_range) + "!"

assert len(allowed_sections) == 0, "Not all sections were set in config.ini: " + str(allowed_sections)
assert len(allowed_options) == 0,  "Not all options were set in config.ini: "  + str(allowed_options)
