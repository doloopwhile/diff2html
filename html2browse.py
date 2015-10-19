#!/usr/bin/env python3
'''
Display html input on browser.

Known issue:
    This script does not delete temporary file.
'''
import sys
import tempfile
import fileinput
import webbrowser
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument('files', nargs='*', action='store')

    args = parser.parse_args()

    f = tempfile.NamedTemporaryFile('w', prefix='html2browse.',
            suffix='.html', delete=False)

    for line in fileinput.input(args.files):
        f.write(line)
    print(f.name)

    webbrowser.open(f.name)

if __name__ == '__main__':
    main()
