import xai16.parser

assembly, labels, sourcemap = xai16.parser.parse_block('''

start:
    LDR R3, 100

''')


assert assembly == [['LDR', 'R3', '100']]
assert labels == {'start': 0}
assert sourcemap == {0:3}
