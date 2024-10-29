class SymbolTable:
    """Keeps a correspondence between symbolic labels and numeric
    addresses."""

    def __init__(self):
        """Creates a new empty symbol table filled with predefined symbols."""

        # Predefined symbols equate to memory locations
        self._symbols = \
            {
                'SP':0,
                'LCL':1,
                'ARG':2,
                'THIS':3,
                'THAT':4,
                'R0':0,
                'R1':1,
                'R2':2,
                'R3':3,
                'R4':4,
                'R5':5,
                'R6':6,
                'R7':7,
                'R8':8,
                'R9':9,
                'R10':10,
                'R11':11,
                'R12':12,
                'R13':13,
                'R14':14,
                'R15':15,
                'SCREEN':0x4000,
                'KBD':0x6000
            }
    
    def add_entry(self,symbol:str,address:int):
        """Adds the pair (symbol,address) to the table."""
        self._symbols[symbol] = address

    def contains(self,symbol:str):
        """Does the symbol table contain the given symbol?"""
        return symbol in self._symbols
    
    def get_address(self,symbol:str):
        """Returns the address associated with the symbol."""
        return self._symbols[symbol]
