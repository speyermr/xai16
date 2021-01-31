import xai16

emu = xai16.run('''
        MOV R0, #4
        MOV R1, #3
        ADD R2, R0, R1
        HALT
        ''')

assert emu.halted
assert emu.registers[2] == 7
assert emu.pc == 8

import xai16.render
print(xai16.render.registers_header())

emu = xai16.run('''
        MOV R0, #4
        MOV R1, #0xa  // 10
        BL mul
done:   HALT
mul:    MOV R2, #0 // R0 * R1 = R2
mul_i:  CMP R1, #0
        BEQ [R11]
        ADD R2, R2, R0
        SUB R1, R1, #1
        MOV R2, #40
        B mul_i
        ''')

assert emu.registers[2] == 40 # 4 x 0xa == 40
