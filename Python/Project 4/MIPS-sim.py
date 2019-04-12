

import time

# This class keeps track of all the statistics needed for
# simulation results.
# Feel free to add any stats 
class Statistic:
    
    def __init__(self,debugMode):
        self.I = ""              # Current instr being executed
        self.name = ""           # name of the instruction
        self.cycle = 0           # Total cycles in simulation
        self.DIC = 0             # Total Dynamic Instr Count
        self.threeCycles= 0      # How many instr that took 3 cycles to execute
        self.fourCycles = 0      #                          4 cycles
        self.fiveCycles = 0      #                          5 cycles
        self.debugMode = debugMode
        #self.DataHazard = 0     # Helpful statistics needed for slow-pipe, fast-pipe implementation
        #self.ControlHazard = 0  #
        #self.NOPcount = 0       #
        #self.flushCount = 0     #
        #self.stallCount = 0     #

    def log(self,I,name,cycle,pc):
        self.I = I
        self.name = name
        self.cycle = self.cycle + cycle
        self.pc = pc
        self.DIC += 1
        self.threeCycles += 1 if (cycle == 3) else 0
        self.fourCycles += 1 if (cycle == 4) else 0
        self.fiveCycles += 1 if (cycle == 5) else 0

        # Student TO-DO:
        # update data + control hazards, NOP, flush, stall statistics


    # Since the self.cycle has the updated cycles, need to substract x cycles for correct printing , i.e (self.cycle - x)
    def prints(self):
        imm = int(self.I[16:32],2) if self.I[16]=='0' else -(65535 -int(self.I[16:32],2)+1)
        if(self.debugMode):
            print("\n")
            print("Instruction: " + self.I)
            if(self.name == "add"):
                print("Cycle: " + str(self.cycle-4) + "|PC: " +str(self.pc*4) + " add $" + str(int(self.I[16:21],2)) + ",$" +str(int(self.I[6:11],2)) + ",$" + str(int(self.I[11:16],2)) + "   Taking 4 cycles")
            elif(self.name == "addi"):
                print("Cycle: " + str(self.cycle-4) + "|PC: " +str(self.pc*4) + " addi $" + str(int(self.I[16:21],2)) + ",$" +str(int(self.I[6:11],2)) + ","  + str(imm)  + "   Taking 4 cycles")
            elif(self.name == "beq"):
                print("Cycle: " + str(self.cycle-3) + "|PC: " +str(self.pc*4) + " beq $" + str(int(self.I[6:11],2)) + ",$" +str(int(self.I[11:16],2)) + ","  + str(imm)  + "   Taking 3 cycles")
            elif(self.name == "slt"):
                print("Cycle: " + str(self.cycle-4) + "|PC: " +str(self.pc*4) + " slt $" + str(int(self.I[16:21],2)) + ",$" +str(int(self.I[6:11],2)) + ",$" + str(int(self.I[11:16],2)) + "   Taking 4 cycles")
            elif(self.name == "sw"):
                print("Cycle: " + str(self.cycle-4) + "|PC :" +str(self.pc*4) + " sw $" + str(int(self.I[6:11],2)) + "," + str(int(self.I[16:32],2) - 8192) + "($" + str(int(self.I[6:11],2)) + ")" + "   Taking 4 cycles"  )
            else:
                print("")

    def exitSim(self):
        print("***Finished simulation***")
        print("Total # of cycles: " + str(self.cycle))
        print("Dynamic instructions count: " +str(self.DIC) + ". Break down:")
        print("                    " + str(self.threeCycles) + " instructions take 3 cycles" )  
        print("                    " + str(self.fourCycles) + " instructions take 4 cycles" )
        print("                    " + str(self.fiveCycles) + " instructions take 5 cycles" )




def simulate(Instructions, InstructionsHex, debugMode):
    start_time = time.time()
    print("***Starting simulation***")
    Register = [0 for i in range(24)]   # initialize registers from $0-$24, but 
                                        # only utilize $8 - $23 as stated in guideline
    Memory = [0 for i in range(1024)]
    stats = Statistic(debugMode) # init. the statistic class, keeps track of debugmode as well

    PC =  0  

    finished = False
    while(not(finished)):
        fetch = Instructions[PC]
        
        if(fetch[0:32] == '00010000000000001111111111111111'):
            finished = True
            print("PC = " + str(PC*4) + "  Instruction: 0x" + InstructionsHex[PC] + " : Deadloop. Exiting simulation" )

        elif(fetch[0:6] == '000000' and fetch[26:32] == '100000'): 
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] + Register[int(fetch[11:16],2)]
            stats.log(fetch,"add", 4,PC)  # ADD instr, 4 cycles
            PC += 1

        elif(fetch[0:6] == '001000'):  
            imm = int(fetch[16:32],2) if fetch[16]=='0' else -(65535 -int(fetch[16:32],2)+1)
            Register[int(fetch[11:16],2)] = Register[int(fetch[6:11],2)] + imm
            stats.log(fetch,"addi", 4, PC) # ADDI instr, 4 cycles
            PC += 1

        elif(fetch[0:6] == '000100'):  
            imm = int(fetch[16:32],2) if fetch[16]=='0' else -(65535 -int(fetch[16:32],2)+1)
            stats.log(fetch,"beq", 3, PC) # BEQ instr, 3 cycles
            PC += 1
            PC = PC + imm if (Register[int(fetch[6:11],2)] == Register[int(fetch[11:16],2)]) else PC

        elif(fetch[0:6] == '000000' and fetch[26:32] == '101010'):
            Register[int(fetch[16:21],2)] = 1 if Register[int(fetch[6:11],2)] < Register[int(fetch[11:16],2)] else 0
            stats.log(fetch,"slt", 4, PC) # SLT instr, 4 cycles
            PC += 1
        elif(fetch[0:6] == '101011'):
            #Sanity check for word-addressing 
            if ( int(fetch[30:32])%4 != 0 ):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", hex(int(fetch,2)))
                exit()       
            imm = int(fetch[16:32],2)
            Memory[imm + Register[int(fetch[6:11],2)] - 8192]= Register[int(fetch[11:16],2)] # Store word into memory
            stats.log(fetch,"sw", 4, PC)    # SW instr, 4 cycles
            PC += 1
        else:
            print("Instruction " + str(InstructionsHex[PC]) + " not supported. Exiting")
            exit()

        if(not(finished)):
            stats.prints()

    if(finished):
        elapsed_time = time.time() - start_time
        stats.exitSim()
        print("Registers: " + str(Register))
        print("Total elapsed time: " + str(elapsed_time) + " seconds")
        


    




def main():
    
    Instructions = []   # a place to hold all instructions
    InstructionsHex = [] # raw data of instruction , in hex
    print("Welcome to ECE366 Advanced MIPS Simulator.  Please choose the mode of running: ")
    debugMode = True if int(input(" 1 = Debug Mode         2 = Normal Execution \n")) == 1 else False
    if (debugMode):
        print("Debug Mode\n") 
    else:
        print("Normal Execution \n")
    I_file = open("i_mem_TRUNG.txt", "r")
    for line in I_file:
        if(line == "\n" or line[0] =='#'):
            continue    # ignore empty lins, comments
        line = line.replace('\n', '')   # delete endline characters in the line
        InstructionsHex.append(line)
        line = format(int(line,16),"032b")
        Instructions.append(line)

    simulate(Instructions, InstructionsHex, debugMode)


if __name__ == "__main__":
    main()
