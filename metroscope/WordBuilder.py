"""The class that holds the representation of a word."""

from pronouncing import stresses, phones_for_word, rhyming_part
from nltk import SyllableTokenizer

SSP = SyllableTokenizer()


class WordBuilder(object):
    """
    Prepare a given word for analysis.

    Word is given as it is in the original, and the class provides a lowercase
    version ready for CMU lookup and syllable separation, as well as a list of
    syllable objects with various properties.
    """

    def __init__(self, word, pattern='', custom_dict={}):
        """Initialize from original word."""
        self.word = word
        self.pattern = pattern
        self.custom_dict = custom_dict

    def __str__(self):
        """Create the informal string representation of the class."""
        return self.word

    def __repr__(self):
        """Create the formal string representation of the class."""
        return "WordBuilder('" + self.word + "')"

    @property
    def _phones_list(self):
        """Return the list of phones of the original word."""
        word_phones = []
        try:
            word_phones.extend(self.custom_dict[self._clean_word]["phones"])
        except KeyError:
            pass
        word_phones.extend(phones_for_word(self._clean_word))
        if word_phones == []:
            return None
        else:
            return word_phones

    @property
    def _phones(self):
        """Return the current phones (as per index into phones list)."""
        if self._phones_list is None:
            return None
        return self._phones_list[0]

    @property
    def _raw_syllables(self):
        """Return the syllables of the original word."""
        try:
            word_syllables = self.custom_dict[self._clean_word]["syllables"]
        except KeyError:
            word_syllables = SSP.tokenize(self.word)
        return word_syllables

    @property
    def stress_list(self):
        """
        Return a string of the stresses for the given word.

        Consumers of this list make the following assumptions:
         - syllables with a "1" should be stressed by the meter
         - syllables with a "2" can be stressed or unstressed by the meter
         - syllables with a "0" should be unstressed by the meter
        """
        if self._phones is None:
            return ""
        word_stresses = stresses(self._phones)
        # Poets often signal syllables that would normally be silent this way.
        if "è" in self.word:
            word_stresses += "2"
        # Words of one syllable can usually be pronounced either way.
        if word_stresses in ("1", "0"):
            word_stresses = "2"
        return word_stresses

    @property
    def _stressed_syllables(self):
        """Combine the syllables and stresses of the original word."""
        word = self.word
        syllables = self._raw_syllables
        stresses = self.stress_list
        if stresses == "":
            return None
        result = []
        for syllable in syllables:
            if len(stresses) > 1:
                result.append([word[0:len(syllable)], stresses[0]])
                word = word[len(syllable):]
                stresses = stresses[1:]
            elif len(stresses) == 1:
                result.append([word, stresses[0]])
                stresses = ""
        return result

    @property
    def _clean_word(self):
        """Prepare a word for CMU lookup."""
        clean = self.word
        # First, force lowercase and strip punctuation
        clean = clean.lower()
        for punct in ".,;:!?—'\"":
            clean = clean.replace(punct, "")
        # Many poets mark added stress on a silent e with an è
        clean = clean.replace("è", "e")
        # Many poets mark elided vowels with a ’ at the end of a wor
        if clean[-2:] == "’s":
            clean = clean.replace("’s", "")
        clean = clean.replace("’d", "ed")
        return clean

    @property
    def syllables(self):
        """
        Build the syllable objects from the word.

        Returns a list of namedtuples:
            - Syllable.text: string of the original syllable,
            - Syllable.stress: Boolean for pattern stress,
            - Syllable.match: Boolean for match between pattern & pronunciation
        """
        from collections import namedtuple
        Syllable = namedtuple('Syllable', 'text stress match')
        stressed_syllables = self._stressed_syllables
        if stressed_syllables is None:
            return [Syllable(
                text=self.word,
                stress=None,
                match=False,
            )]
        result = []
        # Create a copy of pattern you can mutate safely
        pattern = self.pattern[:]
        for syllable, pronunciation_stress in stressed_syllables:
            if pattern:
                if pattern[0] == '1':
                    result.append(Syllable(
                        text=syllable,
                        stress=True,
                        match=pronunciation_stress != '0',
                    ))
                else:
                    result.append(Syllable(
                        text=syllable,
                        stress=False,
                        match=pronunciation_stress != '1',
                    ))
                pattern = pattern[1:]
            else:
                result.append(Syllable(
                    text=syllable,
                    stress=None,
                    match=False,
                    ))
        return result

    @property
    def rhyming_part(self):
        """Return the rhyming part of the original word."""
        phones = self._phones
        if phones is None:
            return None
        result = rhyming_part(phones)
        for stress in "012":
            result = result.replace(stress, "")
        return result
