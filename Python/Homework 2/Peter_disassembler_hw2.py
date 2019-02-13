
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
			if ( fetch[16] == "0" ):			
				offset = str( int( fetch[16:], 2 ) )
			else:
				offset = format( int( fetch[16:], 2) - 1, "016b" ) 	# If we want to represent a negative value, we take the binary representation of its magnitude 
									# invert all the bits, then add one. This is just meant to reverse to process since we start with the negative string.
				inverted_offset = ""
				for index in range( 16 ):	# bitwise inversion of the binary string
					if ( offset[index] == "0" ):
						inverted_offset = inverted_offset + "1"
					else:
						inverted_offset = inverted_offset + "0" 
				offset = str( -1 * int( inverted_offset, 2 ) ) 
			print( "lw $" + t + ", " + offset + "($" + s + ")" )
		elif ( fetch[0:6] ==  "001101" ):		# ORI
			if ( fetch[16] == "0" ):			
				imm = str( int( fetch[16:], 2 ) )
			else:
				imm = format( int( fetch[16:], 2) - 1, "016b" ) 	# If we want to represent a negative value, we take the binary representation of its magnitude 
									# invert all the bits, then add one. This is just meant to reverse to process since we start with the negative string. 
				inverted_imm = ""
				for index in range( 16 ):	# bitwise inversion of the binary string
					if ( imm[index] == "0" ):
						inverted_imm = inverted_imm + "1"
					else:
						inverted_imm = inverted_imm + "0"
				imm = str( -1 * int( str( inverted_imm ), 2 ) ) 
			print( "ori $" + t + ", $" + s + " " + imm )
		elif ( fetch[0:6] ==  "000000" ):		# SUB
			d = str( int( fetch[16:21], 2 ) )
			print( "sub $" + d + ", $" + s + ", $" + t )
		else: 
			print( "Unsupported instruction." )

def main():
	fileName = input( "Please enter MIPS instruction file name: " )
	print( "Note: This program assumes that the instructions are in hex." )
	inputFile = open( fileName, "r" )
	instructions = []	# Declares instructions to be an array
	for line in inputFile:
		if ( line == "\n" or line[0] =='#' ):              # empty lines and comments ignored
			continue
		for index in line:			#This loop will remove any comments. 
			if ( line[index] == "#" ):
				line = line[:index] 
		line = line.replace( '\n', '' )	# Removes new line characters
		line = format( int( line, 16 ), "032b" )	# The int function converts the hex instruction into some numerical value, then format converts it into a binary string 
		instructions.append( line )
	inputFile.close()
	disassemble( instructions )

# These next lines are necessary in Python in order for the Python interpreter to call the main function. 
# It's not really necessary to understand how it works for this class, but it allows us to use this code as a module or a standalone program. 
if __name__ == "__main__":
	main()


