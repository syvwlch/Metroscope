"""The module that generates the HTML for a poem."""

from metroscope import LineBuilder
from string import ascii_uppercase


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
                lines.append(LineBuilder(line))
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
