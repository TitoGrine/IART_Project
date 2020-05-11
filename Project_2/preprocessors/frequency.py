from collections import Counter
from sklearn.base import BaseEstimator, TransformerMixin

class Tokenizer(BaseEstimator, TransformerMixin):

    def __init__(self, cut_limit=1):
        self.cut_limit = cut_limit

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, tweets):
        word_frequency = Counter(tweets)

        for token in tweets:
            if word_frequency[token] <= self.cut_limit:
                tweets.remove(token)

        return tweets
