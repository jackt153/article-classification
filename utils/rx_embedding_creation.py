from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from common_utils.string_clean import CleanStrings


class RxEmbedding(BaseEstimator, TransformerMixin):
    """
    The module takes in pre trainned embedding and menu items for each restaurant.

    For each restaurant it then works out the average word embeddings which creates
    the restaurant embedding.

    """

    def __init__(
        self,
        word_to_int_dict: Dict[str, int],
        emb_matrix: np.ndarray,
        clean_strings: bool,
    ):
        self.word_to_int_dict = word_to_int_dict
        self.emb_matrix = emb_matrix
        self.clean_strings = clean_strings

    def fit(self, X: pd.Series, y=None) -> None:
        """Returns self.

        Args:
            X (pd.Series): Series which contains list of menu items
            y (None): Required to make the class a valid TransformerMixin

        Returns:
            self

        """
        return self

    def transform(self, X: pd.Series, y=None) -> pd.DataFrame:
        """For all rx calculates embeddings

        For all the restaurant in the X series we process each one and create
        a DataFrame containing all the embeddings. The index of X will make up
        the column names.

        Args:
            X (pd.Series): Series which contains list of menu items
            y (None): Required to make the class a valid TransformerMixin

        Returns:
            pd.DataFrame of restaurant embeddings.
        """
        if self.clean_strings == True:
            X = CleanStrings().transform(X)

        results = np.zeros([self.emb_matrix.shape[1], len(X)])

        for i in range(0, len(X)):
            results[:, i] = self._create_emb_vector_per_rx(X.iloc[i].split())

        df_results = pd.DataFrame(results, columns=X.index)
        return df_results.transpose()

    def _create_emb_vector_per_rx(self, menu_list: List[str]) -> np.ndarray:
        """Create embedding for rx

        We initialise an ndarray with the same number of columns as words in the
        menu (which match words in the dictionary). Update each column with the
        word embeddings vector. We then sum across all the columns and divide
        by the number of columns.

        Args:
            menu_list (List[str]): A list of all the words in a menu

        Returns
            numpy array which is the embedding for the rx.
        """

        int_representation_list = list(
            filter(None, [self.word_to_int_dict.get(word) for word in menu_list])
        )

        menu_matrix = np.zeros([self.emb_matrix.shape[1], len(int_representation_list)])

        for j, word in enumerate(int_representation_list):
            menu_matrix[:, j] = self.emb_matrix[word, :]

        return np.divide(menu_matrix.sum(axis=1), (j + 1))
