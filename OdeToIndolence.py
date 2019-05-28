"""Analysis of Keat's Ode to Indolence."""

from Metroscope import show_stress_line

POEM = """
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

IAMBIC_PENTAMETER = 'x/x/x/x/x/'

if __name__ == "__main__":
    for line in POEM.splitlines():
        print(show_stress_line(line, IAMBIC_PENTAMETER))
        print(line)
