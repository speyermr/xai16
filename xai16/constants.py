from enum import Enum, IntEnum


class Device(IntEnum):
    UINT = 4
    CHAR = 7


class AddressMode(IntEnum):
    Direct = 0
    Immediate = 1


class Instruction(IntEnum):
    B    = 0x0
    BL   = 0x1
    LDR  = 0x2
    STR  = 0x3
    MOV  = 0x4
    MVN  = 0x5
    ADD  = 0x6
    SUB  = 0x7
    AND  = 0x8
    ORR  = 0x9
    EOR  = 0xa
    LSL  = 0xb
    LSR  = 0xc
    CMP  = 0xd
    HALT = 0xe
    #      0xf


class Conditional(IntEnum):
    AL = 0
    EQ = 1
    NE = 2
    GT = 3
    LT = 4
    GE = 5
    LE = 6


Conditional_Instructions = {}
for i in Instruction:
    Conditional_Instructions[i.name] = (i, Conditional.AL)
    for c in Conditional:
        k = i.name + c.name
        Conditional_Instructions[k] = (i, c)
