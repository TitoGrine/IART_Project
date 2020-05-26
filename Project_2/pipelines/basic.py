
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

from preprocessors.tokenizer import Tokenizer
from preprocessors.utils import fit


def basic_pipeline(x, y, clsf):
    model = make_pipeline(Tokenizer(), TfidfVectorizer(lowercase=False, tokenizer=lambda _: _))
    vectorized_x = model.fit_transform(x, y)
    return fit(vectorized_x, y, clsf, oversample=True)
