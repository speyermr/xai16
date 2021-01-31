import xai16.lexer
import xai16.parser
        
example = '''

start:
    LDR R3, 100

'''

assembly, label_map, source_map = xai16.parser.parse_block(example)


assert assembly == [['LDR', 'R3', '100']]
assert label_map == {'start': 0}
assert sourcemap == {0:3}

xai16.assembler.assemble(example)
