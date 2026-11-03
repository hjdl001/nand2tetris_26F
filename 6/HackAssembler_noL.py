"""
Hack Assembler, without the symbol table. 
Stough, F26

The idea is to use the Parser to parse each relevant line,
and use the Code to translate binary.
"""

from parser_noL import Parser, InstructionType
from code_noL import Code
from SymbolTable import SymbolTable
import os
import sys

def assembleNoL(filename):
    parse = Parser(filename)
    code = Code()

    print(f'{filename} has {len(parse.lines)} code lines.\n')

    outlines = []
    while parse.hasMoreLines():
        # Process the line, and append some binary string to outlines.
         # move to the next instruction
        parse.advance() # move to the next instruction

        if parse.instructionType() == InstructionType.A_INSTRUCTION:
            # turn the number after @ into 16-bit binary
            address = int(parse.symbol())
            if not 0 <= address <= 32767: # check if the address is within the valid range for a 16-bit instruction
                raise ValueError('address must be between 0 and 32767')
            outlines.append(format(address, '016b'))

        elif parse.instructionType() == InstructionType.C_INSTRUCTION:
            # combine the prefix and the three parts from code_noL.py
            comp_bits = code.comp(parse.comp()) # comp part of c-instruction
            dest_bits = code.dest(parse.dest()) # dest part of c-instruction
            jump_bits = code.jump(parse.jump()) # jump part of c-instruction
            outlines.append('111' + comp_bits + dest_bits + jump_bits) # combine the parts into the final binary instruction

        else:
            raise ValueError('this version does not support labels')

    basename, ext = os.path.splitext(filename)
    outfilename = basename + '.hack'
    with open(outfilename, 'w') as outfile:
        for line in outlines:
            outfile.write(line + '\n')
    print(f'Wrote {len(outlines)} lines to {outfilename}.\n')
        
if __name__ == '__main__':
    assembleNoL(sys.argv[1])