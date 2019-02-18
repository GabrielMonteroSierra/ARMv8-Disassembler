
import sys
import os

""" TRACER """
trace = False

for i in range(len(sys.argv)):
    if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
        inputFileName = sys.argv[i + 1]
        print (inputFileName)
    elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
        outputFileName = sys.argv[i + 1]
        print (outputFileName)

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
memData = []
binMem = []
data = []
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
        global data

    def run(self):
        if trace: print("Run")
        self.readAndSaveInstuctionsAndData()
        self.parseInstuctions()
        self.parseData()
        self.printInstctionsAndData()

    def readAndSaveInstuctionsAndData(self):

        if trace: print("Read And Save Instructions And Data")

        i = 0
        infile = open(inputFileName,"r")
        m = 0
        line = infile.readline()

        """ Reading in Instructions DOES NOT INCLUDE BREAK """
        while line != breakbin:
            instruction.append(line.replace('\n', ''))
            opcode.append(int(instruction[i], base=2) >> 21)
            mem.append(str(96 + (4*m)))
            i += 1
            m += 1
            line = infile.readline()

        """ Saves BREAK in Instruction """
        instruction.append(line.replace('\n', ''))
        opcode.append(int(instruction[i], base=2) >> 21)
        mem.append(str(96 + (4 * m)))

        """ Reading in Data """
        i = 0
        offset = 1
        while True:
            line = infile.readline()
            if line == '':
                break
            binMem.append(line)
            binMem[i] = binMem[i].replace('\n', '')
            memData.append(str(int(mem[m]) + (4 * offset)))
            i += 1
            offset += 1

        infile.close()
        return

    def parseInstuctions(self):
        if trace: print ("Parse Instuctions")
        #DONE - ADD , SUB ,B , AND, ORR
        """TODO - ADDI , SUBI , LSL, LSR, EOR, LDUR, STUR, CBZ, CBNZ, MOVZ, MOVK , NOP"""

        for i in range(len(opcode)):

            if opcode[i] == 1112:
                opcodeStr.append("\tADD")
                arg1.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg2.append((int(instruction[i], base=2) & rmMask) >> 16)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))
                instrSpaced.append(instruction[i][:11] + " " + instruction[i][11:16]+ " " + instruction[i][16:22] + " "
                                   + instruction[i][22:27] + " " + instruction[i][27:32])


            elif opcode[i] == 1624:
                opcodeStr.append("\tSUB")
                arg1.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg2.append((int(instruction[i], base=2) & rmMask) >> 16)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))
                instrSpaced.append(instruction[i][:11] + " " + instruction[i][11:16] + " " + instruction[i][16:22] + " "
                                   + instruction[i][22:27] + " " + instruction[i][27:32])

            elif opcode[i] == 2038:
                opcodeStr.append("\tBREAK")
                arg1.append('')
                arg2.append('')
                arg3.append('')
                arg1Str.append("")
                arg2Str.append("")
                arg3Str.append("")
                instrSpaced.append(instruction[i][:8] + " " + instruction[i][8:11] + " " + instruction[i][11:16] + " "
                                   + instruction[i][16:21] + " " + instruction[i][21:26] + " " + instruction[i][26:32])
            elif opcode[i] == 1112:
                opcodeStr.append("\tAND")
                arg1.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg2.append((int(instruction[i], base=2) & rmMask) >> 16)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))
                instrSpaced.append(instruction[i][:11] + " " + instruction[i][11:16] + " " + instruction[i][16:22] + " "
                                   + instruction[i][22:27] + " " + instruction[i][27:32])

            elif opcode[i] == 1360:
                opcodeStr.append("\tORR")
                arg1.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg2.append((int(instruction[i], base=2) & rmMask) >> 16)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))
                instrSpaced.append(instruction[i][:11] + " " + instruction[i][11:16] + " " + instruction[i][16:22] + " "
                                   + instruction[i][22:27] + " " + instruction[i][27:32])

            else:
                opcodeStr.append("\tINVALID INSTRUCTION")
                arg1.append('')
                arg2.append('')
                arg3.append('')
                arg1Str.append("")
                arg2Str.append("")
                arg3Str.append("")
                instrSpaced.append(instruction[i])
        return



    def parseData(self):
        if trace: print("Parse Data")
        for i in range(len(binMem)):
            data.append(int(binMem[i], 2) - (1 << 32))

    def printInstctionsAndData(self):
        if trace: print ("Print Insructions and Data")
        outfile = open(outputFileName,"w")
        for i in range(len(instruction)):
            line = (instrSpaced[i] + "\t" + mem[i] + opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i] +"\n")
            outfile.write(line)
        for i in range(len(binMem)):
            line = (binMem[i] + "\t" + memData[i] + "\t" +str(data[i])+ "\n")
            outfile.write(line)
        outfile.close()

if __name__ == "__main__":
    main()

