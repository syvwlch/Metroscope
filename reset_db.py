"""Reset the database."""

from run import db, Meter, Poet, Poem


def reset_db():
    """Reset the database with the sample poems."""
    db.drop_all()
    db.create_all()

    db.session.add(Meter(name='Iambic Pentameter',
                         pattern='0101010101'))
    db.session.add(Meter(name='Cataleptic Anapestic Trimeter',
                         pattern='01001001'))

    db.session.add(Poet(name='John Keats'))
    db.session.add(Poet(name='Edward Lear'))
    db.session.add(Poet(name='John Donne'))
    db.session.add(Poet(name='Wilfred Owen'))

    db.session.commit()

    with open('Texts/FreeTexts/OdeOnIndolence.txt', "r") as poem:
        db.session.add(Poem(title='Ode on Indolence',
                            keyword='OdeOnIndolence',
                            raw_text=str(poem.read()),
                            poet_id=1,
                            meter_id=1))
    with open('Texts/FreeTexts/OldManWithBeard.txt', "r") as poem:
        db.session.add(Poem(title='There Was an Old Man with a Beard',
                            keyword='OldManWithBeard',
                            raw_text=str(poem.read()),
                            poet_id=2,
                            meter_id=2))
    with open('Texts/FreeTexts/Flea.txt', "r") as poem:
        db.session.add(Poem(title='The Flea',
                            keyword='Flea',
                            raw_text=str(poem.read()),
                            poet_id=3,
                            meter_id=1))
    with open('Texts/FreeTexts/AnthemForDoomedYouth.txt', "r") as poem:
        db.session.add(Poem(title='Anthem for Doomed Youth',
                            keyword='AnthemForDoomedYouth',
                            raw_text=str(poem.read()),
                            poet_id=4,
                            meter_id=1))

    db.session.commit()


if __name__ == "__main__":
    reset_db()
