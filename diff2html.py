#!/usr/bin/env python3
from __future__ import print_function, unicode_literals
import io
import re
import fileinput
import sys
from argparse import ArgumentParser
from functools import partial

def quote_html(s):
    '''Quote html special chars and replace space with nbsp'''
    def repl_quote_html(m):
        tokens = []
        quote_dict = {
            ' ': '&nbsp;',
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            '"': '&quot;',
        }
        for c in m.group(0):
            tokens.append(quote_dict[c])
        return ''.join(tokens)
    return re.sub('[ &<>"]', repl_quote_html, s)


def print_html(print_function, lines, title, encoding):
    p = print_function
    q = quote_html
    p('<?DOCTYPE html?>')
    p('<html>')
    p('<head>')
    p('<meta http-equiv="Content-Type" content="text/html; charset={}">'
            .format(q(encoding)))
    if title is not None:
        p('<title>{}</title>'.format(q(title)))
    p('''
        <style>
            span.diffcommand { color: teal; }
            span.removed     { color: red; }
            span.inserted    { color: green; }
            span.linenumber  { color: purple; }
        </style>
    ''')
    p('</head>')

    for line in lines:
        if line.startswith('+++'):
            p(q(line))
        elif line.startswith('---'):
            p(q(line))
        elif line.startswith('+'):
            p('<span class="inserted">{}</span>'.format(q(line)))
        elif line.startswith('-'):
            p('<span class="removed">{}</span>'.format(q(line)))
        elif line.startswith('diff'):
            p('<span class="diffcommand">{}</span>'.format(q(line)))
        else:
            m = re.match(r'^@@.*?@@', line)
            if m:
                num = m.group(0)
                rest = line[len(num):]
                p('<span class="linenumber">{}</span>{}'
                            .format(q(num), q(rest)))
            else:
                p(q(line))
        p('<br />')
    p('</body>')
    p('</html>')


def main():
    parser = ArgumentParser()
    parser.add_argument('--output-file', '-o', action='store')
    parser.add_argument('--output-encoding', action='store',
            default=sys.getdefaultencoding())
    parser.add_argument('--title', action='store')
    parser.add_argument('files', nargs='*', action='store')

    args = parser.parse_args()
    encoding = args.output_encoding

    if args.output_file:
        output_file = io.open(args.output_file, 'w', encoding=encoding)
    else:
        output_file = sys.stdout

    try:
        print_html(partial(print, file=output_file),
            fileinput.input(args.files), title=args.title, encoding=encoding)
    finally:
        output_file.close()

if __name__ == '__main__':
    main()
