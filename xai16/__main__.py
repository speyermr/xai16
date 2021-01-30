from xai16.assembler import assemble
from xai16.render import render
from time import sleep 
import xai16.emulator as emulator

import sys
path = sys.argv[1]

with open(path) as f:
    assembler = f.read()

code, sourcemap = assemble(assembler)
e = emulator.build(code)

RESET = "\033[0;0H"

while not e.halted:
    e.step()
    print(RESET + render(e, assembler, sourcemap))
    sleep(0.1)
