"""Experiments with scanning meter."""

import pronouncing as prn


def clean_word(word):
    """Prepare a word for CMU lookup."""
    clean_word = word.replace("è", "e").lower()
    for punct in ".,;!?":
        clean_word = clean_word.replace(punct, "")
    return clean_word


def get_stress_word(word):
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


def clean_line(line):
    """Prepare a line of text for show_stress_line."""
    return line.replace("-", " ")


def show_stress_line(line, stress_pattern):
    """Mark stresses over vowels in a line of text."""
    say = ""
    VOWELS = "aeiouyAEIOUY"
    line = clean_line(line)
    for word in line.split():
        word_stresses = get_stress_word(word)
        for char in word:
            if char in VOWELS and len(word_stresses) and len(stress_pattern):
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


if __name__ == "__main__":
    print("This is a module, import it into a script to use.")
