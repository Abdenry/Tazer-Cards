/*
* MCP4251 Datasheet: https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/DataSheets/22060b.pdf
*/
#ifndef MCP42XX_H
#define MCP42XX_H

#include <avr/io.h>
#include <stdint.h>
#include <SPI.h>

// Register Addresses as described on P.33 Section 4.2

#define WIPER0ADD   0x00
#define WIPER1ADD   0x01
#define TCONADD     0x04
#define STATUSREG   0x05

// Device Command addresses as described on P.47 Section 7.0

#define CMDWRITE    0x00
#define CMDREAD     0xC
#define CMDINCR     0x04
#define CMDDECR     0x08

void MCP4251init();
void MCP4251writeData(int wiperAddress, uint16_t value);
void MCP4251increment(int wiperAddress);
void MCP4251decrement(int wiperAddress);

#endif