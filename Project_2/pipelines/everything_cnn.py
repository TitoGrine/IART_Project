from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

from classifiers.cnn import CNN
from preprocessors.d_stopwords import Stopwords
from preprocessors.lemmatization import Lemmatization
from preprocessors.miscellaneous import Miscellaneous
from preprocessors.misspelling import Misspelling
from preprocessors.utils import split


def everything_cnn_pipeline(x, y, clsf):
    model = make_pipeline(Stopwords(), Lemmatization(), Miscellaneous(),
                          Misspelling(), TfidfVectorizer(lowercase=False, tokenizer=lambda _: _))
    vectorized_x = model.fit_transform(x, y)
    x_train, y_train, x_test, y_test = split(vectorized_x, y, oversample=True)
    clsf.fit(x_train, y_train, x_test, y_test)