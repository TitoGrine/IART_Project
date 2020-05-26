from emoji import demojize
from sklearn.base import BaseEstimator, TransformerMixin


class Emojis(BaseEstimator, TransformerMixin):

    def __init__(self, use_aliases=False):
        self.use_aliases = use_aliases
        self.create_dictionary()

    def create_dictionary(self):
        emoticons = {}
        with open("preprocessors/emoticons.txt") as file:
            for line in file:
                (key, val) = line.split()
                emoticons[key] = val

        self.emoticons = emoticons

    def demojize(self, token):
        token = demojize(token, use_aliases=self.use_aliases)

        if token in self.emoticons:
            token = self.emoticons[token]

        return ' '.join(token.replace(":", "").split())

    def process(self, tokens):
        return map(self.demojize, tokens)

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, tweets):
        return list(map(lambda token: self.process(token), tweets))
