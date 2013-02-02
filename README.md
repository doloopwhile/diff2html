diff2html.py
============
Colorize script for unified diff

* diff2html.py
    * Script to translate output of diff -u to html
* html2browse.py
    * Script to browse html output on web browser

Usage
-----
### Browse git diff on web browser ###

    git diff | python diff2html.py | python html2browse.py

### Save output as file ###

    git diff | python diff2html.py -o gitdiff.html
