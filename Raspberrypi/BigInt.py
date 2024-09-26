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
    BigInt takes an integer and converts it to a hex array if the number is not
    already a hex array. Operations are forwarded to the calculator class which
    effectively encapsulates the alchitry au+ fpga's emulated functionality.
'''
import Calculator
import time
import sys




class BigInt:
    
    BASE_TWO = 2
    BASE_TEN = 10
    BASE_HEX = 16
    
    NUM_BITS_IN_BYTE = 8
    
    BINARY_STR_ONE = "1"
    BINARY_STR_ZERO = "0"
    DECIMAL_STR_ZERO = "0"
    HEX_STR_ZERO = "0"
    
    MIN_HEX_STR_MIN_LOWER = 'a'
    MIN_HEX_STR_MAX_LOWER = 'f'
    MIN_HEX_STR_MIN_UPPER = 'A'
    MIN_HEX_STR_MAX_UPPER = 'F'
    
    hexArr = []
    calculator = None
    
    
    

    #if the number is a string, assume it is a string containing a decimal 
    #integer, otherwise, assume that the number is already hex array and copy
    def __init__(self, number):
        self.hexArr = []
        if(self.calculator is None):
            self.calculator = Calculator.Calculator()
        
        #convert to hex array
        if(isinstance(number, str)):
            binaryStr = ""

            while(len(number) > 0 and number != self.DECIMAL_STR_ZERO):
                
                if(int(number[len(number) - 1]) % self.BASE_TWO):
                    binaryStr += self.BINARY_STR_ONE
                else:
                    binaryStr += self.BINARY_STR_ZERO
                
                number, remainder = self.getLongDivision(number, self.BASE_TWO, self.BASE_TEN)

            while(len(binaryStr) < (self.calculator.OPERAND_LENGTH * self.NUM_BITS_IN_BYTE)):
                binaryStr += self.BINARY_STR_ZERO
                
            #reverse string
            binaryStr = binaryStr[::-1]
            
            
            
            for i in range(0, (self.calculator.OPERAND_LENGTH * self.NUM_BITS_IN_BYTE), self.NUM_BITS_IN_BYTE):
                byte = int(binaryStr[i: (i + self.NUM_BITS_IN_BYTE)], self.BASE_TWO)
                self.hexArr.append(byte)
        elif(isinstance(number, list)):
            #deep copy the given hex array
            self.hexArr = []
            for elem in number:
                self.hexArr.append(elem)
        else:
            #deep copy the given hex array
            self.hexArr = []
            for elem in number.hexArr:
                self.hexArr.append(elem)

    def __eq__(self, other):
        opType = self.calculator.OperationType.EQUALS.value
        result = self.calculator.calculate(opType, self.hexArr, other.hexArr)
        if(result != self.calculator.zeroArr):
            return True
        return False
        
    def __lt__(self, other):            
        opType = self.calculator.OperationType.LESS_THAN.value
        result = self.calculator.calculate(opType, self.hexArr, other.hexArr)
        if(result != self.calculator.zeroArr):
            return True
        return False
        
    def __ne__(self, other):
        if(self == other):
            return False
        return True
        
    def __gt__(self, b):
        return b < self
        
    def __ge__(self, other):
        lt = self < other
        if(lt == True):
            return False
        return True
        
    def __le__(self, other):
        if(self == other):
            return True
        gt = (self > other)
        if(gt == True):
            return False
        return True
        
    def __add__(self, other):
        a = BigInt(self.hexArr)
        a += other
        return a
        
    def __iadd__(self, other):
        a = self
        b = other

        opType = self.calculator.OperationType.ADDITION.value
        a.hexArr = self.calculator.calculate(opType, a.hexArr, b.hexArr)
        return a
        
    def __isub__(self, other):
        a = self
        b = other
        
        opType = self.calculator.OperationType.SUBTRACTION.value
        a.hexArr = self.calculator.calculate(opType, a.hexArr, b.hexArr)
        return a
        
    def __sub__(self, other):
        a = BigInt(self.hexArr)
        a -= other
        return a
        
    def __mul__(self, other):
        a = BigInt(self.hexArr)
        a *= other
        return a
        
    def __imul__(self, other):
        a = self
        b = other
        opType = self.calculator.OperationType.MULTIPLICATION.value
        a.hexArr = self.calculator.calculate(opType, a.hexArr, b.hexArr)
        return a
    
    def __idiv__(self, other):

        # Create new BigPreciseNum objects
        a = BigInt(self.hexArr)
        b = BigInt(other.hexArr)
        

        # Perform the division directly on the internal numbers
        a /= b
    
    
        return a
    
    def __truediv__(self, other):
        a = []
        for elem in self.hexArr:
            a.append(elem)
            
        b = []
        for elem in other.hexArr:
            b.append(elem)
        # No need to create new variables; modify self in place
        if not isinstance(other, BigInt):
            raise TypeError("Division can only be performed with BigPreciseNum objects")
    

        opType = self.calculator.OperationType.DIVISION.value
        self.hexArr = self.calculator.calculate(opType, a, b)
    
        
        return self
        
        
    def printStr(self):
        outputStr = self.getStr()
        print(outputStr)
        
    def getStr(self):
        
        hexStr = ""
        output = ""
        for i in range(0, self.calculator.OPERAND_LENGTH):
            if(self.hexArr[i] < self.BASE_HEX):
                hexStr += self.HEX_STR_ZERO
            hexStr += (f'{self.hexArr[i]:x}')
            
        while(hexStr != self.HEX_STR_ZERO):
            remainder = 0
            hexStr, remainder = self.getLongDivision(hexStr, self.BASE_TEN, self.BASE_HEX)
            output += str(remainder)
            
        #reverse string
        output = output[::-1]
        return output
        
    '''
    dividendStr: must be a hex or decimal string
    divider: must be decimal number
    base: the base of the dividend string
    quotient: returns a hex string if the dividend is in hex, 
        otherwise it returns a decimal string
    '''
    def getLongDivision(self, dividendStr, divider, base):
        output = ""
        i = 0
        digit = 0
        carryover = 0
        
        while(i < len(dividendStr)):
            num = dividendStr[i]
            if(num >= self.MIN_HEX_STR_MIN_LOWER and num <= self.MIN_HEX_STR_MAX_LOWER):
                digit = self.BASE_TEN + (ord(num) - ord(self.MIN_HEX_STR_MIN_LOWER))
            elif(num >= self.MIN_HEX_STR_MIN_UPPER and num <= self.MIN_HEX_STR_MAX_UPPER):
                digit = self.BASE_TEN + (ord(num) - ord(self.MIN_HEX_STR_MIN_UPPER))
            else:
                digit = int(num)
                
            digit += carryover
            
            multipleOfDivider = 0
            while(multipleOfDivider * divider <= digit):
                multipleOfDivider += 1
            
            if((multipleOfDivider - 1) >= 0):
                if((multipleOfDivider - 1) < self.BASE_TEN):
                    output += str(multipleOfDivider - 1) 
                else:
                    output += chr((multipleOfDivider - 1) - self.BASE_TEN + ord(self.MIN_HEX_STR_MIN_UPPER))
            
            remainder = (digit - ((multipleOfDivider - 1) * divider))
            carryover = base * remainder
            i += 1
            
        #get rid of leading zeros
        quotient = ""
        hasHitFirstNonZeroDigit = False
        for i in range(0, len(output)):
            if(hasHitFirstNonZeroDigit == True or output[i] != self.HEX_STR_ZERO):
                quotient += output[i]
            
            if(hasHitFirstNonZeroDigit == False and output[i] != self.HEX_STR_ZERO):
                hasHitFirstNonZeroDigit = True
            
            
        if(len(quotient) == 0):
            quotient = self.HEX_STR_ZERO
        return quotient, remainder
        
            

    
        
        
        
        


'''
def NthFibonacci(n, zero, one):
    a = BigInt(one.hexArr)
    b = BigInt(one.hexArr)
    c = BigInt(zero.hexArr)
    
    if(n <= 0):
        return c
    n -= 1
    while(n > 0):
        c = a + b
        b = a
        a = c
        
        n -= 1
    return b


def NthCatalan(n, zero, one):
    a = BigInt(one.hexArr)
    b = BigInt(zero.hexArr)
    iBigInt = BigInt(one.hexArr)
    iBigInt += one
    
    for i in range(2, (n + 1)):
        a *= iBigInt
        iBigInt += one
        
    midPt = BigInt(iBigInt.hexArr)
    
    b.hexArr = a.hexArr
    for i in range((n + 1), ((2 * n) + 1)):
        b *= iBigInt
        iBigInt += one
    a *= a
    a *= (midPt)
    b /= a
    return b


    
def NthFactorial(n, one):
    f = BigInt(one.hexArr)
    iBigInt = BigInt(one.hexArr)
    iBigInt += one
    
    for i in range(2, (n + 1)):
        f *= iBigInt
        iBigInt += one
        
    return f



one = BigInt("1")
zero = BigInt("0")


start = time.time()

for i in range(0, 101):
    print("fib")
    print(str(i))
    result = NthFibonacci(i, zero, one)
    result.printStr()
end = time.time()
print(end - start)
result.printStr()

start = time.time()
for i in range(0, 101):
    print("fact")
    print(str(i))
    result = NthFactorial(i, one)
    result.printStr()
end = time.time()
print(end - start)
result.printStr()



start = time.time()
for i in range(0, 101):
    print("catalan")
    print(str(i))
    result = NthCatalan(i, zero, one)
    result.printStr()
end = time.time()
print(end - start)
result.printStr()


'''