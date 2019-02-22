# Sample simulator for ECE366, spring 2019
# Instructor: Dr. Wenjing Rao
# Code written by Peter

# Supported instructions along with some assumptions:
#   ori: I-type, assuming zero extension
#   addi: I-type, assuming sign extension, can deal with negative numbers in 2's cmp
#   sub: R-type, assuming registers containing numbers in 2's cmp
#   beq: I-type, with the following functionality:
#       if rs == rt, pc = pc+4+imm<<2
#       if rs != rt, pc = pc+4

def simulate( instructions, instructionsHex, debugMode ):
	registers = [0, 0, 0, 0, 0, 0, 0, 0]
	#memSize = 80 	#in bytes
	#memory = [0 for i in range( memSize )]
	programDone = False
	PC = 0		#program counter 
	DIC = 0 	#dynamic instruction count 

	print( "Starting simulation..." )
	while ( not( programDone ) ):
		fetch = instructions[PC]
		if ( fetch[0:32] == "00010000000000001111111111111111" ):
			programDone = True
			DIC += 1
		elif ( fetch[0:6] == "001000" ):	#addi
			imm = int( fetch[16:32],2 ) if fetch[16] == '0' else -( 65536 - int( fetch[16:32],2 ) ) #range of number for 16 bit unsigned is 0 to 65535
			if ( debugMode ):
				print( "PC = " + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "addi $" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) + "," + str(imm) )
			PC += 1
			DIC += 1
			registers[int(fetch[11:16], 2)] = registers[int(fetch[6:11], 2)] + imm
		elif ( fetch[0:6] == "001101" ):	#ori
			imm = int( fetch[16:32],2 ) if fetch[16] == '0' else -( 65536 - int( fetch[16:32],2 ) ) #range of number for 16 bit unsigned is 0 to 65535
			if ( debugMode ):
				print("PC = " + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "ori $" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) + "," + str(imm) )
			imm = int( fetch[16:32],2 )	#I'm basically ignoring the fact that this could be a negative number since it we're zero-extending it.
			PC += 1
			DIC += 1
			registers[int(fetch[11:16], 2)] = registers[int(fetch[6:11], 2)] | imm
		elif ( fetch[0:6] == "000000" ):	#sub
			if ( debugMode ):
				print("PC = " + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "sub $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
			PC += 1
			DIC += 1
			registers[int(fetch[16:21], 2)] = registers[int(fetch[6:11], 2)] - registers[int(fetch[11:16], 2)]
		elif ( fetch[0:6] == "000100" ):	#beq
			imm = int( fetch[16:32],2 ) if fetch[16] == '0' else -( 65536 - int( fetch[16:32],2 ) )
			if ( debugMode ):
				print( "PC = " + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "beq $" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) + "," + str(imm) )
			PC += 1
			DIC += 1
			if ( registers[int(fetch[6:11], 2)] == registers[int(fetch[11:16], 2)] ):
				PC = PC + imm
		else:
			print( "Unsupported instruction, ending simulator..." )
			programDone = True


def main():
	print( "Note: This program assumes that the instructions are in hex." )
	fileName = input( "Please enter MIPS instruction file name: " )
	inputFile = open( fileName, "r" )
	instructions = []	# Declares instructions to be an array
	instructionsHex = []
	for line in inputFile:
		if ( line == "\n" or line[0] =='#' ):              # empty lines and comments ignored
			continue

		line = line.replace( '\n', '' )	# Removes new line characters
		instructionsHex.append( line )
		line = format( int( line, 16 ), "032b" )	# The int function converts the hex instruction into some numerical value, then format converts it into a binary string 
		instructions.append( line )
	inputFile.close()
	debugMode = True if  int( input( "1 = debug mode         2 = normal execution\n" ) ) == 1 else False
	simulate( instructions, instructionsHex, debugMode )


if __name__ == "__main__":
    main()
