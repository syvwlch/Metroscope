"""Experiments with scanning meter."""

from pronouncing import stresses_for_word
from syllabipy.sonoripy import SonoriPy


def clean_word(word):
    """Prepare a word for CMU lookup."""
    clean = word
    # Many poets mark added stress on a silent e with an è
    clean = clean.replace("è", "e")
    # Many poets mark elided vowels with a ’
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


def get_syllables_word(word):
    """Retrieve the syllables for a given word."""
    syllables = SonoriPy(word.lower())
    result = []
    for syllable in syllables:
        result.append(word[0:len(syllable)])
        word = word[len(syllable):]
    return result


def clean_line(line):
    """Prepare a line of text for show_stress_line."""
    clean = line
    for sep in "—-":
        clean = clean.replace(sep, " ")
    return clean


def stress_line(line, stress_pattern):
    """
    Mark up a line of verse based on the stress pattern provided.

    Return a tuple with:
    - the stresses aligned with the first vowel of each syllable, and
    - the line with the stressed syllables forced to uppercase.
    """
    VOWELS = "aeèiouyAEIOUY"
    aligned_stresses = ""
    stressed_line = ""
    line = clean_line(line)
    for word in line.split():
        number_stresses = len(get_stress_word(word))
        word_stresses = stress_pattern[0:number_stresses]
        stress_pattern = stress_pattern[number_stresses:]
        word_syllables = get_syllables_word(word)
        for syllable in word_syllables:
            if len(word_syllables) and len(word_stresses):
                syllable_stress = word_stresses[0]
                word_stresses = word_stresses[1:]
                if syllable_stress == "/":
                    stressed_line += "<strong>"
                    stressed_line += syllable
                    stressed_line += "</strong>"
                else:
                    stressed_line += syllable
                for char in syllable:
                    if char in VOWELS:
                        aligned_stresses += syllable_stress
                        syllable_stress = " "
                    else:
                        aligned_stresses += " "
            elif len(word_syllables) and not len(word_stresses):
                stressed_line += syllable
                for char in syllable:
                    aligned_stresses += " "
            else:
                stressed_line += " "
                aligned_stresses += " "
        stressed_line += " "
        aligned_stresses += " "
    return aligned_stresses, stressed_line


def scanned_poem(path, meter):
    """Create HTML div with the scanned poem."""
    result = "<div>\n<p>\n"
    with open(path, "r") as poem:
        for line in poem:
            if line == "\n":
                result += "</p>\n<p>"
            else:
                _, stressed_line = stress_line(line, meter)
                result += stressed_line
                result += "<br>\n"
    result += "</p>\n</div>"
    return result


if __name__ == "__main__":
    print("This is a module, import it into a script to use.")
