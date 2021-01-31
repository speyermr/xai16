from xai16.constants import Instruction, AddressMode, Conditional

I = Instruction

def assemble(assembly, label_map):
    exe = []
    for tokens in assembly:
        cs = assemble_one(tokens, label_map)
        exe.extend(cs)
    return exe

def assemble_one(tokens, label_map):
    instruction_token, *args = tokens

    instruction, condition = parse_instruction(instruction_token)
    rd, rn, am, op2 = None, None, None, 0

    # <address>
    if instruction in {I.B}:
        assert len(args) == 1, f'{instruction} <address>'
        am, op2 = to_address(args[0], label_map)

    # Rd, <address>
    if instruction in {I.LDR, I.STR}: #, I.INP, I.OUT}:
        assert len(args) == 2, f'{instruction} <Rd> <address>'
        rd, token = args
        am, op2 = to_address(token, label_map)

    # Rd, op2
    if instruction in {I.MOV, I.MVN}:
        assert len(args) == 2, f'{instruction} <Rd> <op2>'
        rd, token = args
        am, op2 = to_operand(token)

    # Rd, Rn, op2
    if instruction in {I.ADD, I.SUB, I.AND, I.ORR, I.EOR, I.LSL, I.LSR}:
        assert len(args) == 3, f'{instruction} <Rd> <Rn> <op2>'
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
    am = am.value if am else 0

    # op__ c__A rn__ rd__  |  operand2
    # op__ c__A rn__ rd__  |  address
    v = 0
    v |= opcode << 12
    v |= condition.value << 9
    v |= am << 8
    v |= rn << 4
    v |= rd

    return (v, op2)

def to_address(token, label_map):
    if token in label_map:
        return AddressMode.Immediate, label_map[token]
    elif token[0:1] == '[':
        assert token[1] == 'R'
        assert token[-1] == ']'
        reg = int(token[2:-1])
        return AddressMode.Direct, reg
    else:
        address = int(token, 0)
        return AddressMode.Immediate, address

def to_operand(token):
    if token[0] == 'R':
        reg = int(token[1:])
        return AddressMode.Direct, reg
    elif token[0] == '#':
        val = int(token[1:], 0)
        return AddressMode.Immediate, val
    else:
        raise Exception(f'unparseable op2: {token}')

    
def to_register(name):
    if name[0] == 'R':
        return int(name[1:])
    else:
        raise Exception(f'unknown register "{name}"')

def parse_instruction(instruction):
    for candidate in Instruction:
        if instruction.startswith(candidate.name):
            i = candidate
            break
    else:
        raise Exception(f'unknown instruction {instruction}')

    l = len(i.name)
    conditional = instruction[l:]
    if conditional == '':
        return (i, Conditional.AL)
    else:
        for candidate in Conditional:
            if conditional == candidate.name:
                return (i, candidate)
        else:
            raise Exception(f'unknown conditional {conditional!r} / {instruction!r}')
