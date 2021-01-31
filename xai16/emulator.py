from xai16.constants import *

MEMORY_SIZE = 256
NUM_REGISTERS = 13

class Emulator():
    def __init__(self, memory, registers=None, pc=0, cmp=0, screen='', halted=False):
        self.memory = memory
        while len(self.memory) < MEMORY_SIZE: self.memory.append(0)
        self.registers = registers if registers else [0] * NUM_REGISTERS
        self.pc = pc
        self.cmp = cmp
        self.screen = screen
        self.halted = halted

    def copy(self):
        mem = self.memory[:]
        rrs = self.registers[:]
        return Emulator(mem, rrs, self.pc, self.cmp, self.screen, self.halted)

    def step(self):
        r = self.registers
        c0 = self.memory[self.pc + 0]
        op2 = self.memory[self.pc + 1]
        self.pc += 2
        opcode = (c0 >> 12) & 0b1111
        condition = (c0 >> 9) & 0b0111
        am = (c0 >> 8) & 0b1
        rn = (c0 >> 4) & 0b1111
        rd = (c0 >> 0) & 0b1111
        instruction = list(Instruction)[opcode]
        if am != AddressMode.Immediate: op2 = r[op2]

        if condition == Conditional.AL: pass
        elif condition == Conditional.EQ and not self.cmp == 0: return
        elif condition == Conditional.NE and not self.cmp != 0: return
        elif condition == Conditional.GT and not self.cmp > 0: return
        elif condition == Conditional.GE and not self.cmp >= 0: return
        elif condition == Conditional.LT and not self.cmp < 0: return
        elif condition == Conditional.LE and not self.cmp <= 0: return

        if instruction == Instruction.HALT:   self.halted = True
        elif instruction == Instruction.LDR:  r[rd] = self.memory[op2]
        elif instruction == Instruction.STR:  self.memory[op2] = r[rd]
        elif instruction == Instruction.ADD:  r[rd] = r[rn] + op2
        elif instruction == Instruction.SUB:  r[rd] = r[rn] - op2
        elif instruction == Instruction.MOV:  r[rd] = op2
        elif instruction == Instruction.CMP:  self.cmp = r[rn] - op2
        elif instruction == Instruction.B:    self.pc = op2
        elif instruction == Instruction.BL:   r[11], self.pc = self.pc, op2
        elif instruction == Instruction.AND:  r[rd] = r[rn]  & op2
        elif instruction == Instruction.ORR:  r[rd] = r[rn]  & op2
        elif instruction == Instruction.EOR:  r[rd] = r[rn]  ^ op2
        elif instruction == Instruction.MVN:  r[rd] =        ~ op2
        elif instruction == Instruction.LSL:  r[rd] = r[rn] << op2
        elif instruction == Instruction.LSR:  r[rd] = r[rn] >> op2
        else:
            raise Exception(f'unknown instruction {instruction}')
