from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

from classifiers.cnn import CNN
from preprocessors.lemmatization import Lemmatization
from preprocessors.tokenizer import Tokenizer
from preprocessors.utils import fit, split


def simple_pipeline(x, y):
    model = make_pipeline(Tokenizer(preserve_case=False, strip_handles=False), Lemmatization(),
                          TfidfVectorizer(lowercase=False, tokenizer=lambda _: _))
    vectorized_x = model.fit_transform(x, y)
    clsf = CNN(kernel_size=4, filters=1000, units=1000)
    x_train, y_train, x_test, y_test = split(vectorized_x, y, oversample=True)
    clsf.fit(x_train, y_train, x_test, y_test)
