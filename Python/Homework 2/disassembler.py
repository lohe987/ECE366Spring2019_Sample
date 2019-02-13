# ECE 366 Computer Organization  Spring2019
# Instructor: Wenjing Rao
# Author: Trung Le

# A simple Python program to get students started on Homework 2
# Reference sheet:   http://www.mrc.uidaho.edu/mrc/people/jff/digital/MIPSir.html

def processInstr(instr):
    if(instr[0:6] == "001101"):  # ORI
        if(instr[16] == '1'):   # Negative immediate conversion
            imm = 65535 - int(instr[16:32],2) + 1
            imm = -imm
        else:
            imm = int(instr[16:32],2)
        print("ori $" + str(int(instr[11:16],2)) + ",$" + str(int(instr[6:11],2)) + "," + str(imm))
    
    elif(instr[0:6] == "000000" and instr[21:32] =="00000100010") : # SUB
        print("sub $" +str(int(instr[16:21],2)) + ",$" + str(int(instr[6:11],2)) + ",$" + str(int(instr[11:16],2))    )

    elif(instr[0:6] == "100011"): # LW
        if(instr[16] == '1'):   # Negative immediate conversion
            imm = 65535 - int(instr[16:32],2) + 1
            imm = -imm
        else:
            imm = int(instr[16:32],2)
        print("lw $" + str(int(instr[11:16],2)) + "," + str(imm) + "($" + str(int(instr[6:11],2)) + ")")

    # You need to finish the following instructions
    #elif() # ADD
    #   TO DO


    #elif() # ADDI 
    #   TO DO


    #elif() # SLT
    #   TO DO


    #elif() # SW
    #   TO DO

    else:
        print("Instruction " + instr + " not supported. Exiting")
        exit()

def main():
    filename = "machine.txt"
    print("Reading in machine code from " + filename)
    file = open(filename,"r")
    for line in file:
        if (line == "\n"):
            continue    # Skip empty lines

        instr = bin(int(line[2:10],16))[2:].zfill(32)
        #  'zfill' pads the string with 0's to normalize instruction's length of 32

        print("\nhex:" + line + "bin:" + instr)
        print(instr[0:4]+ " " +instr[4:8] + " " + instr[8:12] + " " + instr[12:16]+ " " + instr[16:20]+ " "+ instr[20:24]+ " "+ instr[24:28]+ " "+ instr[28:32])

        processInstr(instr)



if __name__ == "__main__":
    main()
