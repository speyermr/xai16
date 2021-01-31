import xai16.lexer
import xai16.assembler
        
example = '''

start:
    LDR R3, 100

'''

assembly, label_map, source_map = xai16.lexer.lex_block(example)


assert assembly == [['LDR', 'R3', '100']]
assert label_map == {'start': 0}
assert source_map == {0:3}

exe = xai16.assembler.assemble(assembly, label_map)
print(exe)
