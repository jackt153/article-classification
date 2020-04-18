import re
import string
from typing import List

import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.base import BaseEstimator, TransformerMixin

STOPWORDS = stopwords.words("english")

class CleanStrings(BaseEstimator, TransformerMixin):
    """The class allows us to clean strings.

    The class is designed so that we can pass a pandas series of articles.
    It is then cleaned to make the classification easier.

    """

    def __init__(
        self,
        remove_digits: bool = True,
        stop_words: List[str] = STOPWORDS,
        alphanumeric: set = set(string.printable),
        stemmer=nltk.stem.snowball.SnowballStemmer(language="english"),
        min_num_characters: int = 2,

    ):
        self.remove_digits = remove_digits
        self.stop_words = stop_words
        self.alphanumeric = alphanumeric
        self.stemmer = stemmer
        self.min_num_characters = min_num_characters

    def fit(self, X: pd.Series, y=None) -> None:
        """Returns self.

        Args:
            param1 (pd.Series): Series which contains strings
            param2 (None): Required to make the class a valid TransformerMixin

        Returns:
            self

        """
        return self

    def transform(self, X: pd.Series, y=None) -> pd.Series:
        """Text is converted into a more friendly NLP format

        A Pandas Series is passed in with each row being a restaurant's menu items.
        - Removes characters within the brackets (optional).
        - Lowercase
        - Removes all digits
        - Removes all punctuation
        - Removes stop stop_words
        - Removes non alphanumeric characters
        - Uses a stemmer which can be defined above.

        Args:
            param1 (pd.Series): Series which contains strings
            param2 (None): Required to make the class a valid TransformerMixin

        Returns:
            self
        """
        if self.remove_digits == True:
            X = X.str.replace("\d+", "")

        X = (
            X.str.lower()
            .str.replace("[!\"#$%&'()*£+,-.:;<=>?@[\]^_`{}~]", " ")
            .apply(
                lambda x: " ".join(
                    word for word in x.split() if word not in self.stop_words
                )
            )
            .apply(lambda y: "".join(filter(lambda x: x in self.alphanumeric, y)))
        )

        if self.stemmer is not None:
            X = X.apply(
                lambda x: " ".join(self.stemmer.stem(word) for word in x.split())
            )

        return X
