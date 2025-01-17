from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import EnglishStemmer
from sklearn.base import BaseEstimator, TransformerMixin


class Stemming(BaseEstimator, TransformerMixin):

    def __init__(self, algorithm):

        if algorithm == "lancaster":
            self.stemmer = LancasterStemmer()
        elif algorithm == "porter":
            self.stemmer = PorterStemmer()
        elif algorithm == "snowball":
            self.stemmer = EnglishStemmer()

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, tweet):
        return list(map(lambda x: map(self.stemmer.stem, x), tweet))
