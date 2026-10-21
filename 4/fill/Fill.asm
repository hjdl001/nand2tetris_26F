// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// approach: check the keyboard and choose black or white.
// only fill the screen when the color changes.
// color stores the chosen color.
// status stores the color used for the last screen fill.
// address stores the screen location being updated.

// use 1 as an initial status because it is neither black nor white
// this makes sure the program fills the screen the first time
    @status
    M=1

(LOOP)
    // select the keyboard register and read its value into d
    // zero means no key is pressed; nonzero means a key is pressed
    @KBD // keyboard register 
    D=M // keyboard value 

    // jump to white if the keyboard value is zero
    @WHITE
    D;JEQ

    // otherwise, continue into the black case
(BLACK)
    // -1 has all 16 bits set to 1, which makes the pixels black
    @color
    M=-1

    // skip the white case and check if the color changed
    @CHECK
    0;JMP

(WHITE)
    // 0 has all 16 bits set to 0, which makes the pixels white
    @color
    M=0

(CHECK)
    // subtract the previous color from the chosen color
    // a result of zero means the colors are the same
    @color
    D=M
    @status
    D=D-M

    // if the color did not change, check the keyboard again
    @LOOP
    D;JEQ

    // save the chosen color as the new status
    @color
    D=M
    @status
    M=D

    // load the first screen address into d
    // d=a gets the address itself, not the contents at that address
    @SCREEN
    D=A

    // save the first screen address in the address variable
    @address
    M=D

(FILL)
    // load the current screen address into d
    @address
    D=M

    // subtract the keyboard address from the current address
    // kbd is immediately after the last screen word
    @KBD
    D=D-A

    // stop filling when the current address reaches kbd
    // this prevents writing outside the screen memory
    @LOOP
    D;JGE

    // load the chosen color into d
    @color
    D=M

    // select the address variable, then load its stored address into a
    // m now refers to the screen word at that address
    @address
    A=M

    // write the color into that screen word
    // each screen word controls 16 pixels
    M=D

    // move to the next screen word
    @address
    M=M+1

    // repeat until all 8192 screen words have been filled
    @FILL
    0;JMP