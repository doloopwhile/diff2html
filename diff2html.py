#!/usr/bin/env python3
import re
import fileinput
import sys
from argparse import ArgumentParser

def quote_html(s):
    def repl_quote_html(m):
        tokens = []
        for c in m.group(0):
            tokens.append({
                ' ': '&nbsp;',
                '<': '&lt;',
                '>': '&gt;',
                '&': '&amp;',
                '"': '&quot;',
            }[c])
        return ''.join(tokens)
    return re.sub('[ &<>"]', repl_quote_html, s)

def main():
    parser = ArgumentParser()
    parser.add_argument('--output-file', '-o', action='store')
    parser.add_argument('files', nargs='*', action='store')

    args = parser.parse_args()
    if args.output_file:
        output_file = open(args.output_file, 'w',
                encoding=sys.getdefaultencoding())
    else:
        output_file = sys.stdout
    def p(output_file=output_file):
        return lambda *a, **kw: print(file=output_file, *a, **kw)
    p = p()
    p('''
        <html>
        <head>
            <style>
            span.diffcommand { color: teal; }
            span.removed     { color: red; }
            span.inserted    { color: green; }
            span.linenumber  { color: purple; }
            </style>
        </head>
    ''')

    for line in fileinput.input(args.files):
        q = quote_html
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

if __name__ == '__main__':
    main()
