"""The module that generates the HTML for a poem."""

from metroscope import LineBuilder


CUSTOM_DICT = {
                "phidian": {"phones": ["F IH1 D IY0 N"]},
                "indolence": {"phones": ["IH2 N D OW0 L EH1 N S"]},
                "benumbed": {"syllables": ["be", "numbed"],
                             "phones": ["B IY2 N AH1 M D"]},
                "unhaunted": {"syllables": ["un", "haun", "ted"],
                              "phones": ["AH0 N HH AO1 N T IH0 D"]},
                "nothingness": {"syllables": ["no", "thing", "ness"],
                                "phones": ["N AH1 TH IH0 NG N EH1 S"]},
                "embroidered": {"syllables": ["em", "broi", "dered"],
                                "phones": ["IH0 M B R OY1 D ER0 D"]},
                "besprinkled": {"syllables": ["be", "sprin", "kled"],
                                "phones": ["B IY2 S P R IH1 NG K AH0 L D"]},
                "o’er": {"syllables": ["o’er"],
                         "phones": ["AO1 R"]},
                "ambition": {"syllables": ["am", "bi", "tion"]},
                "unmeek": {"phones": ["AH0 N M IY1 K"]},
                "poesy": {"syllables": ["po", "e", "sy"],
                          "phones": ["P OW1 AH0 Z AY1"]},
                "forsooth": {"phones": ["F AO2 R S UW1 TH"]},
                "honeyed": {"syllables": ["ho", "neyed"],
                            "phones": ["HH AH1 N IY0 D"]},
                "casement": {"syllables": ["case", "ment"],
                             "phones": ["K EY1 S M AH0 N T"]},
                "leaved": {"syllables": ["leaved"],
                           "phones": ["L IY1 V D"]},
                "throstle": {"syllables": ["thro", "stle"],
                             "phones": ["TH R AA1 S AH0 L"]},
                "farewell": {"syllables": ["fare", "well"]},
                "dieted": {"syllables": ["di", "e", "ted"],
                           "phones": ["D AY1 AH0 T IH2 D"]},
                "masque": {"phones": ["M AE1 S K"]},
                "fall’n": {"syllables": ["fall’n"],
                           "phones": ["F AA1 L N"]},
                "spright": {"phones": ["S P R AY1 T"]},
                "flowers": {"syllables": ["flowers"],
                            "phones": ["F L AW1 ER Z"]},
                "flower": {"syllables": ["flower"],
                           "phones": ["F L AW1 ER"]},
                "flowery": {"syllables": ["flowe", "ry"],
                            "phones": ["F L AW1 ER IY0"]},
                "into": {"syllables": ["in", "to"]},
                "deniest": {"phones": ["D IH0 N AY1 S T"]},
                "know’st": {"syllables": ["know’st"],
                            "phones": ["N OW1 S T"]},
                "triumph’st": {"syllables": ["tri", "umph’st"],
                               "phones": ["T R AY1 AH0 M F S T"]},
                "say’st": {"syllables": ["say’st"],
                           "phones": ["S EY1 S T"]},
                "find’st": {"syllables": ["find’st"],
                            "phones": ["F AY1 N D S T"]},
                "yield’st": {"syllables": ["yield’st"],
                             "phones": ["Y IY1 L D"]},
                "purpled": {"phones": ["P ER1 P AH0 L D"]},
                "maidenhead": {"phones": ["M EY1 D AH0 N HH EH1 D"]},
                "only": {"syllables": ["on", "ly"]},
                "stutt’ring": {"syllables": ["stutt’", "ring"],
                               "phones": ["S T AH1 T R IH0 NG"]},
                "orisons": {"syllables": ["o", "ri", "son"],
                            "phones": ["AO1 R AH0 S AH2 N Z"]},
                "mockeries": {"syllables": ["mocke", "ries"],
                              "phones": ["M AA1 K ER IY0 Z"]},
                "pallor": {"syllables": ["pa", "llor"],
                           "phones": ["P AE1 L ER0"]},
              }


def rhyme_designator(index):
    """
    Returns a string with an uppercase letter and a modifier.

    The modifier indicates how many times around the alphabet the index has
    gone, e.g. for index = 27, the string is A'.
    """
    from string import ascii_uppercase
    num = len(ascii_uppercase)
    letter = ascii_uppercase[index % num]
    modifier = index // num
    if modifier == 0:
        modifier = ""
    else:
        modifier = str(modifier)
    return letter + modifier


def scanned_poem(poem, meter_pattern):
    """
    Create a list of lines from the poem.

    Each line will include:
     1. the HTML showing the stress patter, and
     2. the rhyming part at the end of the line, and
     3. the designator for the rhyme in the rhyme scheme.
    """

    lines = []
    rhymes = {"None": "_"}
    for line in poem.split("\n"):
        if line != "":
            lb = LineBuilder(line, custom_dict=CUSTOM_DICT)
            rp = str(lb._rhyming_part)
            try:
                rd = rhymes[rp]
            except KeyError:
                rhymes.update({rp: rhyme_designator(len(rhymes)-1)})
                rd = rhymes[rp]

            lines.append({
                "HTML": lb.stressed_HTML(meter_pattern),
                "rhyming_part": rp,
                "rhyme_designator": rd,
            })
        else:
            rhymes = {"None": "_"}
            lines.append({
                "HTML": "<br>",
                "rhyming_part": "",
                "rhyme_designator": "",
            })
    return lines

    # rhymes = {"None": "_"}
    # result = "<table>\n<tr>\n"
    # for line in lines:
    #     if line is None:
    #         result += "<td><br></td>\n</tr>\n<tr>"
    #         rhymes = {"None": "_"}
    #     else:
    #         result += "<td>"
    #         result += line.stressed_HTML(meter_pattern)
    #         rp = str(line._rhyming_part)
    #         result += "</td>\n<td data-toggle='tooltip' title='"
    #         result += rp + "'>"
    #         try:
    #             result += rhymes[rp] + "</td>\n"
    #         except KeyError:
    #             index = len(rhymes)-1
    #             rhymes.update({rp: rhyme_designator(index)})
    #             result += rhymes[rp] + "</td>\n"
    #         result += "</tr>\n<tr>"
    # result += "</tr>\n</table>"
    # return result
