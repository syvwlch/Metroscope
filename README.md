# What is Metroscope about?

## Experiments in shareable scansions of poetry and lyrics.

This summer I wanted to play with scansion, meter, and rhyme, rather than a specific text. I will use John Lennard's ['The Poetry Handbook'](https://books.google.com/books/about/The_Poetry_Handbook.html?id=0eRtOqjNMxEC)'The Poetry Handbook' as a guide and source of example/exercises.

This started out at the command line with a rough little script, but since the goal is showing patterns in the text and sharing with friends without forcing them to install anything, I switched to HTML output and made a little website.

## Implementation details

This site is coded in Python, which is my go-to language for fooling around. I'm using this project as an opportunity to learn the Flask web framework and some of its major extensions.

What's left of the original command line script is the module that processes a line of verse based on the pronunciation of the words it contains.

The code lives on github at [/syvwlch/Metroscope](https://github.com/syvwlch/Metroscope), under the MIT license.

I'm also playing around with Travis CI for Continuous Integration and Heroku for deployment to staging and production. This site is currently hosted on Heroku.

The public repository only has text that is in the public domain, of course, but you can put other text in /Texts/NonFreeTexts/ as well. The gitignore file has been set to ignore anything you place there.

## Attribution and dependencies

Currently the main dependencies are on Flask and Bootstrap, plus:

1. Allison Parrish's excellent interface to CMU's dictionary of pronunciations: [pronouncingpy](https://github.com/aparrish/pronouncingpy)

2. and Christopher Henc's handy syllabification algorithm, which has been merged into NLTK: [sonority_sequencing](https://www.nltk.org/api/nltk.tokenize.html#nltk.tokenize.sonority_sequencing.SyllableTokenizer)

The lyre favicon design is by [Andrejs Kirma](https://thenounproject.com/andrejs/) from the Noun Project.

Check the pipfile for the full list of dependencies.

Note that I use PostgreSQL for the production DB which creates a dependency on psycopg2. When you run pipenv install on a new cloned repository, you may run into an issue with psycopg2 not installing. It gets built from source, and that requires that pg_config be on your path. Since I use [postgresapp.com](http://postgresapp.com/), that meant:
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin
