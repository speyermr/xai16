import sys
import tty
import termios
import os

import xai16.render

RESET = "\033[0;0H"

class UI:
    def __init__(self, emu, source, source_map):
        self.h = []
        self.emu = emu
        self.source = source
        self.source_map = source_map

    def step(self):
        if self.emu.halted:
            return
        self.h.append(self.emu)
        self.emu = self.emu.copy()
        self.emu.step()

    def undo(self):
        if self.h:
            self.emu = self.h.pop()

    def show_source(self):
        lines = self.source.splitlines()
        addr = self.emu.pc
        pc_ln = self.source_map[addr]
        addr_map = dict((v,k) for k,v in self.source_map.items())
        for ln, line in enumerate(lines):
            mk = '->' if ln == pc_ln else '  '
            ad = addr_map.get(ln)
            if ad is not None:
                ad = f'{ad:03x}'
            else:
                ad = '   '
            print(mk, ad, line, end="\r\n")

    def show_registers(self):
        r = xai16.render.registers_header()
        print(r, end="\r\n")
        r = xai16.render.registers(self.emu)
        print(r, end="\r\n")

    def render(self):
        print(RESET, end='')
        self.show_registers()
        self.show_source()

    def loop(self):
        fd = sys.stdin.fileno()
        saved_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        buf = ''
        try:
            print("\033[?25l")
            self.render()
            while True:
                ch = sys.stdin.read(1).lower()
                buf += ch
                if buf.endswith("\x1b[c"):
                    self.step()
                    self.render()
                if buf.endswith("\x1b[d"):
                    self.undo()
                    self.render()
                if ch == 'q':
                    break
                if ch == 's':
                    self.show_source()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, saved_settings)
            print("\033[?25h")
