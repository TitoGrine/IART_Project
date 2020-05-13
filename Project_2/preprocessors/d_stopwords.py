from collections import Counter

class Stopwords:

    def __init__(self, word_frequency):
        self.word_frequency = word_frequency

    @staticmethod
    def stopwords_create(token_list):
        save_file = open("preprocessors/frequency_dictionary.txt", "w+")
        word_frequency = Counter(token_list)

        for word in word_frequency:
            save_file.write(word + " " + word_frequency[word] + '\n')

        save_file.close()

        return Stopwords(word_frequency)

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

    def remove_stopwords(tweet, freq_limit=1):
        processed_tweet = list(map(lambda token: self.process(token, freq_limit), tweet))
        processed_tweet = list(filter(lambda token: (token != ""), processed_tweet))

        return processed_tweet




