"""The module that generates the HTML for a poem."""

from metroscope import LineBuilder
from string import ascii_uppercase


CUSTOM_DICT = {
                "phidian": {"syllables": ["phi", "dian"],
                            "phones": "F IH1 D IY0 N"},
                "indolence": {"syllables": ["in", "do", "lence"],
                              "phones": "IH2 N D OW0 L EH1 N S"},
                "benumbed": {"syllables": ["be", "numbed"],
                             "phones": "B IY2 N AH1 M D"},
                "unhaunted": {"syllables": ["un", "haun", "ted"],
                              "phones": "AH0 N HH AO1 N T IH0 D"},
                "nothingness": {"syllables": ["no", "thing", "ness"],
                                "phones": "N AH1 TH IH0 NG N EH1 S",
                                "stresses": "101"},
                "embroidered": {"syllables": ["em", "broi", "dered"],
                                "phones": "IH0 M B R OY1 D ER0 D"},
                "besprinkled": {"syllables": ["be", "sprin", "kled"],
                                "phones": "B IY2 S P R IH1 NG K AH0 L D"},
                "o’er": {"syllables": ["o’er"],
                         "phones": "AO1 R"},
                "unmeek": {"syllables": ["un", "meek"],
                           "phones": "AH0 N M IY1 K"},
                "poesy": {"syllables": ["po", "e", "sy"],
                          "phones": "P OW1 AH0 Z AY1"},
                "forsooth": {"syllables": ["for", "sooth"],
                             "phones": "F AO2 R S UW1 TH"},
                "honeyed": {"syllables": ["ho", "neyed"],
                            "phones": "HH AH1 N IY0 D"},
                "casement": {"syllables": ["case", "ment"],
                             "phones": "K EY1 S M AH0 N T"},
                "leaved": {"syllables": ["leaved"],
                           "phones": "L IY1 V D"},
                "throstle": {"syllables": ["thro", "stle"],
                             "phones": "TH R AA1 S AH0 L"},
                "farewell": {"syllables": ["fare", "well"],
                             "phones": "F EH2 R W EH1 L"},
                "dieted": {"syllables": ["di", "e", "ted"],
                           "phones": "D AY1 AH0 T IH2 D"},
                "masque": {"syllables": ["masque"],
                           "phones": "M AE1 S K"},
                "fall’n": {"syllables": ["fall’n"],
                           "phones": "F AA1 L N"},
                "spright": {"syllables": ["spright"],
                            "phones": "S P R AY1 T"},
                "flowers": {"syllables": ["flowers"],
                            "phones": "F L AW1 ER Z"},
                "flower": {"syllables": ["flower"],
                           "phones": "F L AW1 ER"},
                "flowery": {"syllables": ["flowe", "ry"],
                            "phones": "F L AW1 ER IY0"},
                "deniest": {"syllables": ["de", "niest"],
                            "phones": "",
                            "stresses": "10"},
                "know’st": {"syllables": ["know’st"],
                            "phones": "",
                            "stresses": "1"},
                "triumph’st": {"syllables": ["tri", "umph’st"],
                               "phones": "",
                               "stresses": "10"},
                "say’st": {"syllables": ["say’st"],
                           "phones": "",
                           "stresses": "1"},
                "find’st": {"syllables": ["find’st"],
                            "phones": "",
                            "stresses": "1"},
                "yield’st": {"syllables": ["yield’st"],
                             "phones": "",
                             "stresses": "1"},
                "’tis": {"syllables": ["’tis"],
                         "phones": "",
                         "stresses": "1"},
                "purpled": {"syllables": ["pur", "pled"],
                            "phones": "",
                            "stresses": "10"},
                "maidenhead": {"syllables": ["mai", "den", "head"],
                               "phones": "",
                               "stresses": "101"},
                "orisons": {"syllables": ["o", "ri", "son"],
                            "phones": "",
                            "stresses": "102"},
                "mockeries": {"syllables": ["mocke", "ries"],
                              "phones": "",
                              "stresses": "10"},
                "pallor": {"syllables": ["pa", "llor"],
                           "phones": "",
                           "stresses": "10"},
              }


def scanned_poem(path, meter):
    """
    Create HTML with the scanned poem.

    Wrap the poem in a <div> tag, each stanza in a <p> tag,
    and end each line with a <br> tag.
    """
    lines = []
    with open(path, "r") as poem:
        for line in poem:
            if line != "\n":
                lines.append(LineBuilder(line, custom_dict=CUSTOM_DICT))
            else:
                lines.append(None)

    rhymes = {"None": "_"}
    result = "<table>\n<tr>\n"
    for line in lines:
        if line is None:
            result += "<td><br></td>\n</tr>\n<tr>"
            rhymes = {"None": "_"}
        else:
            result += "<td>"
            result += line.stressed_HTML(meter)
            result += "</td>\n<td>_"
            rp = str(line._rhyming_part)
            try:
                result += rhymes[rp] + "</td>\n"
            except KeyError:
                rhymes.update({rp: ascii_uppercase[len(rhymes)-1]})
                result += rhymes[rp] + " (" + rp + ")</td>\n"
            result += "</tr>\n<tr>"
    result += "</tr>\n</table>"
    return result


if __name__ == "__main__":
    print("This is a module, import it into a script to use.")
