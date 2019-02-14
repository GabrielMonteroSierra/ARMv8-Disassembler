
import sys
import os

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

### Masks
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
    print("Main")
    x = TestMe()
    x.run()

class TestMe:
    def __init__(self):
        print('Constuctor TestMe')

    def run(self):
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
        print("Run")
        self.readAndSaveInstuctionsAndData()
        self.parseInstuctions()

    def readAndSaveInstuctionsAndData(self):
        # DONE

        print("Entering Read And Save Instructions And Data")

        i = 0
        infile = open(inputFileName,"r")
        mem.append(94)
        m =1
        line = infile.readline()
        print(type(line))
        """Reading in Instructions DOES NOT INCLUDE BREAK"""
        while line != breakbin:
            instruction.append(line.replace('\n', ''))
            opcode.append(int(instruction[i], base=2) >> 21)
            mem.append(94 + (4*m))
            i = i + 1
            m = m + 1
            line = infile.readline()

        """Reading in Data"""
        i = 0
        while True:
            line = infile.readline()
            if line == '':
                break
            binMem.append(line)
            binMem[i] = binMem[i].replace('\n', '')
            i=i+1
            mem.append(94 + (4 * m))
            m = m + 1

    def parseInstuctions(self):
        print ("Entering Parse Instuctions")

        for i in range(len(opcode)):
            print(opcode[i])

    def parseData(self):
        print("Entering Parse Data")

    def printInstctions(self):
        print ("Entering Print Insructions and Data")




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