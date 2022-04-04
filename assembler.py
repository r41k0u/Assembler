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

for i in range(len(input_stream)):
    input_stream[i] = input_stream[i].split()

start_addr = hex(int(input_stream[0][-1], 16))

for i in range(1, len(input_stream)):
    input_stream[i].append(int(start_addr, 16) + 3*(i-1))
    if "RSUB" in input_stream[i]:
        break

