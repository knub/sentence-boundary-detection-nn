import ConfigParser

allowed_sections = ['word_vector', 'windowing', 'features']
allowed_configuration = [ 'key_error_vector', 'window_size', 'punctuation_position', 'use_question_mark' ]
config = ConfigParser.ConfigParser()
config.read('config.ini')

# check validity:
for section in config.sections():
    assert section in allowed_sections, "Section " + section + " is not allowed!"
    for (name, value) in config.items(section):
        assert name in allowed_configuration, "Key " + name + " is not allowed!"
