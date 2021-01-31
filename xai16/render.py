def render(emulator, source, source_map):
    row = lambda: [' '] * 80
    frame = [row() for _ in range(24)]

    def draw(x, y, s):
        for i, c in enumerate(s):
            frame[y][x + i] = c

    for n, b in enumerate(emulator.memory):
        cx = n % 8
        cy = n // 8
        fx = 1 + (cx * 9)
        fy = 7 + (cy)
        s = f'{b:08x}'
        #draw(fx, fy, s)

    for i, v in enumerate(emulator.registers):
        cx = i % 8
        cy = i // 8
        fx = 0 + (cx * 5)
        fy = 0 + (cy * 2)
        draw(fx, fy+0, f'R{i}')
        draw(fx, fy+1, f'{v:04x}')

    draw(35, 2, 'CMP')
    draw(35, 3, '{:04x}'.format(emulator.cmp))
    draw(2, 5, '>' + emulator.screen)

    lines = source.splitlines()
    for ii, line in enumerate(lines):
        mk = '>' if emulator.pc == ii else ' '
        if 7 + ii < 24:
            draw(2, 7 + ii, f'{mk} {ii} {line}')

    return "\n".join(''.join(row) for row in frame)


def registers(emulator):
    # PC   CMP  R0   R1   R2   R3   R4   R5   R6   R7   R8   R9   R10  R11  R12
    # .... .... .... .... .... .... .... .... .... .... .... .... .... .... ....
    values = [emulator.pc, emulator.cmp] + [emulator.registers[n] for n in range(13)]
    return ' '.join(f'{v:04x}' for v in values)

def registers_header():
    names = ['PC', 'CMP'] + [f'R{n}' for n in range(13)]
    return ' '.join(f'{n:4s}' for n in names)
