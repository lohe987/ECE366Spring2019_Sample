# Just quickly test all the instructions so make sure that they work properly...

somewhere_over_the_rainbow:
	ori $0, $0, 0x1000
	addi $1, $0, 0x2000
	sub $2, $0, $1
	lw $3, 0x0FFC($1)
	beq $0, $1, somewhere_over_the_rainbow

addi $4, $0, 8
addi $5, $0, 0

loop:
	lw $3, 0($1)	#miss
	lw $3, 4($1)	#hit
	lw $3, 8($1)	#hit
	lw $3, 12($1)	#hit
	addi $1, $1, 0x0010	#Moves the address to the next set
	addi $5, $5, 1
	beq $4, $5, done
	beq $0, $0, loop
done:
	beq $0, $0, done

