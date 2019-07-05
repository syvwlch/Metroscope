"""
Initialize the metroscope package.

WordBuilder is a class meant to hold a single word and generate
representations of aspect of its pronunciation, such as stressed syllables or
rhymes.

Linebuilder is a class meant to hold one line of verse, and it is built up
from a series of WordBuilder instances.

scanned_poem() is a function that takes the raw text of a poem, and using a
series of LineBuilder instances, themselves made of series of WordBuilder
instances, returns an HTML table with the poem's text with the scansion made
visible in one column, and the rhyme scheme in another.
"""

from .WordBuilder import WordBuilder
from .LineBuilder import LineBuilder
from .scanned_poem import scanned_poem

__all__ = ["WordBuilder", "LineBuilder", "scanned_poem"]
