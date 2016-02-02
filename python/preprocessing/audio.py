import nltk, nltk.data
from intervaltree import IntervalTree
from preprocessing.tokens import AudioToken, PunctuationToken, Punctuation
import numpy as np

class Audio(object):

    def __init__(self):
        self.sentences = []
        self.pitch_interval = IntervalTree()
        self.talk_id = 0
        self.group_name = None

        self.token_count = None

        self.PITCH_FILTER = 300.0
        self.YAAFE_STEP_SIZE = 512.0
        self.TED_AUDIO_SAMPLE_RATE = 16000.0

    def get_tokens(self):
        tokens = []
        for sentence in self.sentences:
            tokens.extend(sentence.tokens)
        return tokens

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def build_interval_tree(self):
        self.token_count = 0
        for token in self.get_tokens():
            if not token.is_punctuation():
                self.token_count += 1
                self.pitch_interval.addi(token.begin, token.begin + token.duration, token)

    def parse_pitch_feature(self, filename):
        with open(filename, "r") as file_:
            for line_unenc in file_:
                # parse line
                line = unicode(line_unenc, errors='ignore')
                line = line.rstrip()

                line_parts = line.split(" ")
                second = float(line_parts[0])
                pitch_level = float(line_parts[1])

                if pitch_level < self.PITCH_FILTER:
                    try:
                        token = next(iter(self.pitch_interval[second])).data
                        token.append_pitch_level(pitch_level)
                    except:
                        continue

        token_without_pitch = 0.0
        for sentence in self.sentences:
            avg_pitch = sentence.get_avg_pitch_level()
            for token in sentence.get_tokens():
                if not token.is_punctuation():
                    try:
                        token.pitch = (reduce(lambda x, y: x + y, token.pitch_levels) / len(token.pitch_levels)) - avg_pitch
                    except:
                        token_without_pitch += 1
                        token.pitch = 0.0

        # print("%2.2f %% of tokens had no pitch level." % (token_without_pitch / self.token_count * 100))

    def parse_energy_feature(self, filename):
        intervall = self.YAAFE_STEP_SIZE / self.TED_AUDIO_SAMPLE_RATE

        with open(filename, "r") as file_:
            i = -1
            for line_unenc in file_:
                # parse line
                line = unicode(line_unenc, errors='ignore')

                if line.startswith("%"):
                    continue

                i += 1
                energy_level = float(line.rstrip())

                try:
                    token = next(iter(self.pitch_interval[i * intervall])).data
                    token.append_energy_level(energy_level)
                except:
                    continue

        token_without_energy = 0.0
        for sentence in self.sentences:
            avg_energy = sentence.get_avg_energy_level()
            for token in sentence.get_tokens():
                if not token.is_punctuation():
                    try:
                        token.energy = (reduce(lambda x, y: x + y, token.energy_levels) / len(token.energy_levels)) - avg_energy
                    except:
                        token_without_energy += 1
                        token.energy = 0.0

        # print("%2.2f %% of tokens had no energy level." % (token_without_energy / self.token_count * 100))


    def normalize(self):
        all_pauses = np.zeros(self.token_count, dtype = np.float32)
        all_pitches = np.zeros(self.token_count, dtype = np.float32)
        all_energies = np.zeros(self.token_count, dtype = np.float32)

        i = 0
        for token in self.get_tokens():
            if not token.is_punctuation():
                # restrict pause length to 2 seconds at most
                token.pause_before = min(token.pause_before, 2)
                token.pause_after = min(token.pause_after, 2)

                all_pauses[i] = token.pause_before
                all_pitches[i] = token.pitch
                all_energies[i] = token.energy
                i += 1

        pause_mean = np.mean(all_pauses)
        pitch_mean = np.mean(all_pitches)
        energy_mean = np.mean(all_energies)

        pause_std = np.std(all_pauses)
        pitch_std = np.std(all_pitches)
        energy_std = np.std(all_energies)

        for token in self.get_tokens():
            if not token.is_punctuation():
                token.set_pause_before((token.pause_before - pause_mean) / pause_std)
                token.set_pause_after((token.pause_after - pause_mean) / pause_std)
                token.set_pitch((token.pitch - pitch_mean) / pitch_std)
                token.set_energy((token.energy - energy_mean) / energy_std)

    def __str__(self):
        sentences_str = ''.join(map(str, self.sentences))
        return sentences_str


class AudioSentence(object):

    def __init__(self):
        self.tokens = []
        self.begin = 0
        self.end = 0

    def get_avg_pitch_level(self):
        audio_tokens = []
        for token in self.tokens:
            if not token.is_punctuation():
                audio_tokens.append(token)
        l = [item for token in audio_tokens for item in token.pitch_levels]
        try:
            return reduce(lambda x, y: x + y, l) / len(l)
        except:
            # print("Sentence has no pitch levels. Setting avg_pitch to 0.0.")
            return 0.0

    def get_avg_energy_level(self):
        audio_tokens = []
        for token in self.tokens:
            if not token.is_punctuation():
                audio_tokens.append(token)
        l = [item for token in audio_tokens for item in token.energy_levels]
        try:
            return reduce(lambda x, y: x + y, l) / len(l)
        except:
            # print("Sentence has no energy levels. Setting avg_energy to 0.0.")
            return 0.0

    def prepare(self):
        for i, token in enumerate(self.tokens):
            # Capitalize first letter
            if i == 0:
                token.word = token.word.title()

            # Capitalize common words
            if token.word == "i":
                token.word = "I"

    def tokenize(self):
        sentence_str = ' '.join(map(lambda t: t.word, self.tokens))

        raw_tokens = nltk.word_tokenize(sentence_str)

        final_tokens = []

        raw_idx = 0
        for idx in range(len(self.tokens)):
            if len(self.tokens[idx].word) == len(raw_tokens[raw_idx]):
                final_tokens.append(self.tokens[idx])
                raw_idx += 1
            else:
                # we need to split up our token
                current_index = raw_idx + 2
                while ''.join(raw_tokens[raw_idx:current_index]) != self.tokens[idx].word:
                    print(raw_tokens[raw_idx:current_index], self.tokens[idx].word)
                    current_index += 1

                nr_tokens = current_index - raw_idx

                current_begin = self.tokens[idx].begin
                duration_step = self.tokens[idx].duration / nr_tokens

                for i in range(raw_idx, current_index):
                    new_token = AudioToken(raw_tokens[i])
                    new_token.duration = duration_step
                    new_token.begin = current_begin

                    current_begin += duration_step

                    final_tokens.append(new_token)

                raw_idx += nr_tokens

        assert(idx == len(self.tokens) - 1)
        assert(raw_idx == len(raw_tokens))

        final_tokens.append(PunctuationToken(".", Punctuation.PERIOD))
        self.tokens = final_tokens

    def append_token(self, token):
        self.tokens.append(token)

    def set_tokens(self, tokens):
        self.tokens = tokens

    def get_tokens(self):
        return self.tokens

    def __str__(self):
        tokens_str = ', '.join(map(str, self.tokens))

        return "begin: %s tokens: %s \n" % (self.begin, tokens_str)
