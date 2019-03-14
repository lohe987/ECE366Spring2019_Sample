# ECE 366 Computer Organization  Spring2019
# Instructor: Wenjing Rao
# Author: Trung Le


# Simple simulator for the DC ISA
# Assumption:
#   8-bit instruction
#   8-bit data ( Both registers and memory)
#   4 general purpose registers:   R0, R1, R2, R3

# The DC architecture supports a special instruction called     dc - Drop and Combine
#   Format: dc Rx, Ry
#   Functionality :  drop 4 MSB bits of Ry, drop 4 LSB bits of RX, and comebine Rx and Ry into R0


def process2Comp(string):
    if(string[0] == '1'):
        return -(15 - int(string,2) + 1)
    else:
        return int(string,2)
    

def simulate(memory,I):
    PC = 0                                  # Program counter
    Register = [ 0 for i in range(4)]        # Initialize register R0,R1,R2,R3
    finished = False
    print("***Simulation started***")
    while(not(finished)):
        fetch = I[PC]
        if(fetch == "11111111"): # terminate
            finished = True
        elif(fetch[0:4] == "0100"): # INIT instruction
            PC += 4
            imm = process2Comp(fetch[4:8])
            Register[0] = imm
            print ("init R0," + str(imm))
        elif(fetch[0:4] == "0101"): # ADD instruction
            PC += 4
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            print ("add R" + str(Rx) + ",R" + str(Ry))
            Register[Rx] = Register[Rx] + Register[Ry]
        elif(fetch[0:4] == "0110"): # SUB
            PC += 4
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            Register[Rx] = Register[Rx] - Register[Ry]
            print ("sub R" + str(Rx) + ",R" + str(Ry))
        elif(fetch[0:4] == "0111"): # ADDI
            PC += 4
            Rx = int(fetch[4:6],2)
            imm = int(fetch[4:6],2)
            Register[Rx] = Register[Rx] + imm
            print ("addi R" + str(Rx) + "," + str(imm))
        elif(fetch[0:4] == "1100"): # SLT
            PC += 4
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            print ("slt R" + str(Rx) + ",R" + str(Ry))
            if ( Register[Rx] < Register[Ry]):
                Register[0] = 1
            else:
                Register[0] = 1
        elif(fetch[0:4] == "1101"): # XOR
            PC += 4
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            print ("xor R" + str(Rx) + ",R" + str(Ry))
            Register[Rx] = Register[Rx] ^ Register[Ry]
        elif(fetch[0:4] == "1110"): # DC 
            PC += 4
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            Register[0] = (Register[Rx] & 240) | (Register[Ry] & 15)
            print ("dc R" + str(Rx) + ",R" + str(Ry))
            #  TODO: a bit messy 
            #  '&' is bitwise AND operation,  
            #   '240' is   11110000 binary,
            #    'Rx & 240'   equivalent to dropping 4 bit LSB of Rx
            #   similarly for dropping 4 bit MSB
        elif(fetch[0:4] == "0001"): # LOAD
            PC += 4
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            Register[Rx] = memory[Register[Ry]]
            print ("load R" + str(Rx) + ",R" + str(Ry))
        elif(fetch[0:4] == "0000"): # STORE
            PC += 4
            Rx = int(fetch[4:6],2)
            Ry = int(fetch[6:8],2)
            memory[Register[Ry]] = Register[Rx]
            print ("store R" + str(Rx) + ",R" + str(Ry))
        elif(fetch[0:2] == "10"):   # BEQ
            Rx = int(fetch[2:4],2)
            imm = process2Comp(fetch[4:8])
            if (Register[Rx] == 0):
                PC = PC + 4 + (4*imm)
            else:
                PC += 4
            print("beq R" + str(Rx) + "," + str(imm))
        elif(fetch[0:3] == "001"):  # Jump
            imm = process2Comp(fetch[3:8])
            PC = PC + 4 + (4*imm)
            print("j " + str(imm))
        else:
            print("Instruction not supported. Exiting")
            exit()
    print("Simulation finished")
    print("Registers contents: ", Register)


def main():
    filename = "program_TRUNG.txt"
    print("Reading in machine code from " + filename)
    file = open(filename,"r")
    memory = [0 for i in range(1000)]     # The memory of the machine
    I = []                                  # Instrucdtions to execute
    for line in file:
        if (line == "\n" or line[0] == "#" ):
            continue    # Skip empty lines and comments
        instr = bin(int(line[2:4],16))[2:].zfill(8)
        #  'zfill' pads the string with 0's to normalize instruction's length of 32
        I.append(instr)
        I.append(0)     # Since PC increments by 4,  let's fill
        I.append(0)     # null spaces with 0's to align correct 
        I.append(0)     # address


    simulate(memory,I)
if __name__ == "__main__":
    main()

