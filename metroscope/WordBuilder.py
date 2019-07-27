"""The class that holds the representation of a word."""

from pronouncing import stresses, phones_for_word, rhyming_part
from nltk import SyllableTokenizer


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


SSP = SyllableTokenizer()


def nltk_syllables(word):
    """Return syllables from nltk's SyllableTokenizer."""
    return [SSP.tokenize(word)]


def pronouncing_phones(word):
    """Return the phones list from the prounouncing package."""
    return phones_for_word(clean_word(word))


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
        self._valid_phones = self._custom_dict_before_source(
            key="phones",
            source=pronouncing_phones,
            default='',
        )
        self._phones = self.valid_phones[0]
        self._valid_syllables = self._custom_dict_before_source(
            key="syllables",
            source=nltk_syllables,
            default=self.word,
        )
        raw_syllables = []
        for syllable in self._valid_syllables[0]:
            raw_syllables.append(word[0:len(syllable)])
            word = word[len(syllable):]
        self._raw_syllables = raw_syllables

    def _custom_dict_before_source(self, key, source, default=''):
        """
        Try the custom dict first, then the source, then the default.

        Assumes that custom dict returns a single valid item and source returns
        a list of valid items.
        Use `source=lambda x: [source(x)]` if the source returns a single item.
        """
        valid_items = []

        try:
            valid_items.append(
                self.custom_dict[clean_word(self.word)][key]
            )
        except KeyError:
            pass

        valid_items.extend(source(self.word))

        if valid_items == []:
            valid_items = [default]

        return valid_items

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
        Syllable = namedtuple(
            'Syllable',
            'text stress match',
        )

        stresses = self.stresses
        pattern = self.pattern

        if stresses == "":
            return [Syllable(
                text=self.word,
                stress=None,
                match=False,
            )]

        voiced_syllables = []
        for index, syllable in enumerate(self._raw_syllables):
            try:
                stresses[index]
                voiced_syllables.append(syllable)
            except IndexError:
                voiced_syllables[-1] += syllable

        result = []
        for index, syllable in enumerate(voiced_syllables):
            try:
                stress = (pattern[index] == '1')
                if stresses[index] == '2':
                    match = True
                else:
                    match = pattern[index] == stresses[index]
            except IndexError:
                stress = None
                match = False
            text = syllable
            result.append(Syllable(
                text=text,
                stress=stress,
                match=match,
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
