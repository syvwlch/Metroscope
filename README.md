# Metroscope
Experiments in automated scanning of poetry and lyrics.

This summer I want to play with scansion, meter, and rhyme, rather than a specific text. I will use John Lennard's 'The Poetry Handbook' as a guide and source of example/exercises.

This started out as a rough little script, but it shows enough promise that I decided to make a repository and apply some discipline.

Metroscope.py is the module, which is imported into the actual analysis scripts.

Currently the only dependencies are:
Allison Parrish's excellent interface to CMU's dictionary of pronunciations

https://github.com/aparrish/pronouncingpy

and Christopher Henc's handy syllabification algorithm.

https://github.com/henchc/syllabipy

The public repository only has text that is in the public domain, of course, but you can put other text in /Texts/NonFreeTexts/ as well. The gitignore file has been set to ignore anything you place there.
