# MIPS Processor Simulator in myHDL

## Overview
This repository contains the hardware design and simulation of a single-cycle MIPS processor architecture. The project was developed using **myHDL**, allowing the digital hardware (datapath and control logic) to be modeled, simulated, and verified entirely within Python.

## Key Features & Architecture
* **Complete Datapath:** Integrates a fully functional Arithmetic Logic Unit (ALU), a 32-register File, Instruction Memory, and Data Memory modules.
* **Custom Control Unit:** Decodes MIPS instructions and generates precise routing signals for multiplexers, write enables, and ALU operations.
* **Memory & Stalling Logic:** Implements basic hazard detection via a stall function to safely handle simultaneous Memory Read/Write operations.
* **Instruction Set Architecture (ISA):** Successfully decodes and executes the following core MIPS instructions:
  * **R-Type:** `ADD`, `SUB`, `AND`, `OR`, `XOR`
  * **I-Type:** `ADDI`, `SUBI`, `LW` (Load Word), `SW` (Store Word), `BEQ` (Branch on Equal)

## Simulation & Verification
The system utilizes myHDL testbenches to simulate clock cycles and verify register state changes. The testbench extracts 32-bit binary machine code from the `instructions2` file, feeds it into the program counter (PC), and logs the exact state of the pipeline (ALU results, zero flags, branch outputs, and mux selections) at each positive clock edge.

### Testbench Execution (`instructions2`)
The default simulation runs the following compiled assembly program to verify the datapath, ALU routing, memory synchronization, and branch logic:
```assembly
ADD  $13, $12, $10
SUB  $15, $13, $13
ADDI $21, $25, 273
BEQ  $18, $18, 2    # Branch evaluation
ADDI $21, $25, 785  # (Repeated to test pipeline continuity)
ADDI $21, $25, 785
ADDI $21, $25, 785
ADDI $21, $25, 785
ADDI $21, $25, 785
ADDI $21, $25, 785
ADDI $21, $25, 785
XOR  $13, $18, $21
XOR  $1,  $8,  $29
SW   $23, 58($22)
