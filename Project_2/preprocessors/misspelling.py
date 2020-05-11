import pkg_resources
from symspellpy import SymSpell, Verbosity
from sklearn.base import BaseEstimator, TransformerMixin

class Misspelling(BaseEstimator, TransformerMixin):

    def __init__(self, max_edit_distance=3, prefix_length=5, transfer_casing=True):
        self.max_edit_distance = max_edit_distance
        self.prefix_length = prefix_length
        self.transfer_casing = transfer_casing

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, tweets):
        sym_spell = SymSpell(max_edit_distance=self.max_edit_distance, prefix_length=self.prefix_length)
        dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
        sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

        for token in tweets:
            suggestions = sym_spell.lookup(text, Verbosity.CLOSEST, max_edit_distance=2, include_unknown=True, transfer_casing=True)
            token = suggestions[0].term

        return tweets
