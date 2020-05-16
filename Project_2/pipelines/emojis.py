from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline

from preprocessors.tokenizer import Tokenizer
from preprocessors.emojis import Emojis
from preprocessors.utils import fit


def emojis_pipeline(x, y, clsf):
    model = make_pipeline(Tokenizer(preserve_case=False, strip_handles=False), Emojis(),
                          TfidfVectorizer(lowercase=False, tokenizer=lambda _: _))
    vectorized_x = model.fit_transform(x, y)
    fit(vectorized_x, y, clsf, oversample=True)
    return model
