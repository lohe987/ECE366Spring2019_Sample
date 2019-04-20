# Supported instructions along with some assumptions:
#   ori: I-type, assuming zero extension
#   addi: I-type, assuming sign extension, can deal with negative numbers in 2's cmp
#   sub: R-type, assuming registers containing numbers in 2's cmp
#   beq: I-type, with the following functionality:
#       if rs == rt, pc = pc+4+(imm<<2)
#       if rs != rt, pc = pc+4
#   lw support has been added 

# run with Python3
# There's some poor coding habits in this. 
# I'll probably switch over to using 4 spaces for Python in future code since python uses so much indentation

# I added a variable to keep track of the pipeline cycle count and wrote some really basic bookkeeping code.
# It doesn't handle any of the hazards.

# The cache configuration that's provided in the sample code has 8 blocks, thus 8 sets since it's a direct mapped cache.
# Since it's a direct mapped cache, I didn't bother creating a set class, but it's something that should be considered
# if you end up using this sample code as your base.
# The sample code already supports the user choosing how many words are in a block, but the words are always 4 bytes; 
# other dimensions of the cache 

from math import log, ceil
import random 

MEM_SPACE = 1024	#4-byte word accessible memory space 
Memory = [0 for i in range(MEM_SPACE)] 

# This memory space will correspond to the address spaces 0x2000 - 0x3000 when used by lw (and sw if it were implemented)
# 0x1000 == 0d4096, and 4096 / 4 == 1024, thus 1024 words

class Block:
	def __init__(self, _wordsPerBlock, _whichSet):
		self.data = [ 0 for i in range( _wordsPerBlock ) ]
		self.size = _wordsPerBlock
		self.setIndex = format( _whichSet, 'b' ) # Since this is a direct-mapped cache, I can get away with combining the block and set class
							# Blocks and set are not the same thing though. 
		self.valid = False 
		self.tag = "undefined"
	def LoadBlock(self, memIndex, tag ):
		#print( "memIndex: " + str( memIndex ) )
		self.tag = tag
		self.valid = True
		for i in range( self.size ): 
			self.data[i] = Memory[i +  memIndex] 

	#Have this function return 1 if valid && tag match, -1 if not valid && tag doesn't match
	def CheckBlockTag( self, tag ):
		if ( self.valid == False ): 
			return -1
		if ( self.tag != tag ):
			return -1
		return 1
	def ReadBlock( self, offset ):
		return self.data[offset]

# A direct mapped cache with 8 blocks in it, but the user can chose the words per block
class Cache:
	def __init__(self, _wordsPerBlock):
		self.Cache = [] 	#Declares cache to be an empty list		
		for i in range( 8 ): 		
			tempBlock = Block( _wordsPerBlock, i )
			self.Cache.append( tempBlock )  #Adds a block to the end of the list, but caches should really be made up of sets
		self.wordsPerBlock = _wordsPerBlock
		self.blockCount = 8 
		# There are a lot of other things that the Cache should keep track of.
		# Try to have each level of the data structure also contain information that you think you'd need at that level. 

	def AccessCache( self, addr, outFile):	
		inBlkOffset = addr[-( 2 + ceil( log( self.wordsPerBlock, 2) ) ): -2]
		# 8 sets means I need 8 patterns from the address so I know which set to access, thus 3 bits of the address are devoted to set index. 
		setIndex = int( addr[-( 2 + 3 + ceil( log( self.wordsPerBlock, 2) ) ):-( 2 + ceil( log( self.wordsPerBlock, 2) ) )], 2 )
		# Negative values are kind of nifty to use in Python for accessing indices from right to left instead of the default left to right
		# The tail of the list has the index -1 (I think...), and it basically works the same way as the value grows in magnitude. 
		tag = addr[:-( 2 + 3 + ceil( log( self.wordsPerBlock, 2) ) )]
		if ( self.Cache[setIndex].CheckBlockTag( tag ) == -1 ):
			outFile.write( "Cache miss, loading correct block from deeper memory...\n" )
			zeroString = ""
			if ( self.wordsPerBlock != 1 ): 	#This is easier than trying to think through the issue mentioned below 
				for i in range( ceil( log( self.wordsPerBlock, 2 ) ) ):	#There might be a bug here with this loop if wordsPerBlock is 1 or 0; 0 should be a rejected number though
					zeroString = zeroString + "0"  	#Does it execute at all if wordsPerBlock is 1? Hopefully it doesn't...
			memIndex = ( int( ( tag + format( setIndex, "03b" ) + zeroString + "00" ), 2 ) // 4 ) - 2048
			self.Cache[setIndex].LoadBlock( memIndex, tag )
		else:
			outFile.write( "Cache hit! Accessing data now...\n" )
		data = self.Cache[setIndex].ReadBlock( int( inBlkOffset, 2 ) )
		return data 

def simulate( instructions, instructionsHex, debugMode, program):

	outFile = open("output_" + program , "w")
	registers = [0, 0, 0, 0, 0, 0, 0, 0]
	programDone = False
	PC = 0		#program counter 
	DIC = 0 	#dynamic instruction count
	#counters
	Cycle = 0
	threeCycles = 0     
	fourCycles = 0      
	fiveCycles = 0	
	pipelineCycles = 4

	DM_Cache = Cache( 4 ) #Create a direct mapped cache that has 4 words per block

	print( "Starting simulation..." )
	while ( not( programDone ) ):
		fetch = instructions[PC]
		registers[0] = 0 
		if ( fetch[0:32] == "00010000000000001111111111111111" ): 	#This is technically a branch instruction
			programDone = True
			DIC += 1
			threeCycles += 3
			Cycle += 3
			pipelineCycles += 1
		elif ( fetch[0:6] == "001000" ):	#addi
			imm = int( fetch[16:32],2 ) if fetch[16] == '0' else -( 65536 - int( fetch[16:32],2 ) ) #range of number for 16 bit unsigned is 0 to 65535
			if ( debugMode ):
				print("Cycle " + str(Cycle) + " for multi-cycle:")
				print("PC =" + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "addi $" + str(int(fetch[11:16],2)) + ",$" + str(int(fetch[6:11],2)) + ", " + str(imm) )
				print("Taking 4 cycles for multi-cycle\n")
			outFile.write("Cycle " + str(Cycle) + " for multi-cycle:\n")
			outFile.write("PC =" + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "addi $" + str(int(fetch[11:16],2)) + ",$" + str(int(fetch[6:11],2)) + ", " + str(imm) + "\n" )
			outFile.write("Takes 4 cycles for multi-cycle\n\n")
			PC += 1
			Cycle += 4
			fourCycles += 1
			pipelineCycles += 1
			DIC += 1
			registers[int(fetch[11:16], 2)] = registers[int(fetch[6:11], 2)] + imm
		elif ( fetch[0:6] == "001101" ):	#ori
			imm = int( fetch[16:32],2 ) if fetch[16] == '0' else -( 65536 - int( fetch[16:32],2 ) ) #range of number for 16 bit unsigned is 0 to 65535
			if ( debugMode ):
				print("Cycle " + str(Cycle) + " for multi-cycle:")
				print( "PC = " + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "ori $" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) + "," + str(imm) )
				print("Takes 4 cycles for multi-cycle\n")
			outFile.write( "Cycle " + str(Cycle) + " for multi-cycle:\n" )
			outFile.write( "PC = " + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "ori $" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) + "," + str(imm) + "\n" )
			outFile.write( "Takes 4 cycles for multi-cycle\n\n" )
			imm = int( fetch[16:32],2 )	#I'm basically ignoring the fact that this could be a negative number since it we're zero-extending it.
			PC += 1
			Cycle += 4
			fourCycles += 1
			pipelineCycles += 1
			DIC += 1
			registers[int(fetch[11:16], 2)] = registers[int(fetch[6:11], 2)] | imm
		elif ( fetch[0:6] == "000000" ):	#sub
			#rs = int( fetch[6:11],2 )
			#rt = int( fetch[11:16],2 )
			#rd = int(fetch[16:21],2)
			if ( debugMode ):
				print("Cycle " + str(Cycle) + " for multi-cycle:")
				print("PC =" + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "sub $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
				print("Takes 4 cycles for multi-cycle\n")
			outFile.write("Cycle " + str(Cycle) + " for multi-cycle:\n")
			outFile.write("PC =" + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "sub $" + str(int(fetch[16:21],2)) + ",$" + str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) + "\n" )
			outFile.write("Takes 4 cycles for multi-cycle\n\n")
			PC += 1
			Cycle += 4
			fourCycles += 1
			pipelineCycles += 1
			DIC += 1
			registers[int(fetch[16:21], 2)] = registers[int(fetch[6:11], 2)] - registers[int(fetch[11:16], 2)]
		elif ( fetch[0:6] == "000100" ):	#beq
			imm = int( fetch[16:32],2 ) if fetch[16] == '0' else -( 65536 - int( fetch[16:32],2 ) )
			if ( debugMode ):
				print("Cycle " + str(Cycle) + " for multi-cycle:")
				print("PC =" + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "beq $" + str(int(fetch[6:11],2)) + ",$" +str(int(fetch[11:16],2)) + "," + str(imm) )
				print("Takes 3 cycles for multi-cycle\n")
			outFile.write("Cycle " + str(Cycle) + " for multi-cycle:\n")
			outFile.write("PC =" + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "beq $" + str(int(fetch[6:11],2)) + ",$" +str(int(fetch[11:16],2)) + "," + str(imm) + "\n" )
			outFile.write("Takes 3 cycles for multi-cycle\n\n")
			Cycle += 3
			threeCycles += 1
			pipelineCycles += 1
			PC += 1
			DIC += 1
			if ( registers[int(fetch[6:11], 2)] == registers[int(fetch[11:16], 2)] ):
				PC = PC + imm
		elif ( fetch[0:6] == "100011" ):	#lw
			imm = int( fetch[16:32],2 ) if fetch[16] == '0' else -( 65536 - int( fetch[16:32],2 ) )
			if( debugMode ):
				print("Cycle " + str(Cycle) + "for multi-cycle:")
				print("PC =" + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "lw $" + str(int(fetch[11:16],2)) + ", 0x" + hex( imm ) + "($" + str( int(fetch[6:11],2) ) + ")" )	
				print("Takes 5 cycles for multi-cycle\n")
			outFile.write("Cycle " + str(Cycle) + "for multi-cycle:\n")
			outFile.write("PC =" + str(PC*4) + " Instruction: 0x" +  instructionsHex[PC] + " :" + "lw $" + str(int(fetch[11:16],2)) + ", 0x" + hex( imm ) + "($" + str( int(fetch[6:11],2) ) + ")\n" )	
			outFile.write("Takes 5 cycles for multi-cycle\n\n")
			addr = format( registers[int( fetch[6:11], 2 )] + imm, "032b" ) 
			registers[int(fetch[11:16],2)] = DM_Cache.AccessCache( addr, outFile )
			Cycle += 5
			fiveCycles += 1
			pipelineCycles += 1
			PC += 1
			DIC += 1
		else:
			print( "Unsupported instruction, ending simulator..." )
			programDone = True
	print( "Simulation complete. Now printing register information:" )
	counter = 0
	for register in registers:
		print( "Register " + str( counter ) + ": " + str( register ) )
		counter += 1
	print( "***********************************************************************\n" )
	print( "Dynamic instructions count: " +str(DIC) + "\n\n" )
	print( "PC: " + str( PC ) )
	print("Dynamic instructions count: " +str(DIC) + "\n\n")
	print("Total # of cycles for multi-cycle: " + str(Cycle) + "\n")
	print("                    " + str(threeCycles) + " instructions take 3 cycles\n" )
	print("                    " + str(fourCycles) + " instructions take 4 cycles\n" )
	print("                    " + str(fiveCycles) + " instructions take 5 cycles\n\n" )
	print( "Total cycles for pipelined CPU: "+ str( pipelineCycles ) + "\n\n" )

	outFile.write("***********************************************************************\n")
	outFile.write("Dynamic instructions count: " +str(DIC) + "\n\n")
	outFile.write("Total # of cycles for multi-cycle: " + str(Cycle) + "\n")
	outFile.write("                    " + str(threeCycles) + " instructions take 3 cycles\n" )
	outFile.write("                    " + str(fourCycles) + " instructions take 4 cycles\n" )
	outFile.write("                    " + str(fiveCycles) + " instructions take 5 cycles\n\n" )
	outFile.write( "Total cycles for pipelined CPU: "+ str( pipelineCycles ) + "\n\n" )
	outFile.close()

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
		line = line.replace( ' ', '' ) 
		instructionsHex.append( line )
		line = format( int( line, 16 ), "032b" )	# The int function converts the hex instruction into some numerical value, then format converts it into a binary string 
		instructions.append( line )
	inputFile.close()
	debugMode = True if  int( input( "1 = debug mode         2 = normal execution\n" ) ) == 1 else False
	programName = fileName.replace( ".txt", "" )
	simulate( instructions, instructionsHex, debugMode, programName )


if __name__ == "__main__":
    main()
