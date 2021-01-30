def parse_block(block):
    lines = block.splitlines()
    return parse(lines)


def parse(lines):
    # Our return values:
    assembly = []
    labels = {}
    sourcemap = {}

    # Some labels appear on the line before so we need to track this
    label = None
    for ii, line in enumerate(lines):
        tokens = tokenize(line)

        # Empty line
        if tokens == []:
            continue

        # The first token is a label if it ends in ':'
        if tokens[0][-1] == ':':
            label = tokens[0][:-1]
            tokens = tokens[1:]

        # Empty line (after parsing the label)
        if tokens == []:
            continue

        # Consume whatever label we have (either from this line, or the
        # previous one.)
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
        # Handle multiple spaces between tokens
        if token == '':
            continue

        # Ignore everything after "//", either as a token or at the start of a
        # token.
        if token[0:2] == '//':
            break

        # Strip suffixed commas
        if token[-1] == ',':
            token = token[:-1]

        r.append(token)
    return r
