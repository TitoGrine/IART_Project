from nltk.tokenize import TweetTokenizer 
from sklearn.base import BaseEstimator, TransformerMixin

class Tokenizer(BaseEstimator, TransformerMixin):

    def __init__(self, preserve_case=True, strip_handles=True, reduce_len=True):
        self.preserve_case = preserve_case
        self.reduce_len = reduce_len
        self.strip_handles = strip_handles

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, text):
        tweetTokenizer = TweetTokenizer(preserve_case=self.preserve_case, reduce_len=self.reduce_len, strip_handles=self.strip_handles)
        
        return tweetTokenizer.tokenize(text)
