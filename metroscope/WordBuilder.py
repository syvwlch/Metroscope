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

        clean_word = self.clean_word(word)

        valid_phones = []
        try:
            valid_phones.extend(self.custom_dict[clean_word]["phones"])
        except KeyError:
            pass
        valid_phones.extend(phones_for_word(clean_word))
        self._valid_phones = valid_phones

        try:
            self._phones = valid_phones[0]
        except IndexError:
            self._phones = ''

        valid_syllables = []
        try:
            valid_syllables.append(self.custom_dict[clean_word]["syllables"])
        except KeyError:
            pass
        valid_syllables.append(SSP.tokenize(self.word))
        self._valid_syllables = valid_syllables

        try:
            self._raw_syllables = valid_syllables[0]
        except IndexError:
            self._raw_syllables = word

    def __str__(self):
        """Create the informal string representation of the class."""
        return self.word

    def __repr__(self):
        """Create the formal string representation of the class."""
        return "WordBuilder('" + self.word + "')"

    @property
    def valid_phones(self):
        """Return the list of possible phones for the original word."""
        return self._valid_phones

    @property
    def phones(self):
        """Return the current phones being used for stress & rhyming_part."""
        return self._phones

    @phones.setter
    def phones(self, proposed_value):
        """Set the current phones to be used for stress & rhyming_part."""
        if proposed_value in self.valid_phones:
            self._phones = proposed_value
        else:
            raise ValueError('These phones are not valid for this word.')

    @property
    def stresses(self):
        """
        Return a string of the stresses for the given word.

        Consumers of this string make the following assumptions:
         - syllables with a "1" should be stressed by the meter
         - syllables with a "2" can be stressed or unstressed by the meter
         - syllables with a "0" should be unstressed by the meter
        """
        phones = self.phones
        word_stresses = stresses(phones)
        # Poets often signal syllables that would normally be silent this way.
        if "è" in self.word:
            word_stresses += "2"
        # Words of one syllable can usually be pronounced either way.
        if word_stresses in ("1", "0"):
            word_stresses = "2"
        return word_stresses

    @staticmethod
    def clean_word(word):
        """Prepare a word for CMU lookup."""
        # First, force lowercase and strip punctuation
        clean = word.lower()
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

        word = self.word
        syllables = self._raw_syllables
        stresses = self.stresses

        if stresses == "":
            return [Syllable(
                text=self.word,
                stress=None,
                match=False,
            )]

        stressed_syllables = []
        for syllable in syllables:
            if len(stresses) > 1:
                stressed_syllables.append([word[0:len(syllable)], stresses[0]])
                word = word[len(syllable):]
                stresses = stresses[1:]
            elif len(stresses) == 1:
                stressed_syllables.append([word, stresses[0]])
                stresses = ""

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
        phones = self.phones
        if phones == '':
            return None
        result = rhyming_part(phones)
        for stress in "012":
            result = result.replace(stress, "")
        return result
