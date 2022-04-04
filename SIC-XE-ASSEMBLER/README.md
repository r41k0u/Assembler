# SIC-XE Assembler


Multipass assembler written in C++ for SIC-XE ISA.


First pass populates the symbol table, assigns the addresses and gives and intermediate assembly code.


The next pass generates the object code, the error file (if any)


To run, enter `g++ -std=c++11 pass2.cpp -o ./asm.obj` in the terminal of cwd.


Then run `./asm.obj` which is the binary created by the code (the actual assembler)


Submission for Tutorial 8 of CSN-252


Pragyansh Chaturvedi

O3 CSE

20115089