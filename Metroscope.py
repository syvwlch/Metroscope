"""Experiments with scanning meter."""

import pronouncing as prn


def stress_line(line, stress_pattern):
    """Mark stresses over vowels in a line of text."""
    custom_dict = {"Phidian": "20"}
    say = ""
    stresses = stress_pattern
    clean_line = line.replace("-", " ")
    for word in clean_line.split():
        clean_word = word.replace("è", "e")
        for punct in ".,;!?":
            clean_word = clean_word.replace(punct, "")
        try:
            word_stresses = prn.stresses_for_word(clean_word)[0]
        except IndexError:
            try:
                word_stresses = custom_dict[clean_word]
            except IndexError:
                word_stresses = ""
        for char in word:
            if char in "aeiouyAEIOUY" and len(word_stresses):
                say += stresses[0]
                stresses = stresses[1:]
                word_stresses = word_stresses[1:]
            elif char in "è":
                say += stresses[0]
                stresses = stresses[1:]
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
