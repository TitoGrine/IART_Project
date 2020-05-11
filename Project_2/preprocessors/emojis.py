from emoji import demojize
from re import sub
from sklearn.base import BaseEstimator, TransformerMixin

class Emojis(BaseEstimator, TransformerMixin):

    def __init__(self, use_aliases=False):
        self.use_aliases = use_aliases
        self.create_dictionary()

    def create_dictionary():
        emoticons = {}
        with open("preprocessors/emoticons.txt") as file: #TODO: Poderá ter de se tirar 'preprocessors/'
            for line in file:
                (key, val) = line.split()
                emoticons[key] = val

        self.emoticons = emoticons

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, tweet):
        for token in tweet:
            token = demojize(token, use_aliases=self.use_aliases)

            if token in self.emoticons:
                token = self.emoticons[token]

        token = ' '.join(token.replace(":", "").split())
        
        return tweet
