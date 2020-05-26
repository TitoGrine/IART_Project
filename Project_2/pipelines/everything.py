from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

from preprocessors.d_stopwords import Stopwords
from preprocessors.emojis import Emojis
from preprocessors.expand import Expand
from preprocessors.lemmatization import Lemmatization
from preprocessors.miscellaneous import Miscellaneous
from preprocessors.misspelling import Misspelling
from preprocessors.utils import fit


def everything_pipeline(x, y, clsf):
    model = make_pipeline(Stopwords(), Miscellaneous(), Expand(), Misspelling(), Emojis(), Lemmatization(),
                          TfidfVectorizer(lowercase=False, tokenizer=lambda _: _))
    vectorized_x = model.fit_transform(x, y)
    return fit(vectorized_x, y, clsf, oversample=True)
