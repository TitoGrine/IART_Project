from re import sub
from sklearn.base import BaseEstimator, TransformerMixin


class Miscellaneous(BaseEstimator, TransformerMixin):

    def __init__(self, single_letters=True, numbers=True, punctuation=True, urls=True, hashtag=True, lower_case=True):
        self.lower_case = lower_case
        self.single_letter = single_letters
        self.numbers = numbers
        self.punctuation = punctuation
        self.urls = urls
        self.hashtag = hashtag

    def apply_regex(self, token):  # Aggregate all regex first an only then apply to token?
        if self.single_letter:
            token = ' '.join(sub("$[a-zA-Z]^", "", token).split())

        if self.numbers:
            token = ' '.join(sub("[0-9]+\.?[0-9]+", "", token).split())

        if self.urls:
            token = ' '.join(sub("(\w+:\/\/\S+)", "", token).split())

        if self.punctuation:
            token = ' '.join(sub("[\.\,\!\?\:\;\-\=\+]", "", token).split())

        if self.hashtag:
            token = ' '.join(token.replace("#", "").split())  # Juntar com a punctuation?

        if self.lower_case:
            token = ' '.join(token.replace("$[A-Z][a-z]^", ""))

        return token

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def process(self, tweet):
        processed_tweet = list(map(lambda token: self.apply_regex(token), tweet))
        processed_tweet = list(filter(lambda token: (token != ""), processed_tweet))

        return processed_tweet

    def transform(self, tweets):
        return map(self.process, tweets)
