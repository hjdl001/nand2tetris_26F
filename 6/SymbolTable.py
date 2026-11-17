

class SymbolTable():
    def __init__(self) -> None:
        self.symT = {}

    def addEntry(self, symbol, address):
        self.symT[symbol] = address

    def contains(self, symbol):
        return symbol in self.symT

    def getAddress(self, symbol):
        assert symbol in self.symT, f'ERROR No symbol {symbol}'
        return self.symT[symbol]

    def initsymT(self): 
        self.symT.update({f'R{i}': i for i in range(16)})
        self.symT['SCREEN'] = 16384
        self.symT['KBD'] = 24576
        self.symT['SP'] = 0
        self.symT['LCL'] = 1
        self.symT['ARG'] = 2
        self.symT['THIS'] = 3
        self.symT['THAT'] = 4