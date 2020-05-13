from sklearn.base import BaseEstimator, TransformerMixin


class SparseToDense(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, X):
        return X.toarray()
