# ReRAM Architectures

Building an MVM (Matrix-Vector Multiplier) computing architecture using 2x2 ReRAM crossbar blocks.  

## 2 x 2 Crossbar Matrix - 2 bit MAC Operations

The basic building block for MVM based ReRAM architectures are 2x2 2-bit Multiplier blocks, which consist of a 2x2 array of crossbar ReRAMs and an ADC (Analog Digital Converter), TIA (Transimpedence Amplifier) and Shift Register at the output of each column, to convert back the analog current output to a digital value. In this project, we will use this 2x2 crossbar as a fundamental blovk to build more complex and higher bit MAC units. 

## 2 x 2 Crossbar Matrix - 4 bit MAC Operations

Using 4 2x2 2-bit MAC blocks, a 2x2 4-bit MAC block can be created. This block requires, 10 shift registers. 8 for the 4 2x2 2-bit blocks and 2 more to hold the final output for the 4-bit MAC. Applying the same logic, a 2x2 8-bit MAC can be built. 

