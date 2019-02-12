sub $1, $1, $1
ori $1, $2, 10
lw $1, ($2)

stall_loop:
	j stall_loop 