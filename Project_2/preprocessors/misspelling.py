import pkg_resources
from symspellpy import SymSpell, Verbosity
from sklearn.base import BaseEstimator, TransformerMixin

class Misspelling(BaseEstimator, TransformerMixin):

    def __init__(self, max_edit_distance=3, prefix_length=5, transfer_casing=True):
        self.max_edit_distance = max_edit_distance
        self.prefix_length = prefix_length
        self.transfer_casing = transfer_casing
        self.sym_spell = SymSpell(max_dictionary_edit_distance=self.max_edit_distance, prefix_length=self.prefix_length)
        dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
        self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    def process(self, token):
        suggestions = self.sym_spell.lookup(token, Verbosity.CLOSEST, max_edit_distance=2, include_unknown=True, transfer_casing=True)
        return suggestions[0].term

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, tweet):
        return list(map(lambda token: self.process(token), tweet))
