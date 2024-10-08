#include "MCP4251.h"

// PB2 is digital IO pin 10 (CS) on the Arduino Uno as labelled on the pinout sheet. Change as necessary.

void MCP4251init(){
    DDRB |= (1<<2);
    PORTB |= (1<<2);
    SPI.begin();
}

// Increments the chosen wiper by 1
void MCP4251increment(int wiperAddress){
    uint8_t commandByte = 0;
    
    if(wiperAddress == WIPER0ADD){
        commandByte = CMDINCR;
        PORTB &= ~(1<<2);
        SPI.transfer(commandByte);
        PORTB |= (1<<2);
    }else if(wiperAddress == WIPER1ADD){
        commandByte = (WIPER1ADD << 4) | CMDINCR;
        PORTB &= ~(1<<2);
        SPI.transfer(commandByte);
        PORTB |= (1<<2);
    }
}

// Decrements the chosen wiper by 1
void MCP4251decrement(int wiperAddress){
    uint8_t commandByte = 0;
    
    if(wiperAddress == WIPER0ADD){
        commandByte = CMDDECR;
        PORTB &= ~(1<<2);
        SPI.transfer(commandByte);
        PORTB |= (1<<2);
    }else if(wiperAddress == WIPER1ADD){
        commandByte = (WIPER1ADD << 4) | CMDDECR;
        PORTB &= ~(1<<2);
        SPI.transfer(commandByte);
        PORTB |= (1<<2);
    }
}

// Sets the wiper to a postion from 0 to 257
void MCP4251writeData(int wiperAddress, uint16_t value){
    uint8_t commandByte = 0;
    uint8_t dataByte = 0;

    if(value > 255){
        commandByte |= 1;
        dataByte = value & 0xFF;
    }else{
        dataByte = value;
    }

    if(wiperAddress == WIPER0ADD){
        PORTB &= ~(1<<2);
        SPI.transfer(commandByte);
        SPI.transfer(dataByte);
        PORTB |= (1<<2);
    }else if(wiperAddress == WIPER1ADD){
        commandByte |= (WIPER1ADD << 4);
        PORTB &= ~(1<<2);
        SPI.transfer(commandByte);
        SPI.transfer(dataByte);
        PORTB |= (1<<2);
    }
}