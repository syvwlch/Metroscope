"""Experiments with scanning meter."""

from pronouncing import stresses_for_word
from syllabipy.sonoripy import SonoriPy


def clean_word(word):
    """Prepare a word for CMU lookup."""
    clean = word
    # Many poets mark added stress on a silent e with an è
    clean = clean.replace("è", "e")
    # Many poets mark elided vowels with a '
    clean = clean.replace("’s", "")
    clean = clean.replace("’d", "ed")
    clean = clean.replace("’r", "er")
    # Lastly, force lowercase and strip punctuation
    clean = clean.lower()
    for punct in ".,;:!?—":
        clean = clean.replace(punct, "")
    return clean


def get_stress_word(word):
    """Retrieve the stresses for the given word."""
    custom_dict = {
                    "phidian": "20",
                    "indolence": "200",
                    "benumbed": "02",
                    "unhaunted": "020",
                    "nothingness": "202",
                    "embroidered": "020",
                    "besprinkled": "020",
                    "o’er": "0",
                    "unmeek": "02",
                    "poesy": "202",
                    "forsooth": "02",
                    "honeyed": "20",
                    "casement": "20",
                    "leaved": "2",
                    "throstle": "20",
                    "’twas": "2",
                    "dieted": "202",
                    "masque": "2",
                    "spright": "2",
                  }
    cleaned_word = clean_word(word)
    try:
        word_stresses = custom_dict[cleaned_word]
    except KeyError:
        try:
            word_stresses = stresses_for_word(cleaned_word)[0]
        except IndexError:
            word_stresses = ""
    if "è" in word:
        word_stresses += "1"
    return word_stresses


def clean_line(line):
    """Prepare a line of text for show_stress_line."""
    clean = line
    for sep in "—-":
        clean = clean.replace(sep, " ")
    return clean


def show_stress_line(line, stress_pattern):
    """Mark stresses over vowels in a line of text."""
    say = ""
    VOWELS = "aeèiouyAEIOUY"
    line = clean_line(line)
    for word in line.split():
        word_stresses = get_stress_word(word)
        for char in word:
            if char in VOWELS and len(word_stresses) and len(stress_pattern):
                say += stress_pattern[0]
                stress_pattern = stress_pattern[1:]
                word_stresses = word_stresses[1:]
            else:
                say += " "
        say += " "
    return say


def uppercase_stress_line(line, stress_pattern):
    """Force stressed syllables to uppercase."""
    say = ""
    line = clean_line(line)
    for word in line.split():
        number_stresses = len(get_stress_word(word))
        word_stresses = stress_pattern[0:number_stresses]
        stress_pattern = stress_pattern[number_stresses:]
        word_syllables = SonoriPy(word.lower())
        for syllable in word_syllables:
            if len(word_syllables) and len(word_stresses):
                if word_stresses[0] == "/":
                    say += syllable.upper()
                else:
                    say += syllable
                word_stresses = word_stresses[1:]
            elif len(word_syllables) and not len(word_stresses):
                say += syllable
            else:
                say += " "
        say += " "
    return say


if __name__ == "__main__":
    print("This is a module, import it into a script to use.")
