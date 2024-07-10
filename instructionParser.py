import re

class InstructionParser:
    def __init__(self,src:str):
        # open the input file
        self._inputFile=open(src, 'r')
        self._currentInstruction=""

    # read next line
    # this method should be called only if hasMoreLines() is true
    def advance(self):
        while True:
            line=self._inputFile.readline()
            # When instruction is valid (not empty line or a comment set the current instruction and return)
            if bool(re.search(r"^([^\S]+)|(\/\/.+)$",line)) == False:
                # Set the new instruction
                self._currentInstruction=line.strip()
                return
            # return if the src file doesn't have more lines 
            elif self.hasMoreLines() == False:
                return
            

    def symbol(self):
        return self._currentInstruction.replace("@","")

    # checks if the file has more lines
    def hasMoreLines(self)->bool:
        # Get the current position
        currentPosition=self._inputFile.tell()
        hasMoreLines=False
        if self._inputFile.readline() != "":
            hasMoreLines=True
        # Reset the current position
        self._inputFile.seek(currentPosition)
        return hasMoreLines
    
    # Returns the current instruction type
    # @2 -> A instruction
    # D=A -> C instruction
    def instructionType(self) -> str:
        if self._currentInstruction[0] == "@":
            return "A_COMMAND"
        return "C_COMMAND"
    
    # Returns the instruction dest field
    def dest(self) -> str | None:
        splitted = self._currentInstruction.split('=')
        if len(splitted) == 2:
            return splitted[0]
        return None
    
    # Returns the instruction comp field
    def comp(self)-> str | None:
        eqSplit = self._currentInstruction.split('=')
        if len(eqSplit) == 2:
            return eqSplit[1]
        return self._currentInstruction.split(';')[0]
    
    # Returns the instruction jump field
    def jump(self)-> str | None:
        splitted = self._currentInstruction.split(';')
        
        if len(splitted) == 2:
            return splitted[1]
        return None


