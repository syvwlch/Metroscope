# Metroscope
Experiments in shareable scansions of poetry and lyrics.

This summer I wanted to play with scansion, meter, and rhyme, rather than a specific text. I will use John Lennard's 'The Poetry Handbook' as a guide and source of example/exercises.

This started out at the command line with a rough little script, but since the goal is showing patterns in the text and sharing with friends without forcing them to install anything, I switched to HTML output and made a little website.

Currently the main dependencies are on Flask and Bootstrap, plus:

1. Allison Parrish's excellent interface to CMU's dictionary of pronunciations:

https://github.com/aparrish/pronouncingpy

2. and Christopher Henc's handy syllabification algorithm, which has been merged into NLTK:

https://www.nltk.org/api/nltk.tokenize.html#nltk.tokenize.sonority_sequencing.SyllableTokenizer

The public repository only has text that is in the public domain, of course, but you can put other text in /Texts/NonFreeTexts/ as well. The gitignore file has been set to ignore anything you place there.

The lyre favicon design is by Andrejs Kirma from the Noun Project.
