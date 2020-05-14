from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC

from preprocessors.d_stopwords import Stopwords
from preprocessors.lemmatization import Lemmatization
from preprocessors.stemming import Stemming
from sklearn.neural_network import MLPClassifier


def stopwords_pipeline(x, y):
    model = make_pipeline(Stopwords(), Lemmatization(),
                          TfidfVectorizer(lowercase=False, tokenizer=lambda _: _), MLPClassifier())
    model.fit(x, y)
    return model
