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
    table = SymbolTable() # create a symbol table for the assembler
    table.initsymT()

    print(f'{filename} has {len(parse.lines)} code lines.\n')

    #read the file the first time
    #do the first pass for the symbol table - hence l instructions
    real_lines = 0

    while parse.hasMoreLines():
            # Process the line, and append some binary string to outlines.
             # move to the next instruction
            parse.advance() # move to the next instruction

            if parse.instructionType() == InstructionType.L_INSTRUCTION:
                # we need to update our symbol table with our new symbol & find number 
                symbol = parse.symbol()
                table.addEntry(symbol, real_lines) # add the symbol and its corresponding line number    
            else: 
                real_lines = real_lines + 1 # adding one to the current real lines that's already included


    # second pass for the symbol table 
    # this includes the a or c instructions
    parse.reset() # reset the parser to the beginning of the file
    newvar = 16 # starting address for new variables

    outlines = []
    while parse.hasMoreLines():
        # Process the line, and append some binary string to outlines.
         # move to the next instruction
        parse.advance() # move to the next instruction

        if parse.instructionType() == InstructionType.A_INSTRUCTION:
            # turn the number after @ into 16-bit binary
            symbol = parse.symbol() 
            # check if it is numeric
            if symbol.isnumeric():
                address = int(symbol)
            else: 
                table.contains(symbol) # returning true or false 
                # need to return something since if its false, either returning a value or it needs to go to the symbol talbe 
                if table.contains(symbol):
                    address = table.getAddress(symbol)
                else: # must be a new symbol and now it needs to refer to some address in RAM; next RAM add available; starting from 16 
                   table.addEntry(symbol, newvar) # 
                   newvar += 1 # next value for a new symbol; since (16, 17,.....)
                   address = table.getAddress(symbol) # get the address of the new symbol - setting addy to be 16 

            outlines.append(format(address, '016b')) # turn add into binary if it is a-instruction

        elif parse.instructionType() == InstructionType.C_INSTRUCTION:
            # combine the prefix and the three parts from code_noL.py
            comp_bits = code.comp(parse.comp()) # comp part of c-instruction
            dest_bits = code.dest(parse.dest()) # dest part of c-instruction
            jump_bits = code.jump(parse.jump()) # jump part of c-instruction
            outlines.append('111' + comp_bits + dest_bits + jump_bits) # combine the parts into the final binary instruction

            # create the binary string for the C-instruction and append it to outlines 
            cinstruction = '111' + comp_bits + dest_bits + jump_bits
            outlines.append(cinstruction)

    # write the output file
    output_filename = os.path.splitext(filename)[0] + '.hack'
    with open(output_filename, 'w') as f:
        for line in outlines:
            f.write(line + '\n')        
            