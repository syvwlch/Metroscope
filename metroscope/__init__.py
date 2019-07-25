"""
Initialize the metroscope package.

WordBuilder is a class meant to hold a single word and generate
representations of aspect of its pronunciation, such as stressed syllables or
rhymes.

Linebuilder is a class meant to hold one line of verse, and it is built up
from a series of WordBuilder instances.
"""

from .WordBuilder import WordBuilder
from .LineBuilder import LineBuilder
from .custom_dict import CUSTOM_DICT

__all__ = ["WordBuilder", "LineBuilder", "CUSTOM_DICT"]
