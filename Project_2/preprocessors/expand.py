from sklearn.base import BaseEstimator, TransformerMixin

class Expand(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.create_dictionary()

    def create_dictionary(self):
        contractions = {}
        with open("preprocessors/contractions.txt") as file: 
            for line in file:
                (key, val) = line.split(':')
                contractions[key] = ' '.join(val.replace(":", "").split())

        self.contractions = contractions

    def expand(self, token):
        if token in self.contractions:
            token = self.emoticons[token]

        return token

    def process(self, tokens):
        return map(self.expand, tokens)

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, tweets):
        return list(map(lambda token: self.process(token), tweets))
