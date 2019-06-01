# Metroscope
Experiments in automated scanning of poetry and lyrics.

This summer I want to play with scansion, meter, and rhyme, rather than a specific text. I will use John Lennard's 'The Poetry Handbook' as a guide and source of example/exercises.

This started out as a rough little script, but it shows enough promise that I decided to make a repository and apply some discipline.

This started out at the command line but since a big part of this is showing patterns in the text, I switched to HTML output and made this into a little website.

Currently the main dependencies are on Flask and Bootstrap, plus:

1. Allison Parrish's excellent interface to CMU's dictionary of pronunciations:

https://github.com/aparrish/pronouncingpy

2. and Christopher Henc's handy syllabification algorithm:

https://github.com/henchc/syllabipy

The public repository only has text that is in the public domain, of course, but you can put other text in /Texts/NonFreeTexts/ as well. The gitignore file has been set to ignore anything you place there.
