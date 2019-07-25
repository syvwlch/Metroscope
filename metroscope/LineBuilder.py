"""The class that provides the representation for a line of verse."""

from metroscope import WordBuilder


class LineBuilder(object):
    """
    Prepare a given line of verse for analysis.

    Line is stored as a list of instances of the WordBuilder class.
    Various representations as strings are provided, including the HTML used
    on the website.
    """

    def __init__(
        self,
        line,
        pattern='',
        custom_dict={},
    ):
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
    def words(self):
        """
        Create the list of WordBuilder instances.

        Distributes the stress pattern of the line across the words, based on
        how many syllables they have. Any left over beats in the pattern get a
        dummy word representation with the text '_'.
        """
        words = []
        # Make a mutable copy of the pattern
        pattern = self.pattern[:]
        for word in self._clean_line().split():
            wb = WordBuilder(word, custom_dict=self.custom_dict)
            number_stresses = len(wb.stress_list)
            wb.pattern = pattern[0:number_stresses]
            pattern = pattern[number_stresses:]
            words.append(wb)
        if pattern != []:
            for stress in pattern:
                words.append(WordBuilder(word='_', pattern=stress))
        return words

    @property
    def rhyming_part(self):
        """Return the rhyming part of the line's last word."""
        if self.words == []:
            return None
        else:
            return self.words[-1].rhyming_part
