import xai16.lexer
import xai16.assembler
import xai16.emulator
import xai16.render

def run(source, loop=1000):
    lines = source.splitlines()
    assembly, label_map, source_map = xai16.lexer.lex(lines)
    print(label_map)
    exe = xai16.assembler.assemble(assembly, label_map)
    emu = xai16.emulator.Emulator(exe)
    i = 0
    while not emu.halted:
        print(xai16.render.registers(emu))

        ai = source_map.get(emu.pc)
        if ai is not None:
            print(lines[source_map[emu.pc]])
        i += 1
        if i >= loop:
            raise Exception('loop!')
        emu.step()
    return emu
