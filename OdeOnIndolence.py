"""Analysis of Keat's Ode on Indolence."""

from Metroscope import show_stress_line, uppercase_stress_line

POEM_PATH = "Texts/FreeTexts/OdeOnIndolence.txt"
POEM_METER = "x/x/x/x/x/"

if __name__ == "__main__":
    with open(POEM_PATH, "r") as poem:
        for line in poem:
            print(show_stress_line(line, POEM_METER))
            print(uppercase_stress_line(line, POEM_METER))
            print(line, end="")
