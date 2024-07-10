import sys
import os
import re
import instructionParser
import codeGenerator
import symbolTable

def main():
    # opens the input file
    src = sys.argv[1]
    # create the output file
    outName = src.replace(".asm",".hack")
    if os.path.exists(outName):
        os.remove(outName)
    out = open(outName,"a")
    parser = instructionParser.InstructionParser(src)
    generator = codeGenerator.CodeGenerator()
    symbol=symbolTable.SymbolTable()
    lineCount = -1

    # First pass
    # Collect the labels and fill the symbol table
    while parser.hasMoreLines():
        parser.advance()
        if parser.instructionType() == "L_INSTRUCTION":
            # Collect the label
            m = re.match(r"^\((.+)\)$",parser._currentInstruction)
            label = m.group(1)
            if symbol.contains(label) == False:
                # Add the label to the table with the line count
                symbol.add_entry(label,lineCount+1)
        else:
            lineCount += 1

    parser = instructionParser.InstructionParser(src)
    address = 16
    
    # Second pass
    while parser.hasMoreLines():
        line = ""
        parser.advance()
        # get the current instruction type
        if parser.instructionType() == "L_INSTRUCTION":
            continue
        elif parser.instructionType() == "C_INSTRUCTION":
            # Generate the c command
            comp = parser.comp()
            a = "1" if comp.find("M") != -1 else "0"
            comp=generator.comp(comp)
            dest = parser.dest()
            if dest == None:
                dest="000"
            else:
                dest=generator.dest(dest)
            jump = parser.jump()
            if jump == None:
                jump = "000"
            else:
                jump = generator.jump(jump)
            line = "111" + a + comp + dest + jump
        else:
            # Generate the a command
            sym = parser.symbol()
            if re.match(r"^\d+$",sym) == None:
                # Get the symbol address from the table
                # If it not exists, add to the table
                if symbol.contains(sym) == False:
                    symbol.add_entry(sym,address)
                    address += 1
                sym=symbol.get_address(sym)
            line = bin(int(sym))[2:].zfill(16)
        # Append the new line
        out.write(line + "\n")

if __name__ == '__main__':
    main()