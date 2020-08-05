// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
// i=R1
// mul=0
// while i>0:
//     mul=mul+R1
//     i--
// store mul in R0

    @R1
    D=M
    @i
    M=D
    @mul
    M=0
(LOOP)
    @i
    D=M
    @STORE
    D;JEQ
    @i
    M=M-1
    @R0
    D=M
    @mul
    M=M+D
    @LOOP
    0;JMP

(STORE)
    @mul
    D=M
    @R2
    M=D
(END)
    @END
    0;JMP
