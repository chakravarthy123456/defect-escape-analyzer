"""
Text matching utilities.

Provides whole-word and whole-phrase matching for scenario indicators.
"""

import re


def contains_term(text: str, term: str) -> bool:
    """
    Return True if the term appears in the text as a whole word
    or whole phrase, ignoring letter case.
    """

    pattern = rf"\b{re.escape(term.lower())}\b"

    return re.search(pattern, text.lower()) is not None
