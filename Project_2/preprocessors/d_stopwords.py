from collections import Counter
import numpy as np

from preprocessors.tokenizer import Tokenizer


class Stopwords(Tokenizer):

    def stopwords_create(self, token_list):
        save_file = open("preprocessors/frequency_dictionary.txt", "w+")
        self.word_frequency = Counter(np.concatenate(token_list).ravel().tolist())

        for word in self.word_frequency:
            save_file.write(word + " " + str(self.word_frequency[word]) + '\n')

        save_file.close()

    @staticmethod
    def stopwords_import(path):
        word_frequency = {}

        with open(path) as file:
            for line in file:
                (key, val) = line.split()
                word_frequency[key] = val

        return Stopwords(word_frequency)

    def process(self, token, freq_limit):
        if not self.word_frequency[token] > freq_limit:
            token = ""

        return token

    def remove_stopwords(self, tweet, freq_limit=1):
        processed_tweet = list(map(lambda token: self.process(token, freq_limit), tweet))
        processed_tweet = list(filter(lambda token: (token != ""), processed_tweet))

        return processed_tweet

    def transform(self, tweets):
        tokens = super().transform(tweets)
        self.stopwords_create(tokens)

        return map(lambda tweet: self.remove_stopwords(tweet), tokens)
