from re import sub
from sklearn.base import BaseEstimator, TransformerMixin

class Miscellaneous(BaseEstimator, TransformerMixin):

    def __init__(self, single_letters=True, numbers=True, punctuation=True, urls=True, hashtag=True):
        self.single_letter = single_letters
        self.numbers = numbers
        self.punctuation = punctuation
        self.urls = urls
        self.hashtag = hashtag

    def apply_regex(token): #Aggregate all regex first an only then apply to token?
        if self.single_letter:
            token = ' '.join(sub("\b[a-zA-Z]\b", "", token).split())

        if self.numbers:
            token = ' '.join(sub("[0-9]+\.?[0-9]+", "", token).split())

        if self.urls:
            token = ' '.join(sub("(\w+:\/\/\S+)", "", token).split())

        if self.punctuation:
            token = ' '.join(sub("[\.\,\!\?\:\;\-\=\+]", "", token).split())

        if self.hashtag:
            token = ' '.join(token.replace("#", "").split()) #Juntar com a punctuation?

        return token
        
    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, tweet):
        processed_tweet = list(map(self.apply_regex, tweet))
        processed_tweet.remove("")

        return processed_tweet        
