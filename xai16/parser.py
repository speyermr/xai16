def parse_block(block):
    lines = block.splitlines()
    return parse(lines)


def parse(lines):
    assembly = []
    labels = {}
    sourcemap = {}
    label = None
    for ii, line in enumerate(lines):
        tokens = tokenize(line)
        if tokens == []:
            continue # Empty line


        # The first token is a label if it ends in ':'
        if tokens[0][-1] == ':':
            label = tokens[0][:-1]
            tokens = tokens[1:]
        if tokens == []:
            continue # Empty line (with label)
        address = len(assembly)
        if label:
            labels[label] = address
        assembly.append(tokens)
        sourcemap[address] = ii
        label = None
    return assembly, labels, sourcemap


def tokenize(line):
    r = []
    for token in line.split(' '):
        if token == '':
            continue
        if token[0:2] == '//':
            break
        if token[-1] == ',':
            token = token[:-1]
        r.append(token)
    return r
