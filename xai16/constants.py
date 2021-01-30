from enum import Enum


class Device(Enum):
    UINT = 4
    CHAR = 7


class AddressMode(Enum):
    DIR = 0b00
    IMM = 0b01
    IND = 0b10
    #     0b01


class Instruction(Enum):
    B    = 0x0
    LDR  = 0x1
    STR  = 0x2
    MOV  = 0x3
    MVN  = 0x4
    ADD  = 0x5
    SUB  = 0x6
    AND  = 0x7
    ORR  = 0x8
    EOR  = 0x9
    LSL  = 0xa
    LSR  = 0xb
    CMP  = 0xc
    HALT = 0xd
    #      0xe
    #      0xf


class Conditional(Enum):
    EQ = 0b001
    NE = 0b010
    GT = 0b011
    LT = 0b100
