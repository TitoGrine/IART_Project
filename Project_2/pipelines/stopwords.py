from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

from preprocessors.d_stopwords import Stopwords
from preprocessors.utils import fit


def stopwords_pipeline(x, y, clsf):
    model = make_pipeline(Stopwords(),
                          TfidfVectorizer(lowercase=False, tokenizer=lambda _: _))
    vectorized_x = model.fit_transform(x, y)
    return fit(vectorized_x, y, clsf, oversample=True)
