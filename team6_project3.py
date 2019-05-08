import sys
import os


""" TRACER """
trace = False
"""
for i in range(len(sys.argv)):
    if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
        inputFileName = sys.argv[i + 1]
        print (inputFileName)
    elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
        outputFileName = sys.argv[i + 1] + "_dis.txt"
        outputFileNameSim = sys.argv[i + 1] + "_sim.txt"
        print (outputFileName)
outfileSim = open(outputFileNameSim, "w")
"""

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
#cycleAndInstruction = []
register = []
maxDataSize = 0
dataEntered = False

for i in range(32):
    register.append(0)


""" Masks """
rnMask = 0x3E0
rmMask = 0x1F0000
rdMask = 0x1F
shmtMask = 0xFC00
addrMask = 0x1FF000
addr2Mask = 0xFFFFE0
imsftMask = 0x600000
imdataMask = 0x1FFFE0
addr3Mask = 0x3FFFFFF
addr3MaskT =0x1FFFFFF
shiftMask = 0x600000
xORMask = 0xFFFFFFFF
cbzMask = 0xFFFFFF
addi_subiMask = 0x3FFC00

"""Pre/Post Buffer Queues"""
preIssue = list()
preMEM = list()
preALU = list()
postMEM = list()
postALU = list()




pc = 0

def twos_comp(val, bits):
    if(val &(1 << (bits -1))) != 0:
        val = val - (1 << bits)
    return val

def main():
    if trace: print("Main")
    x = Disassembler()
    x.run()
    y = Pipeline()
    y.run()


"""
CLASS: DISASSEMBLER
"""
class Disassembler:
    def __init__(self):
        if trace: print('Constuctor Disassembler')
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
        global xORMask



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
        line = line.rstrip()
        """ Reading in Instructions DOES NOT INCLUDE BREAK """
        while line != breakbin.rstrip():
            instruction.append(line)
            opcode.append(int(instruction[i], base=2) >> 21)
            mem.append(str(96 + (4*m)))
            i += 1
            m += 1
            line = infile.readline()
            line = line.rstrip()

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
            dataEntered = True

        infile.close()
        return

    def parseInstuctions(self):
        if trace: print ("Parse Instuctions")

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
            elif opcode[i] == 1104:
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

            elif opcode[i] == 1690:
                opcodeStr.append("\tLSR")
                arg1.append((int(instruction[i], base=2) & shmtMask) >> 10)
                arg2.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg2[i]))
                arg3Str.append(", #" + str(arg1[i]))
                instrSpaced.append(instruction[i][:11] + " " + instruction[i][11:16] + " " + instruction[i][16:22] + " "
                                    + instruction[i][22:27] + " " + instruction[i][27:32])

            elif opcode[i] == 1691:
                opcodeStr.append("\tLSL")
                arg1.append((int(instruction[i], base=2) & shmtMask) >> 10)
                arg2.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg2[i]))
                arg3Str.append(", #" + str(arg1[i]))
                instrSpaced.append(instruction[i][:11] + " " + instruction[i][11:16] + " " + instruction[i][16:22] + " "
                                    + instruction[i][22:27] + " " + instruction[i][27:32])

            elif opcode[i] == 1692:
                opcodeStr.append("\tASR")
                arg1.append((int(instruction[i], base=2) & shmtMask) >> 10)
                arg2.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg2[i]))
                arg3Str.append(", #" + str(arg1[i]))
                instrSpaced.append(instruction[i][:11] + " " + instruction[i][11:16] + " " + instruction[i][16:22] + " "
                                   + instruction[i][22:27] + " " + instruction[i][27:32])

            elif opcode[i] == 1872:
                opcodeStr.append("\tEOR")
                arg1.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg2.append((int(instruction[i], base=2) & rmMask) >> 16)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))
                instrSpaced.append(instruction[i][:11] + " " + instruction[i][11:16] + " " + instruction[i][16:22] + " "
                                    + instruction[i][22:27] + " " + instruction[i][27:32])

            elif opcode[i] == 0:
                opcodeStr.append("\tNOP")
                arg1Str.append("")
                arg2Str.append("")
                arg3Str.append("")
                arg1.append(99999)
                arg2.append(99999)
                arg3.append(99999)
                instrSpaced.append(instruction[i][:11] + " " + instruction[i][11:16] + " " + instruction[i][16:22] + " "
                                    + instruction[i][22:27] + " " + instruction[i][27:32])

            elif opcode[i] == 1160 or opcode[i] == 1161:
                opcodeStr.append("\tADDI")
                arg1.append((int(instruction[i], base=2) & addi_subiMask) >> 10)
                arg2.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg2[i]))
                arg3Str.append(", #" + str(arg1[i]) + "")
                instrSpaced.append(instruction[i][:10] + " " + instruction[i][10:22] + " " + instruction[i][22:27] + " "
                                   + instruction[i][27:32] )

            elif opcode[i] == 1672 or opcode[i] == 1673:
                opcodeStr.append("\tSUBI")
                arg1.append((int(instruction[i], base=2) & addi_subiMask) >> 10)
                arg2.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg2[i]))
                arg3Str.append(", #" + str(arg1[i]) +"")
                instrSpaced.append(instruction[i][:10] + " " + instruction[i][10:22] + " " + instruction[i][22:27] + " "
                                   + instruction[i][27:32] )

            elif 160 <= opcode[i] <= 191:
                opcodeStr.append("\tB")
                arg1.append('')
                arg2.append(twos_comp((int(instruction[i], base=2) & addr3Mask),26))
                arg3.append('')
                arg1Str.append("\t#"+str(arg2[i]))
                arg2Str.append('')
                arg3Str.append('')
                instrSpaced.append(instruction[i][:6] + " " + instruction[i][6:])

            elif 1440 <= opcode[i] <= 1447:
                opcodeStr.append("\tCBZ")
                arg1.append((int(instruction[i], base=2) & rdMask) >> 5)
                arg2.append(twos_comp(((int(instruction[i], base=2) & cbzMask) >> 5),19))
                arg3.append('')
                arg1Str.append("\tR" + str(arg1[i]))
                arg2Str.append(", #" + str(arg2[i]))
                arg3Str.append("")
                instrSpaced.append(instruction[i][:8] + " " + instruction[i][8:27] + " " + instruction[i][27:32] )

            elif 1448 <= opcode[i] <= 1455:
                opcodeStr.append("\tCBNZ")
                arg1.append((int(instruction[i], base=2) & rdMask) >> 5)
                arg2.append(twos_comp(((int(instruction[i], base=2) & cbzMask) >> 5), 19))
                arg3.append('')
                arg1Str.append("\tR" + str(arg1[i]))
                arg2Str.append(", #" + str(arg2[i]))
                arg3Str.append("")
                instrSpaced.append(instruction[i][:8] + " " + instruction[i][8:27] + " " + instruction[i][27:32] )

            elif 1684 <= opcode[i] <= 1687:
                opcodeStr.append("\tMOVZ")
                arg1.append((int(instruction[i], base=2) & shiftMask) >> 21)
                arg2.append((int(instruction[i], base=2) & imdataMask) >> 5)
                arg3.append((int(instruction[i], base=2) & rdMask))
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", " + str(arg2[i]))

                if arg1[i] == 0:
                    arg1[i] = 0
                    arg3Str.append(", LSL " + str(arg1[i]))
                elif arg1[i] == 1:
                    arg1[i] = 16
                    arg3Str.append(", LSL " + str(arg1[i]))
                elif arg1[i] == 2:
                    arg1[i] = 32
                    arg3Str.append(", LSL " + str(arg1[i]))
                elif arg1[i] == 3:
                    arg1[i] = 48
                    arg3Str.append(", LSL " + str(arg1[i]))

                instrSpaced.append(instruction[i][:9] + " " + instruction[i][9:11] + " " + instruction[i][11:27] + " "
                                   + instruction[i][27:32] )

            elif 1940 <= opcode[i] <= 1943:
                opcodeStr.append("\tMOVK")
                arg1.append((int(instruction[i], base=2) & shiftMask) >> 21)
                arg2.append((int(instruction[i], base=2) & imdataMask) >> 5)
                arg3.append((int(instruction[i], base=2) & rdMask))
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", " + str(arg2[i]))

                if arg1[i] == 0:
                    arg1[i] = 0
                    arg3Str.append(", LSL " + str(arg1[i]))
                elif arg1[i] == 1:
                    arg1[i] = 16
                    arg3Str.append(", LSL " + str(arg1[i]))
                elif arg1[i] == 2:
                    arg1[i] = 32
                    arg3Str.append(", LSL " + str(arg1[i]))
                elif arg1[i] == 3:
                    arg1[i] = 48
                    arg3Str.append(", LSL " + str(arg1[i]))

                instrSpaced.append(instruction[i][:9] + " " + instruction[i][9:11] + " " + instruction[i][11:27] + " "
                                   + instruction[i][27:32] )


            elif opcode[i] == 1984:
                opcodeStr.append("\tSTUR")
                arg1.append((int(instruction[i], base=2) & addrMask) >> 12)
                arg2.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", [R" + str(arg2[i]))
                arg3Str.append(", #" + str(arg1[i]) + "]")
                instrSpaced.append(instruction[i][:11] + " " + instruction[i][11:20] + " " + instruction[i][20:22] + " "
                                   + instruction[i][22:27] + " " + instruction[i][27:32])


            elif opcode[i] == 1986:
                opcodeStr.append("\tLDUR")
                arg1.append((int(instruction[i], base=2) & addrMask) >> 12)
                arg2.append((int(instruction[i], base=2) & rnMask) >> 5)
                arg3.append((int(instruction[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", [R" + str(arg2[i]))
                arg3Str.append(", #" + str(arg1[i]) + "]")
                instrSpaced.append(instruction[i][:11] + " " + instruction[i][11:20] + " " + instruction[i][20:22] + " "
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
            data.append(twos_comp(int(binMem[i], 2), 32))

    def printInstctionsAndData(self):
        if trace: print ("Print Insructions and Data")
        outfile = open(outputFileName,"w")
        for i in range(len(instruction)):
            line = (instrSpaced[i] + "\t" + mem[i] + opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i] + "\n")
            outfile.write(line)
        for i in range(len(binMem)):
            line = (binMem[i] + "\t" + memData[i] + "\t" +str(data[i]) + "\n")
            outfile.write(line)
        outfile.close()



"""
CLASS = SIMULATOR
"""
"""
class Simulator:
    def __init__(self):
        if trace: print('Constuctor Simulator')
        global maxDataSize
        global printDataFlag
        global outfileSim

    def runSim(self):
        cycle = 1
        pc = 0
        branchFlag = False
        while instruction[pc] != breakbin.rstrip():

            if opcode[pc] == 1112:  # ADD
                register[arg3[pc]] = register[arg1[pc]] + register[arg2[pc]]

            elif opcode[pc] == 1160 or opcode[pc] == 1161:  # ADDI
                register[arg3[pc]] = register[arg2[pc]] + arg1[pc]


            elif opcode[pc] == 1104:  # AND
                register[arg3[pc]] = register[arg1[pc]] & register[arg2[pc]]

            elif opcode[pc] == 1691:  # LSL
                register[arg3[pc]] = register[arg2[pc]] << arg1[pc]

            elif opcode[pc] == 1690:  # LSR
                if register[arg2[pc]] < 0:
                    register[arg3[pc]] = (register[arg2[pc]] * -1) >> arg1[pc]
                else:
                    register[arg3[pc]] = (register[arg2[pc]] >> arg1[pc])

            elif opcode[pc] == 1692: #ASR
                register[arg3[pc]] = (register[arg2[pc]] >> arg1[pc])

            elif opcode[pc] == 1624:  # SUB
                register[arg3[pc]] = register[arg1[pc]] - register[arg2[pc]]

            elif opcode[pc] == 1672 or opcode[pc] == 1673:  # SUBI
                register[arg3[pc]] = register[arg2[pc]] - arg1[pc]

            elif 160 <= opcode[pc] <= 191: #B
                self.printData(cycle, pc)
                pc = pc + arg2[pc]
                branchFlag = True

            elif opcode[pc] == 1984:  # STUR
                # if the size of the data is to small it will grow
                if dataEntered:
                    while int(memData[len(memData) - 1],base=10) < register[arg2[pc]] + arg1[pc] * 4:
                        data.append(0)
                        last = int(memData[len(memData) - 1], base=10)
                        memData.append(str(last + 4))
                else:
                    data.append(0)
                    last = int(mem[len(mem) - 1], base=10)
                    memData.append(str(last + 4))
                    while int(memData[len(memData) - 1],base=10) < register[arg2[pc]] + arg1[pc] * 4:
                        data.append(0)
                        last = int(memData[len(memData) - 1], base=10)
                        memData.append(str(last + 4))

                index = 0
                for k in range (len(memData)):
                    if int(memData[k], base=10) == register[arg2[pc]] + arg1[pc] * 4:
                        index = k
                data[index] = str(register[arg3[pc]])

            elif opcode[pc] == 1986:  # LDUR
                index = 0
                for k in range(len(memData)):
                    if int(memData[k], base=10) == register[arg2[pc]] + arg1[pc] * 4:
                        index = k
                register[arg3[pc]] = data[index]

            elif 1440 <= opcode[pc] <= 1447:  # CBZ
                if register[arg1[pc]] == 0:
                    self.printData(cycle, pc)
                    pc = pc + arg2[pc]
                    branchFlag = True # if it is equal it zero

            elif 1448 <= opcode[pc] <= 1455:  # CBNZ
                if register[arg1[pc]] != 0:
                    self.printData(cycle, pc)
                    pc = pc + arg2[pc]
                    branchFlag = True # if  its not equal to zero

            elif 1684 <= opcode[pc] <= 1687:  # MOVZ
                register[arg3[pc]] = int(arg2[pc] * 2 ** arg1[pc])

            elif 1940 <= opcode[pc] <= 1943:  # MOVK
                register[arg3[pc]] = int(register[arg3[pc]] + arg2[pc] * 2 ** arg1[pc])

            elif opcode[pc] == 1360:  # ORR
                register[arg3[pc]] = register[arg2[pc]] | register[arg1[pc]]

            elif opcode[pc] == 1872:  # EOR
                register[arg3[pc]] = register[arg2[pc]] ^ register[arg1[pc]]

            else:
                print("")


            if not branchFlag: # Regualr Pc + 4 (but using 1 for the array) :D
                self.printData(cycle, pc)
                pc += 1

            cycle += 1
            branchFlag = False
        self.printData(cycle,pc)
        outfileSim.close()

    def printData(self, cycle, pc):
        if trace: print("PrintData Simulator")
        line = ("====================\n")
        if opcodeStr == "\tNOP":
            line = line + ("cycle: " + str(cycle) + " " + str(mem[pc]) + opcodeStr[pc] +"\n\n")
        else:
            line = line + ("cycle: " + str(cycle) + " " + str(mem[pc]) + opcodeStr[pc] + arg1Str[pc] + arg2Str[pc] + arg3Str[pc] + "\n\n")
        line = line + ("registers:\n")
        line = line + ("R00:\t" + str(register[0]) +"\t" + str(register[1]) + "\t" + str(register[2]) + "\t" + str(register[3]) + "\t" + str(register[4]) + "\t" + str(register[5]) + "\t" + str(register[6]) +"\t" + str(register[7]) +"\n" )
        line = line + ("R08:\t" + str(register[8]) +"\t" + str(register[9]) + "\t" + str(register[10]) + "\t" + str(register[11]) + "\t" + str(register[12]) + "\t" + str(register[13]) + "\t" + str(register[14]) +"\t" + str(register[15])+"\n" )
        line = line + ("R16:\t" + str(register[16]) +"\t" + str(register[17]) + "\t" + str(register[18]) + "\t" + str(register[19]) + "\t" + str(register[20]) + "\t" + str(register[21]) + "\t" + str(register[22]) +"\t" + str(register[23]) +"\n")
        line = line + ("R24:\t" + str(register[24]) +"\t" + str(register[25] )+ "\t" + str(register[26]) + "\t" + str(register[27]) + "\t" + str(register[28]) + "\t" + str(register[29]) + "\t" + str(register[30]) +"\t" + str(register[31]) +"\n\n" )
        line = line + ("data:"+"\n")
        outfileSim.write(line)

        # Makes sure Data has a mod 8 = 0 amount
        while (len(data) % 8) != 0:
            data.append(0)
            last = int(memData[len(memData) -1],base=10)
            memData.append(str(last + 4))

        j = 0
        # Prints the Data
        while j <(len(memData)):
            line = (memData[j]+":" + str(data[j]) + "\t" + str(data[j+1]) + "\t" + str(data[j+2]) + "\t" + str(data[j+3]) + "\t" + str(data[j+4]) + "\t" + str(data[j+5])+ "\t" + str(data[j+6])+ "\t" + str(data[j+7]) + "\n")
            j += 8
            outfileSim.write(line)
        line = "\n\n"
        outfileSim.write(line)
"""

class Entry:
    val1 = -1
    val2 = -1
    val3 = -1
    reg1 = -1
    reg2 = -1
    reg3 = -1 # SAVING REGISTER (DESTINATION) USED ONLY FOR
    opcode = -1
    result = -1 # SAVE ANSWER OF ALU AND MEM INTO HERE



class Pipeline:
    def __init__(self):
        if(trace): print("Pipline")
        global preIssue
        global preMEM
        global preALU
        global postALU
        global postMEM
        test = Entry()
        global test
        test.a1 = 1
        test.a2 = 2
        postALU.append(test)
        postMEM.append(test)
        preIssue.append(test)
        preMEM.append(test)
        preALU.append(test)



    def run(self):
        """TEMP CODE"""
        wb = WB()
        alu = ALU()
        if len(postMEM) > 0 or len(postALU) > 0:
            wb.run()
        if len(preMEM) > 0:
            print("DO MEM")
        if len(preALU) > 0:
            alu.run()
        if len(preIssue) > 0:
            print("DO ISSUE")
        print("DO IF")


class WB:
    def __init__(self):
        if (trace): print ("WB")

    def run(self):
        if len(postMEM) > 0:
            temp = postMEM.pop(0)
            register[temp.reg3] = temp.result
        if len(postALU) > 0:
            temp = postALU.pop(0) #TOP OF THE LIST
            register[temp.reg3] = temp.result

class ALU:
    def __init__(self):
        if(trace): print("ALU")

    def run(self):
        while len(preALU) > 0:
            temp = preALU.pop(0)
            if temp.opcode == 1112:  # ADD
                temp.result = temp.val1 + temp.val2

            elif temp.opcode == 1160 or temp.opcode == 1161:  # ADDI
                temp.result = temp.val2 + temp.val1

            elif temp.opcode == 1104:  # AND
                temp.result = temp.val1 & temp.val2

            elif temp.opcode == 1691:  # LSL
                temp.result = temp.val2 << temp.val1

            elif temp.opcode == 1690:  # LSR
                if temp.val2 < 0:
                    temp.result = (temp.val2 * -1) >> temp.val1
                else:
                    temp.result = (temp.val2 >> temp.val1)

            elif temp.opcode == 1692:  # ASR
                temp.result = (temp.val2 >> temp.val1)

            elif temp.opcode == 1624:  # SUB
                temp.result = temp.val1 - temp.val2

            elif temp.opcode == 1672 or temp.opcode == 1673:  # SUBI
                temp.result = temp.val2 - temp.val1

            elif 1684 <= temp.opcode <= 1687:  # MOVZ
                temp.result = int(temp.val2 * 2 ** temp.val1)

            elif 1940 <= temp.opcode<= 1943:  # MOVK
                temp.result = int(temp.val3 + temp.val2 * 2 ** temp.val1)

            elif temp.opcode == 1360:  # ORR
                temp.result = temp.val2 | temp.val1

            elif temp.opcode == 1872:  # EOR
                temp.result = temp.val2 ^ temp.val1

            postALU.append(temp)





if __name__ == "__main__":
    main()

