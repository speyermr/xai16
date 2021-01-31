from xai16.constants import Instruction, AddressMode

I = Instruction

def parse(tokens, label_map):
    instruction_token, *arguments = *tokens

    instruction, condition, s_flag = parse_instruction(instruction_token)
    rd, rn, am, op2 = None, None, 0, 0

    # <address>
    if instruction in {I.B}:
        assert len(args) == 1, f'{instruction} <address>'
        am, op2 = to_address(args[0], label_map)

    # Rd, <address>
    if instruction in {I.LDR, I.STR, I.INP, I.OUT}:
        assert len(args) == 2, f'{instruction} {Rd} {address}'
        rd, token = args
        am, op2 = to_address(token, label_map)

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
        am, op2 = to_operand(token)

    # none
    if instruction in {I.HALT}:
        pass
    
    opcode = instruction.value
    rd = to_register(rd) if rd else 0
    rn = to_register(rn) if rn else 0

    # op__ c__s rn__ rd__  |  A?op eran d2__ ____
    # op__ c__s rn__ rd__  |  A?ad dres s___ ____
    c0 = (op << 12 | condition << 9 | s << 8 | rn << 4 | rd)
    c1 = (am << 15 | op2)
    return (c0, c1)

def to_address(token, label_map):
    if token in label_map:
        return AddressMode.Immediate, 0, label_map[token]
    elif token[0:1] == '[':
        assert token[1] == 'R'
        assert token[-1] == ']'
        reg = int(token[2:-1])
        return AddressMode.Direct, 0, reg
    else:
        address = int(token)
        return AddressMode.Immediate, 0, address

def to_operand(token):
    if token[0] == 'R':
        reg = int(token[1:])
        return AddressMode.Direct, 0, reg
    elif token[0] == '#':
        val = int(token[1:], 0)
        return AddressMode.Immediate, 0, val
    else:
        raise Exception(f'unparseable op2: {token}')

    
def to_register(name):
    if name[0] == 'R':
        return int(name[1:])
    else:
        raise Exception(f'unknown register "{name}"')

def parse_instruction(instruction):
    i = instruction
    c = None
    s = False

    if i[-1] == 'S':
        s = True
        i = i[:-1]

    for c0 in Cond:
        if i[-2:] == v.name:
            i = i[:-2]
            c = c0

    for i0 in Instr:
        if i0.name == i:
            return (i0, cond, s_flag)

    raise Exception(f'unknown instruction {instruction} / {i}')
