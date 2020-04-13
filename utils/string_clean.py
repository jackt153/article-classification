import re
import string
from typing import List

import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.base import BaseEstimator, TransformerMixin

DELIMITER: str = "|||"
STOPWORDS = stopwords.words("english") + [
    "options",
    "add",
    "option",
    "modifiers",
    "mods",
    "main",
    "mains",
    "menu",
    "hot",
    "side",
    "meal",
    "drink",
    "side",
    "sides",
    "selection",
    "drinks",
    "included",
    "topping",
    "toppings",
    "extra",
    "special",
    "daily",
    "bank",
    "starter",
    "starters",
    "own_options",
    "large",
    "small",
    "extra",
    "on",
    "regional",
    "remove",
    "combo",
    "choice",
    "choices",
    "specials",
    "in",
    "option_mods",
    "classic",
    "build",
    "item",
    "items",
    "medium",
    "business",
    "regular",
    "lunch_otions",
    "set",
]


class CleanStrings(BaseEstimator, TransformerMixin):
    """The class allows us to clean strings.

    The class is designed so that we can pass a pandas series of menu items.
    It is then cleaned to make the classification easier.

    To utilize the dish level it is advised that you use the below statement in your SQL query
    - LISTAGG(DISTINCT  item_name, '||')  AS rx_menu

    """

    def __init__(
        self,
        remove_digits: bool = True,
        remove_bracketed_strings: bool = True,
        stop_words: List[str] = STOPWORDS,
        alphanumeric: set = set(string.printable),
        stemmer=nltk.stem.snowball.SnowballStemmer(language="english"),
        dish_level: bool = False,
        min_num_characters: int = 2,
        stemmed_stop_words: List[str] = [],
    ):
        self.remove_digits = remove_digits
        self.stop_words = stop_words
        self.alphanumeric = alphanumeric
        self.stemmer = stemmer
        self.dish = dish_level
        self.min_num_characters = min_num_characters
        self.stemmed_stop_words = stemmed_stop_words
        self.remove_bracketed_strings = remove_bracketed_strings

    def fit(self, X: pd.Series, y=None) -> None:
        """Returns self.

        Args:
            param1 (pd.Series): Series which contains list of menu items
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
        - Removes all punctuation apart from pipe
        - Removes stop stop_words
        - Removes non alphanumeric characters
        - Uses a stemmer which can be defined above.
        - If we want dish items rather than just menu items then we can use the delimiter rather than white space.


        Args:
            param1 (pd.Series): Series which contains list of menu items
            param2 (None): Required to make the class a valid TransformerMixin

        Returns:
            self
        """
        if self.remove_digits == True:
            X = X.str.replace("\d+", "")

        if self.remove_bracketed_strings == True:
            X = X.apply(lambda x: re.sub("[\(\[].*?[\)\]]", "", x))

        X = (
            X.str.lower()
            .str.replace("[!\"#$%&'()*£+,-.:;<=>?@[\]^_`{}~]", " ")
            .apply(
                lambda x: " ".join(
                    word for word in x.split() if word not in self.stop_words
                )
            )
            .apply(lambda y: "".join(filter(lambda x: x in self.alphanumeric, y)))
            .str.replace("  ", "")
        )
        if self.stemmer is not None:
            X = X.apply(
                lambda x: " ".join(self.stemmer.stem(word) for word in x.split())
            )

        if self.dish == True:
            X = (
                X.apply(lambda x: x.replace(" " + DELIMITER, DELIMITER))
                .apply(lambda x: x.replace(" ", "_"))
                .apply(lambda x: " ".join(word for word in x.split(DELIMITER)))
                .apply(
                    lambda x: " ".join(
                        word
                        for word in x.split()
                        if len(word) > self.min_num_characters
                    )
                )
            )
        else:
            X = (
                X.str.replace(DELIMITER, "")
                .apply(
                    lambda x: " ".join(
                        word
                        for word in x.split()
                        if len(word) > self.min_num_characters
                    )
                )
                .str.replace("|", " ")
                .apply(lambda y: " ".join(word for word in y.split()))
            )

        if self.stemmed_stop_words:
            X = X.apply(
                lambda x: " ".join(
                    [word for word in x.split() if word not in self.stemmed_stop_words]
                )
            )
        return X
