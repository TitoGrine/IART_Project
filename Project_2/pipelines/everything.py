from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC

from preprocessors.d_stopwords import Stopwords
from preprocessors.lemmatization import Lemmatization
from preprocessors.stemming import Stemming
from preprocessors.miscellaneous import Miscellaneous
from preprocessors.misspelling import Misspelling


def everything_pipeline(x, y):
    model = make_pipeline(Stopwords(), Lemmatization(), Miscellaneous(),
                          Misspelling(), TfidfVectorizer(lowercase=False, tokenizer=lambda _: _), MLPClassifier())
    model.fit(x, y)
    return model
