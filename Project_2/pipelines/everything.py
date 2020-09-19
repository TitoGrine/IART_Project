from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

from preprocessors.d_stopwords import Stopwords
from preprocessors.emojis import Emojis
<<<<<<< HEAD
=======
from preprocessors.expand import Expand
>>>>>>> 5b791facd23c54532cf29cd110517ed8143d30ac
from preprocessors.lemmatization import Lemmatization
from preprocessors.miscellaneous import Miscellaneous
from preprocessors.misspelling import Misspelling
from preprocessors.utils import fit


def everything_pipeline(x, y, clsf):
<<<<<<< HEAD
    model = make_pipeline(Stopwords(), Miscellaneous(), Misspelling(), Emojis(), Lemmatization(),
=======
    model = make_pipeline(Stopwords(), Miscellaneous(), Expand(), Misspelling(), Emojis(), Lemmatization(),
>>>>>>> 5b791facd23c54532cf29cd110517ed8143d30ac
                          TfidfVectorizer(lowercase=False, tokenizer=lambda _: _))
    vectorized_x = model.fit_transform(x, y)
    return fit(vectorized_x, y, clsf, oversample=True)
