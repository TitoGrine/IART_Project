from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline

from preprocessors.tokenizer import Tokenizer
from preprocessors.emojis import Emojis


def emojis_pipeline(x, y):
    model = make_pipeline(Tokenizer(preserve_case=False, strip_handles=False), Emojis(), TfidfVectorizer(lowercase=False, tokenizer=lambda _: _), MLPClassifier())
    model.fit(x, y)
    return model
