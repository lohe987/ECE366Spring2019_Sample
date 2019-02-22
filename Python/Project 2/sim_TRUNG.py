# ECE 366 Computer Organization  Spring2019
# Instructor: Wenjing Rao
# Author: Trung Le

# A simple Python program to get students started on Project 2
# Reference sheet:   http://www.mrc.uidaho.edu/mrc/people/jff/digital/MIPSir.html
# Supported instructions: ori, addi, sub, beq 

def process2Comp(string):
    if(string[0] == '1'):
        imm = 65535 - int(string,2) +1
        imm = -imm
    else:
        imm = int(string,2)
    return imm


def simulate(memory, I):
    PC = 0                                  # Program counter
    Register = [ 0 for i in range(24)]    # Initialize register 8-23 
    finished = False
    print("***Simulation started***")
    while(not(finished)):
        Register[0] = 0     # Let's enforce $0 here
        fetch = I[PC]
        if (fetch == "00010000000000001111111111111111"):   # END instruction
            finished = True
            print("***Simulation finished***")
        elif(fetch[0:6] == "001101"):   # ORI instruction
            imm = int(fetch[16:32],2)
            Rs = int(fetch[6:11],2)
            Rt = int(fetch[11:16],2)
            print("PC " + str(PC) + ":  ori $" + str(Rt) + ",$" + str(Rs) + "," + str(imm))
            Register[Rt] = Register[Rs] | imm
            PC += 4
            print("  result: $" + str(Rt) + "=" + str(Register[Rt]))
        elif(fetch[0:6] == "001000"):   # ADDI instruction
            imm = process2Comp(fetch[16:32])
            Rs = int(fetch[6:11],2)
            Rt = int(fetch[11:16],2)
            print("PC " + str(PC) + ":  addi $" + str(Rt) +  ",$" +  str(Rs) + "," +  str(imm))
            Register[Rt] = Register[Rs] + imm
            PC += 4
            print("  result: $" + str(Rt) + "=" + str(Register[Rt]))
        elif(fetch[0:6] == "000000" and fetch[21:32] == "00000100010"):     # SUB instruction
            Rd = int(fetch[16:21],2)
            Rs = int(fetch[6:11],2)
            Rt = int(fetch[11:16],2)
            print("PC " + str(PC) + ":  sub $" + str(Rd) + ",$" + str(Rs) + ",$" + str(Rt))
            Register[Rd] = Register[Rs] - Register[Rt]
            PC += 4
            print("  result: $" + str(Rd) + "=" + str(Register[Rd]))
        elif(fetch[0:6] == "000100"):   # BEQ instruction
            offset = process2Comp(fetch[16:32])
            Rs = int(fetch[6:11],2)
            Rt = int(fetch[11:16],2)
            print("PC " + str(PC) + ":  beq $" + str(Rs) + ",$" + str(Rt) + "," + str(offset))
            if (Register[Rs] == Register[Rt]):
                PC = PC + 4 + (4*offset)
                print("  result: branch Taken")
            else:
                PC = PC + 4
                print("  result: branch Not Taken")
        

        else:
            print("Instruction not supported. Exiting")
            exit()
    
    print("Registers contents:", Register)
   

def main():
    filename = "program_TRUNG.txt"
    print("Reading in machine code from " + filename)
    file = open(filename,"r")
    memory = [0 for i in range(1000)]     # The memory of the machine
    I = []                                  # Instructions to execute
    for line in file:
        if (line == "\n" or line[0] == "#" ):
            continue    # Skip empty lines and comments
        instr = bin(int(line[2:10],16))[2:].zfill(32)
        #  'zfill' pads the string with 0's to normalize instruction's length of 32
        I.append(instr)
        I.append(0)     # Since PC increments by 4,  let's fill
        I.append(0)     # null spaces with 0's to align correct 
        I.append(0)     # address

    simulate(memory,I)

if __name__ == "__main__":
    main()
