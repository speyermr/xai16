from xai16.constants import *
from xai16.parser import parse

I = Instruction

def assemble(text):
    exe = []
    lines = text.splitlines()
    assembly, labels, sourcemap = parse(lines)
    for address, tokens in enumerate(assembly):
        head = tokens[0]
        if head in set(Instr):
            try:
                word = encode(tokens, labels)
            except Exception as ex:
                ii = sourcemap[address]
                line = lines[ii].strip()
                raise Exception(f'in instruction {ii} "{line}": {ex}')
        else:
            word = int(head, 0)
        exe.append(word)
    return exe, sourcemap

def encode(tokens, labels):
    instruction_token, *args = tokens

    instruction, cond, s_flag = parse_instruction(instruction_token)

    rd, rn = None, None
    am, op2 = 0, 0

    I = Instr
    # <address>
    if instruction in {I.B}:
        assert len(args) == 1, f'{instruction} <address>'
        op2 = to_address(labels, args[0])

    # Rd, <address>
    if instruction in {I.LDR, I.STR, I.INP, I.OUT}:
        assert len(args) == 2, f'{instruction} {Rd} {address}'
        rd, token = args
        op2 = to_address(labels, token)

    # Rd, op2
    if instruction in {I.MOV, I.MVN}:
        rd, token = args
        am, op2 = to_operand(token)

    # Rd, Rn, op2
    if instruction in {I.ADD, I.SUB, I.AND, I.ORR, I.EOR, I.LSL, I.LSR}:
        rd, rn, token = args
        am, op2 = to_operand(token)

    # Rn, op2
    if instruction in {I.CMP}:
        rn, token = args
        op2 = to_operand(token)

    # none
    if instruction in {I.HALT}:
        pass
    
    opcode = INSTRUCTIONS.index(instruction)
    rd = to_register(rd) if rd else 0
    rn = to_register(rn) if rn else 0
    flags = am

    #    27   23   19  16                 0
    # ..... .... .... ... ........ ........
    #     |    |    |   |                 |
    #    op   rn   rd  am          operand2
    return (opcode << 27 | rn << 23 | rd << 19 | flags << 16 | op2)

def to_address(labels, token):
    if token in labels:
        return labels[token]
    else:
        return int(token, 0)

def to_operand(token):
    # TODO
    return 0, 0
    
def to_register(name):
    if name[0] == 'R':
        return int(name[1:])
    elif name == 'PC':
        return 13
    else:
        raise Exception(f'unknown register "{name}"')

def parse_instruction(instruction):
    i = instruction

    if i[-1] == 'S':
        s_flag = True
        i = i[:-1]
    else:
        s_flag = False
    
    for v in Cond:
        if i[-2:] == v.name:
            i = i[:-2]
            cond = v
    else:
        cond = None

    for v in Instr:
        if v.name == i:
            return (v, cond, s_flag)

    raise Exception(f'unknown instruction {instruction} / {i}')
