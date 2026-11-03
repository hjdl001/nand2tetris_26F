"""
nand2tetris project 6, the Hack assembler.
stough F26

This is the Code module specified in Ch. 6 
It seems like it will have a lot of predefined bitmappings, like 'JLE':'110'
for the jump part of a C-instruction, and 'D+1':'0011111' for the comp part.
That last one is a 7-bit mapping, the first bit is the a-bit, which is 0 for 
A-register and 1 for M-register, that one's big.
"""
# approach: predefine mappings for dest, comp, and jump parts of c-instructions.
# the mappings are based on the Hack assembly language specification, as found in chap 6

class Code(object):
    def __init__(self):
        self.destmap = {}
        self.compmap = {}
        self.jumpmap = {}
        self.symbmap = {}
        self.makeMaps()

    def dest(self, s):
        assert s in self.destmap, f'Error: no dest bits for {s}'
        return self.destmap[s]

    def comp(self, s):
        assert s in self.compmap, f'Error: no comp bits for {s}'
        return self.compmap[s]

    def jump(self, s):
        assert s in self.jumpmap, f'Error: no jump bits for {s}'
        return self.jumpmap[s]

    def makeMaps(self):
        # destmap goes from 'XXX=' to bits, this is 
        # all from that hack assembly language spec, the table in Ch 4 or Ch. 6 
        # add more
        self.destmap.update({
            # all from that hack assembly language spec, the table
            '000': '000',
            'M':   '001',
            'D':   '010',
            'DM':  '011',
            'MD':  '011',
            'A':   '100',
            'AM':  '101',
            'AD':  '110',
            'ADM': '111',
            'AMD': '111'
            # all done! 
        })
        
        self.jumpmap.update({
            # jump conditions
            '000': '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'
            # all done!
        })
        # compmap is complicated. maybe build the 18 corresponding to a=0 (A in the instruction), then the 10 more for when M replaces A (a=1)
        self.compmap.update({
            '0':   '0101010',
            '1':   '0111111',
            '-1':  '0111010',
            'D':   '0001100',
            'A':   '0110000',
            '!D':  '0001101',
            '!A':  '0110001',
            '-D':  '0001111',
            '-A':  '0110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'D+A': '0000010',
            'D-A': '0010011',
            'A-D': '0000111',
            'D&A': '0000000',
            'D|A': '0010101'
            # all done!
        })
        keys = list(self.compmap.keys()) # completed
        # A little diddy to add the M instead of A versions by
        # just setting a=1 instead of a=0
        for key in keys:
            if 'A' in key:
                self.compmap[key.replace('A','M')] = '1' + self.compmap[key][1:]


