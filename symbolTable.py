# Adds symbol to the table
class SymbolTable:
    def __init__(self):
        # Predefined symbols equate to memory locations
        self._symbols \
            = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,
               'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7,
               'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15,
               'SCREEN':0x4000, 'KBD':0x6000}
    
    # Add a new entry to the symbol table
    def add_entry(self,symbol:str,address:int):
        self._symbols[symbol]=address

    # Check if symbol exists in the table
    def contains(self,symbol:str):
        return symbol in self._symbols
    
    # Returns the address associated with the symbol
    def get_address(self,symbol:str):
        return self._symbols[symbol]
