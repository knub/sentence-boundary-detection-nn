import ConfigParser
from sets import Set
import os

allowed_sections = Set(['word_vector', 'windowing', 'features'])
allowed_options = Set(['key_error_vector', 'window_size', 'punctuation_position', 'use_question_mark', 'pos_tagging'])

sentence_home = os.environ['SENTENCE_HOME']
config = ConfigParser.ConfigParser()
config.read(sentence_home + '/python/config.ini')

# check validity:
for section in config.sections():
    assert section in allowed_sections, "Section " + section + " is not allowed!"
    allowed_sections.remove(section)
    for (name, value) in config.items(section):
        assert name in allowed_options, "Key " + name + " is not allowed!"
        allowed_options.remove(name)

assert len(allowed_sections) == 0, "Not all sections were set in config.ini: " + str(allowed_sections)
assert len(allowed_options) == 0,  "Not all options were set in config.ini: "  + str(allowed_options)
