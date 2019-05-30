"""Analysis of Keat's Ode on Indolence."""

from Metroscope import stress_line

POEM_PATH = "Texts/FreeTexts/OdeOnIndolence.txt"
POEM_METER = "x/x/x/x/x/"

if __name__ == "__main__":
    with open(POEM_PATH, "r") as poem:
        for line in poem:
            aligned_stresses, stressed_line = stress_line(line, POEM_METER)
            print(aligned_stresses)
            print(stressed_line)
            # print(line, end="")
