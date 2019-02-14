instruction = []
opcode = []
opcodeStr = []
instrSpaced = []
arg1 = []
arg2 = []
arg3 = []
arg1Str = []
arg2Str = []
arg3Str = []
mem = []
binMem = []
breakbin = bin(11111111111111111111111111111111)
i = 0
# add instuction[0]

while(instruction[0] != breakbin):

#opcode.append((int(instruction[i], base=2) & mask) )

inst = bin(10101010101)

print(int(inst, base=2) & 7)