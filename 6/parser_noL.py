"""
nand2tetris project 6, the Hack assembler.
stough F26

This is the Parser module specified in Ch. 6
without the ability to handle symbols.
"""

from enum import Enum


class InstructionType(Enum):
    A_INSTRUCTION = 1
    C_INSTRUCTION = 2
    L_INSTRUCTION = 3
    NO_TYPE = 4


class Parser(object): # this is the parser for the hack assembly language, without symbol handling
    def __init__(self, input_file):
        self.lines = []
        self.cur = -1
        self.inputfile = input_file
        self.preprocessFile()
        self.curtype: InstructionType = InstructionType.NO_TYPE
        self.curdest = None
        self.cursymbol = None
        self.curcomp = None
        self.curjump = None

    def hasMoreLines(self):
        # check if there is another instruction to read
        return self.cur + 1 < len(self.lines)

    def advance(self):
        # move to the next instruction and interpret it
        if self.hasMoreLines():
            self.cur += 1 # move to the next line in the list of lines
            self.interpretLine()

    def instructionType(self):
        return self.curtype

    def curLine(self):
        # index 0 is the first instruction
        assert 0 <= self.cur < len(self.lines), 'No current line to report' # ensure the current index is valid
        return str(self.lines[self.cur])

    def symbol(self):
        '''
        Returnes the symbol or decimal as a string: (xxx) or @xxx returns xxx
        '''
        assert self.curtype is InstructionType.A_INSTRUCTION or \
            self.curtype is InstructionType.L_INSTRUCTION, \
            f'symbol only for A or L type, not {self.lines[self.cur]}'
        return self.cursymbol

    def dest(self):
        '''
        Returns the destination part of a C-instruction as a string.
        ADM, 8 possibilities: None, M, D, DM, A, AM, AD, AMD
        '''
        assert self.curtype is InstructionType.C_INSTRUCTION, \
            f'dest only for C-type, not {self.lines[self.cur]}'
        return self.curdest

    def comp(self):
        '''
        Returns one of 28 posibilities for the computation part, to the right of the '='
        and to the left of the ';'. eg 'D=D+1;JLE' returns 'D+1'
        '''
        assert self.curtype is InstructionType.C_INSTRUCTION, \
            f'comp only for C-type, not {self.lines[self.cur]}'
        return self.curcomp

    def jump(self):
        '''
        Returns the jump part of a C-instruction as a string. 8 posibilities, whatever
        is to the right of the ';' in a C-instruction. eg 'D=D+1;JLE' returns 'JLE'
        '''
        assert self.curtype is InstructionType.C_INSTRUCTION, \
            f'jump only for C-type, not {self.lines[self.cur]}'
        return self.curjump

    def preprocessFile(self):
        '''
        Preprocess the input file, removing comments and whitespace, and storing
        the lines in self.lines.
        '''
        with open(self.inputfile, 'r', encoding='utf-8-sig') as infile:
            for line in infile:
                # remove comments and whitespace
                line = line.split('//', 1)[0]
                line = ''.join(line.split())

                if line:
                    self.lines.append(line)

    def interpretLine(self):
        '''
        Interpret the current line. That is, determine all the cursymbol,
        curdest, curcomp, and curjump values. Also set the curtype.
        '''
        line = str(self.lines[self.cur])

        # reset the fields so nothing carries over from the last instruction
        self.curcomp = None
        self.curdest = '000'
        self.curjump = '000'

        if line[0] == '@':
            self.curtype = InstructionType.A_INSTRUCTION
            self.cursymbol = line[1:]

        elif line[0] == '(':
            self.curtype = InstructionType.L_INSTRUCTION
            self.cursymbol = line[1:-1]  # strip the parens

        else:
            # the harder one here. Set the type to C, the symbol to None.
            self.curtype = InstructionType.C_INSTRUCTION
            self.cursymbol = None

            # a c-instruction is dest=comp;jump
            # take out the destination if there is one
            if '=' in line:
                self.curdest, line = line.split('=', 1)

            # take out the jump if there is one
            if ';' in line:
                line, self.curjump = line.split(';', 1)

            # whatever is left is the computation
            self.curcomp = line