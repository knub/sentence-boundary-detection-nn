import ConfigParser, os
from sets import Set

allowed_sections = Set(['word_vector', 'windowing', 'features', 'data'])
allowed_options = Set(['key_error_vector', 'window_size', 'punctuation_position', 'use_question_mark', 'pos_tagging', 'normalize_class_distribution', 'vector', 'number_replacement', 'wikipedia'])

config_path = os.path.join(os.getcwd(), 'config.ini')
if 'SENTENCE_HOME' in os.environ:
    # if environment variable is set, we take that directory instead
    config_path = os.path.join(os.environ['SENTENCE_HOME'], 'python/config.ini')
config = ConfigParser.ConfigParser()
print("Reading config: %s" % config_path)
config.read(config_path)

# check validity:
for section in config.sections():
    assert section in allowed_sections, "Section " + section + " is not allowed!"
    allowed_sections.remove(section)
    for (name, value) in config.items(section):
        assert name in allowed_options, "Key " + name + " is not allowed!"
        allowed_options.remove(name)

assert len(allowed_sections) == 0, "Not all sections were set in config.ini: " + str(allowed_sections)
assert len(allowed_options) == 0,  "Not all options were set in config.ini: "  + str(allowed_options)
