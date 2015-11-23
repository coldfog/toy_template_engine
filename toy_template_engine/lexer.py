import collections
import re

__author__ = 'fengyuyao'

BLOCK_BEGIN = '{%'
BLOCK_END = '%}'
VAR_BEGIN = '{{'
VAR_END = '}}'

Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])


class Lexer(object):
    def __init__(self):

        # self.seps = {'BLOCK_BEGIN', 'BLOCK_END', 'VAR_BEGIN', 'VAR_END'}
        # define the rules
        self.rules = dict(raw_data=[
            ('BLOCK_BEGIN', BLOCK_BEGIN),
            ('BLOCK_END', BLOCK_END),
            ('VAR_BEGIN', VAR_BEGIN),
            ('VAR_END', VAR_END),
            ('DATA', r'.+?(?=(%s))|.+' % (
                '|'.join((BLOCK_BEGIN, VAR_BEGIN, BLOCK_END, VAR_END))
            )),
        ], statement=[
            ('FLOAT', r'\.\d+|\d+\.\d+'),
            ('INT', r'\d+'),
            ('STR', r'(\"[^\"]*\"|\'[^\']*\')'),
            ('OP', "(%s)" % '|'.join(
                (r'\+', r'-', r'\*\*', r'\*', '//',
                 '/', '%',  # math op
                 '\{', '\}', r'\[', r'\]', r'\(', r'\)',  # build-in obj op
                 r'\.',  # attribute op
                 r'==', r'>=', r'<=', r'!=', r'<', r'>',  # cmp op
                 r'and', 'or', 'not',  # logic op
                 r'in', 'is'  # other
                 )
            )),
            ('COMMA', r','),
            ('BOOL', r'(True|False)'),
            ('NAME', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('WHITE_SP', r'\s+'),
            ('NEWLINE', r'(\n|\r|\r\n)'),
        ])

        # compile to re pattern
        for Id, rule in self.rules.items():
            tok_regex = '|'.join('(?P<%s>%s)' % p for p in rule)
            self.rules[Id] = re.compile(tok_regex, re.DOTALL)

        self.match_stack = []

    def tokenize(self, source):
        line = 1

        pos = line_start = 0
        get_token = self.rules['raw_data'].match
        # mo = get_token(source)

        in_block = False
        block_end = len(source)
        while True:  # mo is not None:
            mo = get_token(source, pos)
            if mo is None:
                break

            typ = mo.lastgroup
            val = mo.group(typ)

            pos = mo.end()

            if in_block:
                # assert pos <= block_end, 'parse extra character'
                if pos == block_end:
                    get_token = self.rules['raw_data'].match
                    in_block = False

            if typ == 'WHITE_SP':
                continue
            if typ == 'NEWLINE':
                line += 1
                line_start = 0
                continue

            if typ in {'BLOCK_END', 'VAR_END'} or (typ == 'OP' and val in {'}', ']', ')'}):
                if len(self.match_stack) == 0 or self.match_stack[-1].value != val:  # seps not match
                    break
                self.match_stack.pop()

            if typ == 'DATA' and in_block:
                block_end = mo.end()
                # block_end_tok = Token(typ, val, line, mo.start() - line_start)  # mo
                get_token = self.rules['statement'].match
                pos = block_begin
                # mo = get_token(source, pos)
                continue

            yield Token(typ, val, line, mo.start() - line_start)

            if typ in {'BLOCK_BEGIN', 'VAR_BEGIN'}:
                if typ == 'BLOCK_BEGIN':
                    self.match_stack.append(Token(typ, BLOCK_END, line, mo.start() - line_start))
                elif typ == 'VAR_BEGIN':
                    self.match_stack.append(Token(typ, VAR_END, line, mo.start() - line_start))
                in_block = True
                block_begin = mo.end()
            elif typ == 'OP':
                if val in {'(', '[', '{'}:
                    if val == '(':
                        self.match_stack.append(Token(typ, ')', line, mo.start() - line_start))
                    elif val == '[':
                        self.match_stack.append(Token(typ, ']', line, mo.start() - line_start))
                    elif val == '{':
                        self.match_stack.append(Token(typ, '}', line, mo.start() - line_start))

            line += val.count('\n')
            _line_start = val.rfind('\n')
            if _line_start != -1:
                line_start = _line_start + pos

        if pos != len(source):
            raise RuntimeError('Unexpected character %r on line %d' % (source[pos], line))

        if len(self.match_stack) != 0:
            raise RuntimeError('need {value} to match on line {line} column {column}'.format(
                value=self.match_stack[-1].value,
                line=self.match_stack[-1].line,
                column=self.match_stack[-1].column))


if __name__ == '__main__':
    statements = '''
    # This is something for test, The value of name is {{name+1}}
    # I will list items in blew:
    {% for i in items %}a
        {% for j in [1,22,.3] %}
            This is the items {{i}}.
            This is the items- {{j}}.
        {% endfor %}
    {% endfor- %}
    '''
    lexer = Lexer()

    for token in lexer.tokenize(statements):
        print token  # .value, token.typ
