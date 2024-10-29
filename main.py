import sys
import os
import re
from instructionParser import (InstructionParser)
from codeGenerator import (CodeGenerator)
from symbolTable import (SymbolTable)


def main():
    """The Hack assembler reads as input a text file named xxx.asm, containing a Hack assembly program, and produces as output a text file named xxx.hack, containing the translated Hack machine code."""
    src = sys.argv[1]
    # The generated file name will be xxx.hack from xxx.asm
    outName = src.replace(".asm",".hack")
    if os.path.exists(outName):
        os.remove(outName)
    out = open(outName,"a")
    instructionParser = InstructionParser(src)
    codeGenerator = CodeGenerator()
    symbolTable = SymbolTable()
    lineCount = 0

    # First pass
    # Collect the labels and fill the symbol table
    while instructionParser.hasMoreCommands():
        instructionParser.advance()
        if instructionParser.instructionType() == "L_INSTRUCTION":
            # Collect the label
            m = re.match(r"^\((.+)\)$",instructionParser._currentInstruction)
            label = m.group(1)
            if symbolTable.contains(label) == False:
                symbolTable.add_entry(label,lineCount)
        else:
            lineCount += 1

    instructionParser = InstructionParser(src)
    # Symbol addressing starts with 16
    address = 16
    
    # Second pass
    while instructionParser.hasMoreCommands():
        line = ""
        instructionParser.advance()
        if instructionParser.instructionType() == "L_INSTRUCTION":
            # Skip labels, the first run already collected it
            continue
        elif instructionParser.instructionType() == "C_INSTRUCTION":
            parsedComp = instructionParser.comp()
            # If the comp instruction has M a has to be 1 otherwise 0
            a = "1" if parsedComp.find("M") != -1 else "0"
            comp = codeGenerator.comp(parsedComp)

            parsedDest = instructionParser.dest()
            dest = "000"
            if parsedDest != None:
                dest = codeGenerator.dest(parsedDest)

            parsedJump = instructionParser.jump()
            jump = "000"
            if parsedJump != None:
                jump = codeGenerator.jump(parsedJump)

            line = "111" + a + comp + dest + jump
        else:
            # Generate the A instruction
            symbol = instructionParser.symbol()
            if re.match(r"^\d+$",symbol) == None:
                if symbolTable.contains(symbol) == False:
                    symbolTable.add_entry(symbol,address)
                    address += 1
                symbol = symbolTable.get_address(symbol)
            line = bin(int(symbol))[2:].zfill(16)
        out.write(line + "\n")

if __name__ == '__main__':
    main()
