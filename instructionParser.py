import re

class InstructionParser:
    """Breaks each assembly command into its underlying components (fields and symbols)
    
    Encapsulates access to the input code.
    Reads an assembly language command, parses it, and provides convenient access to the command's components
    (fields and symbols).
    In addition, removes all white space and comments.
    """
    _invalidLinePattern = r"^[\s]*$|^[\s]*\/\/.*$"
    _labelPattern = r"^\(.+\)$"

    def __init__(self,src:str):
        self._inputFile = open(src, 'r')
        self._currentInstruction = ""

    
    def advance(self):
        """Reads the next command from the input and makes it the current command
    
        This method should be called only if hasMoreCommands() is true
        """

        while True:
            line = self._inputFile.readline()
            # When instruction is valid (not empty line or a comment) set the current instruction and return
            if re.match(self._invalidLinePattern,line) == None:
                self._currentInstruction = line.strip()
                return
            elif self.hasMoreCommands() == False:
                return

    def hasMoreCommands(self)->bool:
        """Checks if the file has more commands"""
        # Need to store the current position in order to reset it
        currentPosition = self._inputFile.tell()
        hasMoreCommands = False
        while True:
            line = self._inputFile.readline()
            # If the end of the file has been reached readline() returns ""
            if line == "":
                hasMoreCommands = False
                break
            if re.match(self._invalidLinePattern,line) == None:
                hasMoreCommands = True
                break
        # This command resets the current position
        self._inputFile.seek(currentPosition)   
        return hasMoreCommands
    
    def instructionType(self) -> str:
        """Returns the current instruction type"""
        labelMatch = re.match(self._labelPattern,self._currentInstruction)
        # Every command that starts with "@" -> @123
        if self._currentInstruction[0] == "@":
            return "A_INSTRUCTION"
        # Every instruction that's between parenthesis -> (LOOP)
        elif labelMatch:
            return "L_INSTRUCTION"
        # dest = comp; jump
        return "C_INSTRUCTION"
    
    def symbol(self):
        """Returns the symbol or decimal xxx of the current command @xxx or (xxx)
        
        Should be called only when commandType() is A_COMMAND or L_COMMAND
        """
        return self._currentInstruction.replace("@","").replace("(","").replace(")","")
    
    def dest(self) -> str | None:
        """Returns dest mnemonic in the current C-command
        
        Should be called only when commandType() is C_COMMAND
        """
        splitted = self._currentInstruction.split('=')
        if len(splitted) == 2:
            # dest = comp
            return splitted[0]
        return None
    
    def comp(self)-> str | None:
        """Returns the instruction comp field
        
        Should be called only when commandType() is C_COMMAND
        """
        eqSplit = self._currentInstruction.split('=')
        if len(eqSplit) == 2:
            # dest = comp
            return eqSplit[1]
        # comp; jmp
        return self._currentInstruction.split(';')[0]
    
    def jump(self)-> str | None:
        """Returns the instruction jump field
        
        Should be called only when commandType() is C_COMMAND
        """
        splitted = self._currentInstruction.split(';')
        if len(splitted) == 2:
            # comp; jmp
            return splitted[1]
        return None


