import xai16.parser
import xai16.assembler
        
example = '''

start:
    LDR R3, 100

'''

assembly, labels, sourcemap = xai16.parser.parse_block(example)


assert assembly == [['LDR', 'R3', '100']]
assert labels == {'start': 0}
assert sourcemap == {0:3}

xai16.assembler.assemble(example)
