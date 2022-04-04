inp = open('input.sic')
input_stream = inp.readlines()
inp.close()

isa_tab = {
    "ADD" : 0x18,
    "AND" : 0x40,
    "COMP": 0x28,
    "DIV" : 0x24,
    "J"   : 0x3C,
    "JEQ" : 0x30,
    "JGT" : 0x34,
    "JLT" : 0x38,
    "JSUB": 0x48,
    "LDA" : 0x00,
    "LDCH": 0x50,
    "LDL" : 0x08,
    "LDX" : 0x04,
    "MUL" : 0x20,
    "OR"  : 0x44,
    "RD"  : 0xD8,
    "RSUB": 0x4C,
    "STA" : 0x0C,
    "STCH": 0x54,
    "STL" : 0x14,
    "STSW": 0xE8,
    "STX" : 0x10,
    "SUB" : 0x1C,
    "TD"  : 0xE0,
    "TIX" : 0x2C,
    "WD"  : 0xDC
}

sym_tab = {}

out_code = []

for i in range(len(input_stream)):
    input_stream[i] = input_stream[i].split()

start_addr = hex(int(input_stream[0][-1], 16))
ref_addr = start_addr

for i in range(1, len(input_stream)):
    input_stream[i].append(int(start_addr, 16) + 3*(i-1))

    if "RSUB" in input_stream[i]:
        end_addr = hex(input_stream[i][-1])
        start_addr = hex(0x10000 - i*3)
    elif "RESW" in input_stream[i]:
        start_addr = hex(int(start_addr, 16) - 3 + 3*int(input_stream[i][-2]))
    elif "RESB" in input_stream[i]:
        start_addr = hex(int(start_addr, 16) - 3 + int(input_stream[i][-2]))
    elif "BYTE" in input_stream[i]:
        start_addr = hex(int(start_addr, 16) - 2)

for i in range(len(input_stream)):
    if input_stream[i][0] not in isa_tab:
        sym_tab[input_stream[i][0]] = hex(int(input_stream[i][-1]))

prog_len = str(hex(int(end_addr, 16) - int(input_stream[0][-1], 16)))

header = "H" + input_stream[0][0] + (" "*(5-len(input_stream[0][0]))) + "0"*(6 - len(input_stream[0][-1])) + str(hex(int(input_stream[0][-1], 16)))[2:] + "0"*(8-len(prog_len)) + prog_len[2:]

out_code.append(header)

out_str = "T"
out_str += "0"*(8-len(str(ref_addr))) + str(ref_addr)[2:]

for i in range(len(input_stream)):
    if(int(input_stream[i][-1]) - int(ref_addr, 16)) > 9 :
        out_code.append(out_str)
        out_str = "T"
        ref_addr = hex(input_stream[i][-1])
        out_str += "0"*(8-len(str(ref_addr))) + str(ref_addr)[2:]
    if input_stream[i][0] == "START" or input_stream[i][1] == "START":
        pass
    if input_stream[i][0] in isa_tab:
        out_str+= "0"*(2 - len(str(hex(isa_tab[input_stream[i][0]]))[2:])) + str(hex(isa_tab[input_stream[i][0]]))[2:]
        if input_stream[i][0] == "RSUB":
                out_str+= "0000"
        if "X" in input_stream[i]:
            x = 32768
        else:
            x = 0
        if input_stream[i][1] in sym_tab:
            out_str += "0"*(8 - len(sym_tab[input_stream[i][1]])) + str(hex(int(sym_tab[input_stream[i][1]][2:], 16) + x))[2:]
        elif str(input_stream[i][1])[0] == '#':
            out_str += "0"*(8 - len(str(hex(int(input_stream[i][1][1:]))))) + str(hex(int(input_stream[i][1][1:])))[2:]
    elif input_stream[i][0] in sym_tab:
        if input_stream[i][1] in isa_tab:
            out_str+= "0"*(2 - len(str(hex(isa_tab[input_stream[i][1]]))[2:])) + str(hex(isa_tab[input_stream[i][1]]))[2:]
            if input_stream[i][1] == "RSUB":
                out_str+= "0000"
            if "X" in input_stream[i]:
                x = 32768
            else:
                x = 0
            if input_stream[i][2] in sym_tab:
                out_str += "0"*(8 - len(sym_tab[input_stream[i][2]])) + str(hex(int(sym_tab[input_stream[i][2]][2:], 16) + x))[2:]
            elif str(input_stream[i][1])[0] == '#':
                out_str += "0"*(8 - len(str(hex(int(input_stream[i][2][1:]))))) + str(hex(int(input_stream[i][2][1:])))[2:]
        elif input_stream[i][1] == "WORD":
            out_str += "0"*(10 - len(str(hex(int(input_stream[i][2]))))) + str(hex(int(input_stream[i][2])))[2:]

out_code.append(out_str)
            
out_code.append("E" + "0"*(6 - len(input_stream[0][-1])) + str(hex(int(input_stream[0][-1], 16)))[2:])

for i in range(len(out_code)):
    out_code[i] += "\n"

out = open("asm.obj", "w")
out.writelines(out_code)
out.close()
