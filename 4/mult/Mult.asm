// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

// approach: start the sum at zero and add r0, r1 times.
// r2 stores the running sum and the final answer.
// count stores the number of additions already completed.
// assumes r0 >= 0, r1 >= 0, and r0*r1 < 32768.

    // clear r2 so the sum starts at zero
    @R2
    M=0

    // set the counter to zero because no additions have happened yet
    @count
    M=0

(LOOP)
    // load the number of completed additions into d
    @count
    D=M

    // subtract r1 from the counter
    // a result of zero means we have completed enough additions
    @R1
    D=D-M

    // stop when the counter equals r1
    // if r1 is zero, this also leaves the answer as zero
    @STOP
    D;JEQ

(ADD)
    // load the value being repeatedly added into d
    @R0
    D=M

    // add r0 to the running sum stored in r2
    @R2
    M=D+M

    // increase the counter because one more addition is complete
    @count
    M=M+1

    // return to the loop to check whether another addition is needed
    @LOOP
    0;JMP

(STOP)
    // hack assembly has no halt instruction
    // jump here forever so the final answer stays in r2
    @STOP
    0;JMP