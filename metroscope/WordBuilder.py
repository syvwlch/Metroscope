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

    def __init__(self, word, custom_dict={}):
        """Initialize from original word."""
        self.word = word
        self.custom_dict = custom_dict
        self._is_in_custom_dict = self._clean_word in self.custom_dict

    def __str__(self):
        """Create the informal string representation of the class."""
        return self.word

    def __repr__(self):
        """Create the formal string representation of the class."""
        return "WordBuilder('" + self.word + "')"

    @property
    def _phones(self):
        """Return the phones of the original word."""
        if self._is_in_custom_dict:
            word_phones = self.custom_dict[self._clean_word]["phones"]
        else:
            word_phones = phones_for_word(self._clean_word)[0]
        return word_phones

    @property
    def syllables(self):
        """Return the syllables of the original word."""
        if self._is_in_custom_dict:
            word_syllables = self.custom_dict[self._clean_word]["syllables"]
        else:
            word_syllables = SSP.tokenize(self.word)
        return word_syllables

    @property
    def stress_list(self):
        """
        Return a list of the stresses for the given word.

        Consumers of this list make the following assumptions:
         - syllables with a "1" should be stressed by the meter
         - syllables with a "2" can be stressed or unstressed by the meter
         - syllables with a "0" should be unstressed by the meter
        """
        if self._is_in_custom_dict:
            word_stresses = self.custom_dict[self._clean_word]["stresses"]
        else:
            try:
                # word_stresses = stresses_for_word(str(self._clean_word))[0]
                word_stresses = stresses(self._phones)
            except IndexError:
                word_stresses = ""
        # Poets often signal syllables that would normally be silent this way.
        if "è" in self.word:
            word_stresses += "2"
        # Words of one syllable can usually be pronounced either way.
        if word_stresses in ("1", "0"):
            word_stresses = "2"
        return list(word_stresses)

    @property
    def _stressed_syllables(self):
        """Combine the syllables and stresses of the original word."""
        word = self.word
        syllables = self.syllables
        stresses = self.stress_list
        result = []
        for syllable in syllables:
            if len(stresses) > 1:
                result.append([word[0:len(syllable)], stresses.pop(0)])
                word = word[len(syllable):]
            elif len(stresses) == 1:
                result.append([word, stresses.pop(0)])
            else:
                pass
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

    def _tag_string(self, snippet, tag, style=""):
        """Wrap a text snippet with an html tag."""
        if style == "":
            opening_tag = "<" + tag + ">"
        else:
            opening_tag = "<" + tag + " style='" + style + "'>"
        closing_tag = "</" + tag + ">"
        return opening_tag + snippet + closing_tag

    def _matched_syllables(self, pattern):
        """
        Match the pronounced stresses against the given pattern.

        Private method in service of stressed_HTML().
        Returns a list of lists:
            - syllable string,
            - Boolean for pattern stress,
            - Boolean for match between pattern & pronunciation
        """
        result = []
        for syllable, pronunciation_stress in self._stressed_syllables:
            if pattern:
                if pattern.pop(0):
                    result.append([syllable,
                                   True,
                                   pronunciation_stress != '0'])
                else:
                    result.append([syllable,
                                   False,
                                   pronunciation_stress != '1'])
            else:
                result.append([syllable,
                               None,
                               False])
        return result

    @property
    def _rhyming_part(self):
        """Return the rhyming part of the original word."""
        if not self._is_in_custom_dict:
            phones = phones_for_word(self._clean_word)
        else:
            try:
                phones = self.custom_dict[self._clean_word]["phones"]
            except KeyError:
                phones = []
        if phones != []:
            return rhyming_part(phones[0])
        return None

    def stressed_HTML(self, pattern):
        """
        Mark up the original word based on the stress pattern provided.

        Return the word with the syllables wrapped with HTML tags and style
        attributes based on stress, provided meter, and whether they match.
        Finally, wrap a <span> tag around the entire word.
        """
        STYLES = {True: "color:black",
                  False: "color:red"}
        TAGS = {True: "strong",
                False: "span",
                None: "small"}

        result = ""
        for syllable, stress, match in self._matched_syllables(pattern):
            result += self._tag_string(syllable,
                                       TAGS[stress],
                                       STYLES[match])
        return self._tag_string(result, "span")
