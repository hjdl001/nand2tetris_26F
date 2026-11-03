'''
N2T VM Translator, Project 7, CodeWriter class
stough F26

Example processes in a comment at the bottom. Some of these
ops are going to lead to a lot of assembly instructions.

Notes:
    - Following the API specified in N2T Ch 7
'''

import os
from vm_parser import (CommandType,
                        arithmetic_all,
                        arithmetic_comp,
                        arithmetic_binary,
                        arithmetic_unary)

# Would be a good idea to put together some standard snippets of code that are used over and over again.
# I'm thinking:
# push_d, pop_d: either take D and push it to the stack, or pop the stack into D.
# deref_push, deref_pop: take a segment and index, compute the address, then push or pop to that address.
#                       this is one is for local, argument, this, that. Those are ones where you do addr
#                       arithmetic.
# direct push and pop, for pointer and temp
standard_pushd = '@SP\nA=M\nM=D\n@SP\nM=M+1\n' # done in class but there's a more efficient version.


class CodeWriter(object):
    '''
    I put a bunch of dictionaries here to simplify some processing.
    python has string-formatting capabilities, see my video. For example
    s = '@{}\nD=M\nA=M...{}...'
    s.format('LCL', index)
    '''

    '''
    comparison ops are harder. They involve making a computation on
    x and y, optimistically assuming true (M=-1), then skipping ahead 
    if it was true, or else setting the value to false and falling through.
    The skip ahead has to be unique in the code, so we must keep track. 
    I'll keep that in the init, since it changes versus these others that
    are read only.
    I made a comp_boiler kind of static string that could be used for any
    of the logic ops, which require executing a comparison in assembly, 
    really hard to think about
    s = 'some string {} but also {{}}'
    s.format('first') -> s is now 'some string first but also {}'
    s.format('second') -> s is now 'some string first but also second'
    '''

    def __init__(self, outfile=None):
        if outfile is None:
            outfile = './Garbage.asm'
            print(f'CodeWriter: default outfile {outfile}.')
        self._outfile = outfile
        with open(self._outfile, 'w') as f:
            f.write(f'// CodeWriter Hack assembly output file {outfile}\n\n')
        # You'll have to keep track of comparison counts for the logic ops lt, gt, eq
        self.comp_counts = {
            'lt': 0,
            'eq': 0,
            'gt': 0
        }
        self.static_count = 0
        self.static_name = self.extract_static_name(self._outfile)

    def writeArithmetic(self, command: str):
        '''
        Write asm for the arithmetic op. all of these ops require 
        one or two stack operands, perform an op, then push the result
        back on the stack. Could use the temp registers R13-15. 
        '''
        assert command in arithmetic_all, \
            f'CodeWriter writeArithmetic: unknown command {command}'
        if command in arithmetic_binary:
            # pop two elements off, do the math, push the result?
            # I used a function gettwo for part of this. Write all in asm.
            # with open(self._outfile, 'w') as f:
            #   f.write(somebigstringthatsolvesthisproblem) 
            pass
        elif command in arithmetic_unary:
            # pop just one element, do the unary op and push the result. Write that all in asm.
            pass
        else: # comparison command. by elimination, must be in arithmetic_comp
            # This is an even bigger string. 
            pass

    def writePushPop(self, command: CommandType, segment: str, index: int):
        '''
        Write asm for the push or pop command. So, compute segement+index addr, then 
        either push to sp and update sp, or copy *sp-1 and decrement sp.
        push:
        // compute segment offset
        @SEGMENT 
        '''
        assert command in [CommandType.C_PUSH, CommandType.C_POP], \
            f'CodeWriter writePushPop: unknown command {command}'
        # DO WORK!!
        # this is writing assembly that corresponds to 
        # push segment i, pop segment i. Using potentially those standard
        # strings you maybe defined above. But some segments are treated
        # differently than others, so that's harder. 
            
        
    def staticPushPop(self, command, index):
        '''
        The vm notes something like 'push static i' and needs to be a variable 
        of the @x form. 
        '''
        varname = f'{self.static_name}.{index}'
        # push at least: write to the file f'@{varname}\nD=M\n' + standard_pushd
        pass



    def gettwo(self):
        '''
        gettwo: pops the stack once, leaving D and M with y and x respectively,
        while sp points to (y or) the new stack top. This is the common first step for all binary ops.
        '''
        pass

    def getone(self):
        '''
        Like gettwo, leaving M with x but without decrementing the stack pointer. common first step
        for not/neg
        '''
        pass

    def extract_static_name(self, filename):
        # doing some file path algorithm to the get name without the extension...
        base, file = os.path.split(filename)
        name, ext = os.path.splitext(file)
        return name
        
    def close(self):
        # finish with an infinite loop.
        with open(self._outfile, 'a') as f:
            f.write('(END)\n@END\n0;JMP\n')

    def writeComment(self, comment):
        # Writes the comment into the file, for debugging.
        with open(self._outfile, 'a') as f:
            f.write(f'\n//{comment}\n')

























'''
The CodeWriter class translates individual VM instructions into 
Hack assembly code snippets. For example `push local 3' should 
get RAM[local + 3] and copy its value into location 'sp' and then 
update sp. So maybe
@LCL
D=M
@3
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

Given the limited ops that the Hack platform is capable of, 
`pop this 5` will either require looping (there is no A+5), or 
else maybe:
@5
D=A
@THIS
D=D+A
@R13
M=D   // record this+5
@SP   // get value at stack top
AM=M-1
D=M
@R13  // record that value at this+5
A=M
M=D
@SP
M=M-1 // finishing popping from stack

Probably going to be smart to write little microhelper functions. 
'''