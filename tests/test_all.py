import xai16.lexer
import xai16.assembler
import xai16.emulator
import xai16.render
        
source = '''
        B start

p:
        HALT

start:  MOV R2, #0xaaaa
        STR R2, p
        LDR R3, p
        STR R3, 0x5d
        HALT

'''

assembly, label_map, source_map = xai16.lexer.lex_block(source)

print(label_map)

#assert assembly == [['LDR', 'R3', '100']]
#assert label_map == {'start': 0}
#assert source_map == {0:3}

exe = xai16.assembler.assemble(assembly, label_map)

em = xai16.emulator.Emulator(exe)

print(xai16.render.registers_header())
while not em.halted:
    s = xai16.render.registers(em)
    print(s)
    em.step()
    
s = xai16.render.registers(em)
print(s)
