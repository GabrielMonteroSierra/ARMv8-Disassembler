
import sys
import os
""" TRACER """
trace = True

""" Lists """
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
breakbin = "11111110110111101111111111100111\n"

""" Masks """
rnMask = 0x3E0
rmMask = 0x1F0000
rdMask = 0x1F
shmtMask = 0xFC00
addrMask = 0x1FF000
addr2Mask = 0xFFFFE0
imsftMask = 0x600000
imdataMask = 0x1FFFE0

inputFileName = 'test3_bin.txt'



def main():
    if trace: print("Main")
    x = TestMe()
    x.run()

class TestMe:
    def __init__(self):
        if trace: print('Constuctor TestMe')
        global opcodeStr
        global arg1
        global arg2
        global arg3
        global arg1Str
        global arg2Str
        global arg3Str
        global mem
        global binMem
        global opcode
        global instruction
        global instrSpaced
        global breakbin
        global inputFileName
        global outputFileName
        global rnMask
        global rmMask
        global rdMask

    def run(self):
        if trace: print("Run")
        self.readAndSaveInstuctionsAndData()
        self.parseInstuctions()
        self.parseData()
        self.printInstctionsAndData()

    def readAndSaveInstuctionsAndData(self):
        # DONE

        if trace: print("Read And Save Instructions And Data")

        i = 0
        infile = open(inputFileName,"r")
        m =0
        line = infile.readline()

        """ Reading in Instructions DOES NOT INCLUDE BREAK """
        while line != breakbin:
            instruction.append(line.replace('\n', ''))
            opcode.append(int(instruction[i], base=2) >> 21)
            mem.append(94 + (4*m))
            i += 1
            m += 1
            line = infile.readline()

        """ Saves BREAK in Instruction """
        instruction.append(line.replace('\n', ''))
        opcode.append(int(instruction[i], base=2) >> 21)
        mem.append(94 + (4 * m))

        """ Reading in Data """
        i = 0
        while True:
            line = infile.readline()
            if line == '':
                break
            binMem.append(line)
            binMem[i] = binMem[i].replace('\n', '')
            mem.append(94 + (4 * m))
            i += 1
            m += 1
        return

    def parseInstuctions(self):
        if trace: print ("Parse Instuctions")

        for i in range(len(opcode)):

            if opcode[i] == 1112:
                opcodeStr.append("ADD")
                arg1.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg2.append((int(instruction[i], base=2) & rmMask) >> 16)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))

            elif opcode[i] == 1624:
                opcodeStr.append("SUB")
                arg1.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg2.append((int(instruction[i], base=2) & rmMask) >> 16)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))

            elif opcode[i] == 2038:
                opcodeStr.append("BREAK")
                arg1.append('')
                arg2.append('')
                arg3.append('')
                arg1Str.append("")
                arg2Str.append("")
                arg3Str.append("")

            else:
                opcodeStr.append("INVALID INSTRUCTION")
                arg1.append('')
                arg2.append('')
                arg3.append('')
                arg1Str.append("")
                arg2Str.append("")
                arg3Str.append("")
        return



    def parseData(self):
        if trace: print("Parse Data")

    def printInstctionsAndData(self):
        if trace: print ("Print Insructions and Data")




if __name__ == "__main__":
    main()






"""
while(instruction[0] != breakbin):

    # opcode.append((int(instruction[i], base=2) & mask) )

    inst = bin(10101010101)

  
    print(int(inst, base=2) & 7)
"""


"""
for i in range(len(sys.arg)):
    if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
        inputFileName = sys.argv[i + 1]
        print inputFileName
    elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
        outputFileName = sys.argv[i + 1]
        print outputFileName
"""