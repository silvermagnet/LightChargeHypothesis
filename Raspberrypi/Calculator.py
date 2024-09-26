# -*- coding: utf-8 -*-
'''
The MIT License (MIT)

Copyright (c) 2024 Julie Marty

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''


'''
This class is meant to interface over SPI with the alchitry au+ fpga using the
spidev library. The fpga emulates an ALU(arithmetic logic unit) which is 
basically a calculator for ints. This python calculator class, encapsulates 
that functionality.
'''

from Singleton import singleton
import spidev
from enum import Enum


@singleton
class Calculator:

    class OperationType(Enum):
        LESS_THAN = 0
        EQUALS = 1
        ADDITION = 2
        SUBTRACTION = 3
        MULTIPLICATION = 4
        DIVISION = 5
        
    #each operand is 1200 bits which translates to 1200 / 8 = 150 bytes
    OPERAND_LENGTH = 150 
    
    

    spi = None
    zeroArr = [0x00] * OPERAND_LENGTH
    
    
    def __init__(self):
        
        bus = 0

        device = 1

        self.spi = spidev.SpiDev()

        self.spi.open(bus, device)

        '''
        acceptable spi speeds for the raspberry pi 2 
        that are compatible with the code
        on the alchitry fpga
        62500000
        31200000
        15600000
        7800000 # selected
        3900000
        1953000
        976000
        488000
        244000
        122000
        61000
        30500
        15200
        7629
        '''
        self.spi.max_speed_hz = 7800000
        self.spi.mode = 3
        
    def __del__(self):
        self.spi.close()
        
    '''
        operation type should be
        0 -> less than
        1 -> equal
        2 -> add
        3 -> subtract
        4 -> multiply
        5 -> divide
        
        operand1 and operand2 should be hex strings
        
        returns, 1 or 0 in a hex string for true or false for 'less than' or
                equal operation types, or a result hex string for the other 
                operation types
    '''              
    def calculate(self, operationType, operand1, operand2):
        if( operationType < 0 or operationType > 5):
            raise Exception("invalid operation type")
        if(len(operand1) != self.OPERAND_LENGTH or len(operand2) != self.OPERAND_LENGTH):
            raise Exception("invalid hex arr size")
        
        #sending the operation type
        to_send = [operationType]

        #sending first operator
        for i in range(len(operand1)):
            to_send.append(operand1[i])
            
        #sending second operator
        for i in range(len(operand2)):
            to_send.append(operand2[i])
            
        #calculation operation, effectively allow time to calculate the result
        #of the calculation
        for i in range(0, self.OPERAND_LENGTH):
            to_send.append(0x00)

        
        #allowing time to write the result back to the device
        for i in range(0, self.OPERAND_LENGTH):
            to_send.append(0x00)
            

        response = self.spi.xfer(to_send)
        output = response[len(response) - self.OPERAND_LENGTH: len(response)]


        return output
        


