"""The class that provides the representation for a line of verse."""

from metroscope import WordBuilder


class LineBuilder(object):
    """
    Prepare a given line of verse for analysis.

    Line is stored as a list of instances of the WordBuilder class.
    Various representations as strings are provided, including the HTML used
    on the website.
    """

    def __init__(self, line, pattern='', custom_dict={}):
        """Initialize from original line."""
        self.line = line
        self.pattern = pattern
        self.custom_dict = custom_dict

    def __str__(self):
        """Create the informal string representation of the class."""
        return self.line

    def __repr__(self):
        """Create the formal string representation of the class."""
        return "LineBuilder('" + self.line + "')"

    def _clean_line(self):
        """Prepare a line for splitting on spaces."""
        clean = self.line
        for sep in "—-":
            clean = clean.replace(sep, " ")
        return clean

    @property
    def _word_list(self):
        """Create the list of WordBuilder instances."""
        word_list = []
        for word in self._clean_line().split():
            wb = WordBuilder(word, custom_dict=self.custom_dict)
            word_list.append(wb)
        return word_list

    @property
    def _rhyming_part(self):
        """Return the rhyming part of the line's last word."""
        return self._word_list[-1]._rhyming_part

    def _matched_words(self):
        """
        Match each word's syllables against the pattern.

        Private method in service of stressed_HTML().
        Returns a list of dictionaries:
            - word: WorldBuilder instance for the original word
            - pattern: slice of the line's stress pattern for that word
        """
        matched_words = []
        # Make a mutable copy of the pattern
        pattern = self.pattern[:]
        for word in self._word_list:
            number_stresses = len(word.stress_list)
            word.pattern = pattern[0:number_stresses]
            pattern = pattern[number_stresses:]
            matched_words.append(word)
        if pattern != []:
            for stress in pattern:
                matched_words.append(WordBuilder(word='_', pattern=stress))
        return matched_words
