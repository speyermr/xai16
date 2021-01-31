import xai16

source = '''

        MOV R0, #4
        MOV R1, #0xa  // 10
        BL mul
done:   HALT


mul:    // R0 * R1 = R2
        MOV R2, #0

mul_i:  CMP R1, #0
        BEQ [R11]
        ADD R2, R2, R0
        SUB R1, R1, #1
        MOV R2, #40
        B mul_i
'''

exe, source_map = xai16.compile(source)

from xai16.ui import UI
from xai16.emulator import Emulator

emu = Emulator(exe)
ui = UI(emu, source, source_map)
ui.loop()
