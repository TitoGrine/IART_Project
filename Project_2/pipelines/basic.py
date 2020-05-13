from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from preprocessors.sparse_to_dense import SparseToDense
from preprocessors.tokenizer import Tokenizer


def basic_pipeline(x, y):
    model = make_pipeline(Tokenizer(), TfidfVectorizer(lowercase=False, tokenizer=lambda _: _), SparseToDense(), MultinomialNB())
    model.fit(x, y)
    return model
