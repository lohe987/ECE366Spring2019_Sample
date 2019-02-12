
# UIC, ECE366, Spring 2019
# Instructor: Wenjing Rao
# Code sample for homework2
# A disassembler that supports the MIPS instructions sub, ori, and lw. 
# Note: disassembler goes from machine code to assembly 

# Details of the supported instructions:
# -----------------------------------------------------------------------------------------------------
# LW -- Load word
# Description: A word is loaded into a register from the specified address.
# Operation: $t = MEM[$s + offset]; advance_pc (4);
# Syntax: lw $t, offset($s)
# Encoding: 1000 11ss ssst tttt iiii iiii iiii iiii 
# -----------------------------------------------------------------------------------------------------
# ORI -- Bitwise or immediate
# Description: Bitwise ors a register and an immediate value and stores the result in a register
# Operation: $t = $s | imm; advance_pc (4);
# Syntax: ori $t, $s, imm
# Encoding: 0011 01ss ssst tttt iiii iiii iiii iiii 
# -----------------------------------------------------------------------------------------------------
# SUB -- Subtract
# Description: Subtracts two registers and stores the result in a register
# Operation: $d = $s - $t; advance_pc (4);
# Syntax: sub $d, $s, $t
# Encoding: 0000 00ss ssst tttt dddd d000 0010 0010
# -----------------------------------------------------------------------------------------------------

def disassemble( instructions ): 
	for fetch in instructions:
		s = str( int( fetch[6:11], 2 ) )
		t = str( int( fetch[11:16], 2 ) )
		if ( fetch[0:6] ==  "100011" ): 	# LW			
			offset = str( int( fetch[16], 2 ) )
			print( "lw $" + t + ", " + offset + "($" + s + ")" )
		if ( fetch[0:6] ==  "001101" ):		# ORI			
			imm = str( int( fetch[16], 2 ) )
			print( "ori $" + t + ", $" + s + " " + imm )
		if ( fetch[0:6] ==  "000000" ):		# SUB
			d = str( int( fetch[16:21], 2 ) )
			print( "sub $" + d + ", $" + s + ", $" + t )

def main():
	fileName = input( "Please enter MIPS instruction file name: " )
	print( "Note: This program assumes that the instructions are in hex." )
	inputFile = open( fileName, "r" )
	instructions = []	# Declares instructions to be an array
	for line in inputFile:
		if ( line == "\n" or line[0] =='#' ):              # empty lines and comments ignored
			continue
		line = line.replace( '\n', '' )	# Removes new line characters
		line = format( int( line, 16 ), "032b" )	# The int function converts the hex instruction into some numerical value, then format converts it into a binary string 
		instructions.append( line )
	inputFile.close()
	disassemble( instructions )

# These next lines are necessary in Python in order for the Python interpreter to call the main function. 
# It's not really necessary to understand how it works for this class, but it allows us to use this code as a module or a standalone program. 
if __name__ == "__main__":
	main()


