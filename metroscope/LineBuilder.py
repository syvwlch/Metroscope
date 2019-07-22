"""The class that provides the representation for a line of verse."""

from metroscope import WordBuilder


class LineBuilder(object):
    """
    Prepare a given line of verse for analysis.

    Line is stored as a list of instances of the WordBuilder class.
    Various representations as strings are provided, including the HTML used
    on the website.
    """

    def __init__(self, line, custom_dict={}):
        """Initialize from original line."""
        self.line = line
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

    def _matched_words(self, stress_pattern):
        """
        Match each word's syllables against the given pattern.

        Private method in service of stressed_HTML().
        Returns a list of dictionaries:
            - word: WorldBuilder instance for the original word
            - stresses: slice of the line's stress pattern for that word
        """
        matched_words = []
        for word in self._word_list:
            number_stresses = len(word.stress_list)
            word_meter = stress_pattern[0:number_stresses]
            stress_pattern = stress_pattern[number_stresses:]
            # use the stress pattern directly for the word stresses
            matched_words.append({
                'word': word,
                'stresses': word_meter,
            })
        if stress_pattern != []:
            for stress in stress_pattern:
                matched_words.append({
                    'word': WordBuilder('_'),
                    'stresses': stress,
                })
        return matched_words

    def stressed_HTML(self, stress_pattern):
        """Mark up the line based on the stress pattern provided."""

        stressed_line = ""
        for word in self._matched_words(stress_pattern):
            # use the stress pattern directly for the word stresses
            stressed_line += word['word'].stressed_HTML(word['stresses']) + " "
        return stressed_line
