class CodeGenerator:
    _compTable= {
        "0":"101010",
        "1":"111111",
        "-1":"111010",
        "D":"001100",
        "A":"110000",
        "M":"110000",
        "!D":"001101",
        "!A":"110001",
        "!M":"110001",
        "-D":"001111",
        "-A":"110011",
        "-M":"110011",
        "D+1":"011111",
        "A+1":"110111",
        "M+1":"110111",
        "D-1":"001110",
        "A-1":"110010",
        "M-1":"110010",
        "D+A":"000010",
        "D+M":"000010",
        "D-A":"010011",
        "D-M":"010011",
        "A-D":"000111",
        "M-D":"000111",
        "D&A":"000000",
        "D&M":"000000",
        "D|A":"010101",
        "D|M":"010101"
    }

    # Returns the binary representation of the parsed dest field
    def dest(_,field:str) -> str:
        code=["0","0","0"]
        # if type(field) == "None":
        #     return code
        if field.find("A") != -1:
            code[0]="1"
        if field.find("D") != -1:
            code[1]="1"
        if field.find("M") != -1:
            code[2]="1"
        return "".join(code)
    
    # Returns the binary representation of the parsed jump field
    def jump(_,field:str) -> str:
        code=["0","0","0"]
        # if type(field) == "None":
        #     return code
        if field in ["JLT","JNE","JLE","JMP"]:
            code[0]="1"
        if field in ["JEQ","JGE","JLE","JMP"]:
            code[1]="1"
        if field in ["JGT","JGE","JNE","JMP"]:
            code[2]="1"
        return "".join(code)
    
    # Returns the binary representation of the parsed comp field
    def comp(self,field:str) -> str:
        return self._compTable[field]

