import sys
import os
import instructionParser
import codeGenerator

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
    # while the src has more lines advance
    while parser.hasMoreLines():
        line = ""
        parser.advance()
        # get the current instruction type
        if parser.instructionType() == "C_COMMAND":
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
            line = bin(int(parser.symbol()))[2:].zfill(16)
        # Append the new line
        out.write(line + "\n")

if __name__ == '__main__':
    main()