"""Experiments with scanning meter."""

import pronouncing as prn


def clean_word(word):
    """Prepare a word for CMU lookup."""
    clean_word = word.replace("è", "e").lower()
    for punct in ".,;!?":
        clean_word = clean_word.replace(punct, "")
    return clean_word


def stress_word(word):
    """Retrieve the stresses for the given word."""
    custom_dict = {"phidian": "20"}
    word = clean_word(word)
    try:
        word_stresses = custom_dict[word]
    except KeyError:
        try:
            word_stresses = prn.stresses_for_word(word)[0]
        except IndexError:
            word_stresses = ""
    return word_stresses


def stress_line(line, stress_pattern):
    """Mark stresses over vowels in a line of text."""
    say = ""
    clean_line = line.replace("-", " ")
    for word in clean_line.split():
        word_stresses = stress_word(word)
        for char in word:
            if char in "aeiouyAEIOUY" and len(word_stresses):
                say += stress_pattern[0]
                stress_pattern = stress_pattern[1:]
                word_stresses = word_stresses[1:]
            elif char in "è":
                say += stress_pattern[0]
                stress_pattern = stress_pattern[1:]
            else:
                say += " "
        say += " "
    return say


TESTTEXT = """
One morn before me were three figures seen,
With bowèd necks, and joinèd hands, side-faced;
And one behind the other stepped serene,
In placid sandals, and in white robes graced;
They passed, like figures on a marble urn,
When shifted round to see the other side;
They came again; as when the urn once more
Is shifted round, the first seen shades return;
And they were strange to me, as may betide
With vases, to one deep in Phidian lore."""

TESTMETER = 'x/x/x/x/x/'

for line in TESTTEXT.splitlines():
    print(stress_line(line, TESTMETER))
    print(line)
