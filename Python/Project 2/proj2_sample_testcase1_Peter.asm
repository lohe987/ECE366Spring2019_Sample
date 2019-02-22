addi $1, $0, 5		#test comment
addi $2, $0, 1
addi $3, $0, 2

loop:
	ori $4, $3, 0xFFFF
	sub $3, $3, $2	
	sub $1, $1, $2
	beq $1, $0, end
	beq $0, $0, loop
end:
	beq $0, $0, end
