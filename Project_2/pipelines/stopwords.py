from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline

from preprocessors.d_stopwords import Stopwords
from preprocessors.lemmatization import Lemmatization
from preprocessors.utils import fit


def stopwords_pipeline(x, y, clsf):
    model = make_pipeline(Stopwords(), Lemmatization(),
                          TfidfVectorizer(lowercase=False, tokenizer=lambda _: _), MLPClassifier())
    vectorized_x = model.fit_transform(x, y)
    fit(vectorized_x, y, clsf, oversample=True)
