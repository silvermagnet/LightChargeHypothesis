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
BigPreciseNum either takes a string like "-1.22343545e-7" and converts it to a BigInt
which is the internalNumber, and a boolean, isPositive, which indicates whether
 the number is positive or negative, or takes a BigPreciseNum and copies the 
BigInt and whether it is positive or negative. Initializing from a string
like "-1.22343545e-7" is computationally expensive and should only be used in
the initialization stage of the program.

BigPreciseNum effectively just takes a BigInt and wraps it with some extra
details like whether it is positive or negative and where the effective
decimal point should be in the number. Additionally, the constructor has the
capability to convert scientific number strings into the correct format.
'''

import Calculator
import BigInt


class BigPreciseNum:
    
    #the 1200 bit alu corresponds to 2^1200 = 1.7 * 10^361, 
    #so we take a slighty smaller number of 360 for easy fitting
    NUM_DIGITS = 360 
    
    #this value is roughly halfway through 360. it's not uncommon for values
    #to be squared in the numerator or denominator because of division. The 
    #value of 160 instead of 180 was used due to trial and error.
    DECIMAL_POINT_LOCATION = 160
    
    #this string is a hex array of what is effectively the one's place.
    #specifically it is the hex representation of 1^DECIMAL_POINT_LOCATION .
    #It may be necessary to use some online tools like 
    #https://www.rapidtables.com/convert/number/decimal-to-hex.html to get the 
    #hex string and then buffer it to 300 places since the operand length 
    #should be 150 bytes and each digit is a nibble. 
    #The value shouldn't change unless the code for the fpga changes, so it
    #seems fine to leave this as a constant for performance.
    ONE_PLACE_HEX_STR = "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000B616A12B7FE617AA577B986B314D60092381CF8591999D6395D7DDC4214135713F2F3B70F28505222D0F4FBC32D810000000000000000000000000000000000000000"
    
    ZERO_STR = "0"
    ONE_STR = "1"
    DECIMAL_POINT_STR = "."
    NEGATIVE_STR = "-"
    EXPONENT_STR = "e"
    BASE_TEN_STR = "10"
    NUM_NIBBLES_IN_BYTE = 2 
    BASE_HEX = 16 
    
    isPositive = True
    internalNumber = None
    decimalNum = None 
    zeroNum = None
    numDigits = None
    decimalPtLocation = None
    calculator = None
    
    
    def __init__(self, bigPreciseNum, numDigits=NUM_DIGITS, \
                 decimalPtLocation=DECIMAL_POINT_LOCATION ):
        
        self.numDigits = numDigits
        self.decimalPtLocation = decimalPtLocation
        self.calculator = Calculator.Calculator()
        self.zeroNum = BigInt.BigInt(self.calculator.zeroArr)
            
        # Split the hex string into pairs and convert them to a hex array
        hex_array = []
        for i in range(0, len(self.ONE_PLACE_HEX_STR), self.NUM_NIBBLES_IN_BYTE):
            hex_array.append(int(self.ONE_PLACE_HEX_STR[i:i + self.NUM_NIBBLES_IN_BYTE], self.BASE_HEX))

        self.decimalNum = BigInt.BigInt(hex_array)

        
        if(isinstance(bigPreciseNum, str)):
            power = self.ZERO_STR
            fraction = ""
            integerPart = ""
            
            if(bigPreciseNum.find(self.EXPONENT_STR) >= 0):
                bigPreciseNum, power = bigPreciseNum.split(self.EXPONENT_STR)
             
            if(bigPreciseNum.find(self.DECIMAL_POINT_STR) >= 0):
                bigPreciseNum, fraction = bigPreciseNum.split(self.DECIMAL_POINT_STR)
                
            integerPart = bigPreciseNum
            if(integerPart.find(self.NEGATIVE_STR) >= 0):
                self.isPositive = False
                negative, integerPart = integerPart.split(self.NEGATIVE_STR)
                
                
            #move the integer to the beginning of the decimal point
            if(len(integerPart) > 0):
                self.internalNumber = BigInt.BigInt(integerPart)
                for i in range(0, self.decimalPtLocation):
                    self.internalNumber *= BigInt.BigInt(self.BASE_TEN_STR)
                    
            #add the fraction part
            if(len(fraction) > self.decimalPtLocation):
                while(len(fraction) > self.decimalPtLocation):
                    fraction = fraction[0:self.decimalPtLocation]
            else:
                while(len(fraction) < self.decimalPtLocation):
                    fraction += self.ZERO_STR
            
            fractionBigInt = BigInt.BigInt(fraction)
            self.internalNumber += fractionBigInt
            
            #multiply the number by the power if any
            ten = BigInt.BigInt(self.BASE_TEN_STR)
            
            

            isPositivePower = True
            if(power.find(self.NEGATIVE_STR) >= 0):
                isPositivePower = False
                negative, power = power.split(self.NEGATIVE_STR)
                
            if(isPositivePower):
                for i in range(0, int(power)):
                    self.internalNumber *= ten
            else:
                for i in range(0, int(power)):
                    self.internalNumber /= ten
        else:
            self.isPositive = bigPreciseNum.isPositive
            self.internalNumber = BigInt.BigInt(bigPreciseNum.internalNumber)
            

        
        
    def getStr(self):
        retStr = ""
        if(False == self.isPositive):
            retStr += self.NEGATIVE_STR
            
        intPartExists = False
        firstNumReached = False
        digits = self.internalNumber.getStr()
        
        #reverse string
        digits = digits[::-1]
        
        #strip leading zeros
        i = len(digits) - 1
        while(i > self.decimalPtLocation - 1):
            if(firstNumReached == True):
                retStr += str(digits[i])
            elif((firstNumReached == False) and (digits[i] != self.ZERO_STR)):
                firstNumReached = True
                retStr += digits[i]
            i -= 1
            intPartExists = True
            
        if(False == intPartExists):
            retStr += self.ZERO_STR
        retStr += "."
        i = self.decimalPtLocation - 1
        while(i >= 0):
            if(i >= len(digits)):
                retStr += self.ZERO_STR
            else:
                retStr += digits[i]
            i -= 1
        
        return retStr
        

    
    def printStr(self):
        print(self.getStr())
        
    def __add__(self, other):
        a = BigPreciseNum(self)
        a += other
        return a
        
    def __iadd__(self, other):
        a = self
        b = other
        
        if(a.isPositive == True and b.isPositive == True):
            a.internalNumber += b.internalNumber
            
        elif(a.isPositive == True and b.isPositive == False):
            if(a.internalNumber > b.internalNumber):
                a.internalNumber -= b.internalNumber
            else:
                a.isPositive = False
                a.internalNumber = b.internalNumber - a.internalNumber
        
        elif(a.isPositive == False and b.isPositive == True):
            if(a.internalNumber > b.internalNumber):
                a.internalNumber -= b.internalNumber
            else:
                a.isPositive = True
                a.internalNumber = b.internalNumber - a.internalNumber
            
        else:
            a.internalNumber += b.internalNumber
            
            
        return a
    
    def __sub__(self, other):
        a = BigPreciseNum(self)
        a -= other
        return a
    
    def __isub__(self, other):
        a = self 
        b = other
        
        if(a.isPositive == True and b.isPositive == True):
            if(a.internalNumber > b.internalNumber):
                a.internalNumber -= b.internalNumber
            else:
                a.isPositive = False
                a.internalNumber = b.internalNumber - a.internalNumber
                
        elif(a.isPositive == True and b.isPositive == False):
            a.internalNumber += b.internalNumber
            
        elif(a.isPositive == False and b.isPositive == True):
            a.internalNumber += b.internalNumber
            
        else:
            if(a.internalNumber > b.internalNumber):
                a.internalNumber -= b.internalNumber
            else:
                a.isPositive = True
                a.internalNumber = b.internalNumber - a.internalNumber
        

        
        return a
    
    def __mul__(self, other):
        a = BigPreciseNum(self)
        a *= other
        return a
    
    def __imul__(self, other):
        a = self 
        b = other
        
        if(a.isPositive == False and b.isPositive == False):
            a.isPositive = True
        elif(a.isPositive == True and b.isPositive == False):
            a.isPositive = False


        a.internalNumber *= b.internalNumber 

        a.internalNumber /= self.decimalNum

        

        
        return a
    
    def __idiv__(self, other):

        # Create new BigPreciseNum objects
        a = self
        b = BigPreciseNum(other)
        

        # Perform the division directly on the internal numbers
        a /= b
    
        # Adjust the sign based on the positivity of a and b
        if a.isPositive != b.isPositive:
            a.isPositive = False
        else:
            a.isPositive = True
    
        return a
    def __truediv__(self, other):

        # Create new BigPreciseNum objects
        a = BigPreciseNum(self)
        b = BigPreciseNum(other)
        
        # No need to create new variables; modify self in place
        if not isinstance(other, BigPreciseNum):
            raise TypeError("Division can only be performed with BigPreciseNum objects")
    
        # Modify self based on the positivity rules
        if a.isPositive != b.isPositive:
            a.isPositive = False
        else:
            a.isPositive = True
    
        a.internalNumber *= b.decimalNum
        # Perform in-place division
        a.internalNumber /= b.internalNumber
        
        return a


        
        
    
    def __lt__(self, b):
        a = BigPreciseNum(self)
        
        if(a.isPositive == True and b.isPositive == True):
            return a.internalNumber < b.internalNumber
        elif(a.isPositive == True and b.isPositive == False):
            return False
        elif(a.isPositive == False and b.isPositive == True):
            return True
        else:
            return a.internalNumber > b.internalNumber
        
        raise Exception("error with less than operator")
        
    def __eq__(self, b):
        a = BigPreciseNum(self)
        return ((a.internalNumber == b.internalNumber) and (a.isPositive == b.isPositive))

    def __ne__(self, b):
        return not(self == b)  
    
    def __gt__(self, b):
        return b < self
    
    def __ge__(self, b):
        return not(self < b)
    
    def __le__(self, b):
        return not(self > b)
     


