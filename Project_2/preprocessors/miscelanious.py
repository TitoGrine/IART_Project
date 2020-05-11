from re import sub
from sklearn.base import BaseEstimator, TransformerMixin

class Miscelanious(BaseEstimator, TransformerMixin):

    def __init__(self, single_letters=True, numbers=True, punctuation=True, URLs=True, hashtag=True):
        self.single_letter = single_letters
        self.numbers = numbers
        self.punctuation = punctuation
        self.URLs = URLs
        self.hashtag = hashtag

    def apply_regex(token): #Aggregate all regex first an only then apply to token?
        if self.single_letter:
            token = ' '.join(re.sub("[a-zA-Z]", "", token).split())

        if self.numbers:
            token = ' '.join(re.sub("[0-9]+\.?[0-9]+", "", token).split())

        if self.punctuation:
            token = ' '.join(re.sub("[\.\,\!\?\:\;\-\=\+]", "", token).split())

        if self.URLs:
            token = ' '.join(re.sub("(\w+:\/\/\S+)", "", token).split())

        if self.hashtag:
            token = ' '.join(re.sub("#", "", token).split()) #Juntar com a punctuation?
        
    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, tweet):
        for token in tweet:
            self.apply_regex(token)

        tweet.remove("")

        return tweet        
