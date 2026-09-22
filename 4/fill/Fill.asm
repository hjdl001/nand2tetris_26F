// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// approach: use the keyboard memory-mapped register to check if a key is pressed. 
////if a key is pressed, write 0xFFFF to every pixel in the screen memory. 
//// ff no key is pressed, write 0x0000 to every pixel in the screen memory.

(LOOP)
    // check if a key is currently being pressed
    @KBD
    D=M

    // if the keyboard value is zero, no key is being pressed
    @WHITE
    D;JEQ

(BLACK)
    // set the color value to black
    @color
    M=-1

    // start filling at the first screen address
    @SCREEN
    D=A
    @address
    M=D

(FILL_BLACK)
    // fill the screen with black
    @address
    A=M
    M=D
    @address
    M=M+1
    @FILL_BLACK
    D;JLT

(WHITE)
    // if the keyboard value is not zero, a key is being pressed
    // set the color value to white
    @color
    M=0     
