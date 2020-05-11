import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin

class Tokenizer(BaseEstimator, TransformerMixin):

    def __init__(self, algorithm):
        nltk.download('wordnet')
        self.lemmatizer = WordNetLemmatizer()

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, tweet):
        for token in tweet:
            token = self.lemmatizer.lemmatize(token)

        return tweet
