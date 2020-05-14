from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB

from preprocessors.lemmatization import Lemmatization
from preprocessors.stemming import Stemming
from preprocessors.tokenizer import Tokenizer


def stemming_pipeline(x, y):
    model = make_pipeline(Tokenizer(preserve_case=False, strip_handles=False), Stemming("snowball"),
                          TfidfVectorizer(lowercase=False, tokenizer=lambda _: _), RandomForestClassifier())
    model.fit(x, y)
    return model
