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
BpnMath is stripped down version of what would be the python math library for
BigPreciseNum types. 
'''
import BigPreciseNum
from Singleton import singleton

@singleton
class BpnMath():

        
    #sin consts
    pi = None
    one_hundred_eighty = None
    negOne = None
    precision = None
    one = None
    zero = None
    two = None
    
    #scientific constants
    speed_of_light = None
    planck_length = None
    planck_time = None
    electric_permittivity = None
    coulumb_constant = None
    resistance_of_space = None
    vacuum_permeability = None
    planck_constant = None

    
    def __init__(self):
        
        
        #160 decimal places since BigPreciseNum.DECIMAL_POINT_LOCATION is 160 
        self.pi = BigPreciseNum.BigPreciseNum("3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502")

        self.one_hundred_eighty = BigPreciseNum.BigPreciseNum("180.0")
        self.negOne = BigPreciseNum.BigPreciseNum("-1.0")
        self.one = BigPreciseNum.BigPreciseNum("1.0")
        self.zero = BigPreciseNum.BigPreciseNum("0.0")
        self.two = BigPreciseNum.BigPreciseNum("2.0")
        self.three = BigPreciseNum.BigPreciseNum("3.0")
        self.ten = BigPreciseNum.BigPreciseNum("10.0")
        self.piOverTwo = self.pi / self.two

        #while calculating terms for the trig function series, new terms are 
        #found until they are smaller than this precision. Roughly based off of
        #BigPreciseNum.DECIMAL_POINT_LOCATION = 160
        self.precision = BigPreciseNum.BigPreciseNum("1e-150")
        
        #This value is used for the trig functions. Sometimes, due to a lack of
        #precision in register calculations, values can obtain a value of 
        #something like 1.0000001 even though the maximum range or domain for 
        #the trig function is [-1, 1]. This value is meant to give a little 
        #leniency and assume the functions have drifted slightly above or below
        #their true range or domain. Roughly based off of 
        #BigPreciseNum.DECIMAL_POINT_LOCATION = 160
        self.trig_precision = BigPreciseNum.BigPreciseNum("1e-150")
        
        #The sqrt function squares numbers, so the max number must be the 
        #number of digits divided by 2. Specifically, 
        #(BigPreciseNum.NUM_DIGITS - BigPreciseNum.DECIMAL_POINT_LOCATION)/2 = 
        #100, however, out of an abundance of caution, the number is 70
        #instead of 100
        self.maxNumForSqrt = BigPreciseNum.BigPreciseNum("1e70") 
        
        self.speed_of_light = BigPreciseNum.BigPreciseNum("299792458")
        self.planck_length = BigPreciseNum.BigPreciseNum("1.616255e-35")
        self.electric_permittivity = BigPreciseNum.BigPreciseNum("8.8541878128e-12")
        self.vacuum_permeability = BigPreciseNum.BigPreciseNum("1.25663706212e-6")
        self.planck_constant = BigPreciseNum.BigPreciseNum("6.62607015e-34")
        
        #https://en.wikipedia.org/wiki/Coulomb_constant
        self.coulumb_constant = BigPreciseNum.BigPreciseNum("1.0") / (BigPreciseNum.BigPreciseNum("4.0") * self.pi * self.electric_permittivity)
        
        


    '''
    Some vectors can be quite small, like [0, 0, planck_length, 0]. By scaling
    them to unity first, less precision is lost during calculations like
    getAngleBetweenVectors
    
    '''
    def scaleVectorAboveOne(self, vector):
        vectorCpy = []
        
        if(self.getMagnitude(vector) == self.zero):
            raise Exception("can't scale zero above one")
            exit
            
        allComponentsBelowOne = True
        for i in range(0, len(vector)):
            if(vector[i] >= self.one):
                return vector
            vectorCpy.append(BigPreciseNum.BigPreciseNum(vector[i]))
            
        
        while(allComponentsBelowOne):
            for i in range(0, len(vectorCpy)):
                vectorCpy[i] *= self.ten
            for i in range(0, len(vectorCpy)):
                if(vectorCpy[i].internalNumber >= self.one.internalNumber):
                    allComponentsBelowOne = False
                    
        return vectorCpy
        
        
    
    def getAngleBetweenVectors(self, vector1, vector2):
        
        isEqual = True
        for i in range(0, len(vector1)):
            if(vector1[i] != vector2[i]):
                isEqual = False
                break
        if(isEqual):
            return BigPreciseNum.BigPreciseNum(self.zero)
        
        #scale vectors to be above one before taking magnitude
        vector1 = self.scaleVectorAboveOne(vector1)
        vector2 = self.scaleVectorAboveOne(vector2)
                
        vector1Mag = self.getMagnitude(vector1)
        vector1Norm = []
        for i in range(0, len(vector1)):
            vector1Norm.append(vector1[i] / vector1Mag)
            
        vector2Mag = self.getMagnitude(vector2)
        vector2Norm = []
        for i in range(0, len(vector2)):
            vector2Norm.append(vector2[i] / vector2Mag)
            
        dot_product = BigPreciseNum.BigPreciseNum(self.zero)
        for i in range(0, len(vector1)):
            dot_product += vector1Norm[i] * vector2Norm[i]  
            
        if(dot_product > self.one):
            return BigPreciseNum.BigPreciseNum(self.zero)
        if(dot_product < self.negOne):
            return BigPreciseNum.BigPreciseNum(self.pi)
        return self.arccos(dot_product)
    
    
    
    '''
    This is fairly similar to getAngleBetweenVectors except that it assumes the
    input vectors have been normalized to a magnitude of the planck length. 
    This function is used for speed since getAngleBetweenVectors effectively
    has a for loop where it bumps the magnitude up by a factor of 10 many times.
    '''
    def getAngleBetweenPlanckLengthUnitVectors(self, vector1, vector2):
        
        isEqual = True
        for i in range(0, 4):
            if(vector1[i] != vector2[i]):
                isEqual = False
                break
        if(isEqual):
            return BigPreciseNum.BigPreciseNum(self.zero)
        
        reciprocal_planck_length = self.one / self.planck_length
        vector1Norm = []
        vector2Norm = []
        for i in range(0, len(vector1)):
            vector1Norm.append(vector1[i] * reciprocal_planck_length)
            vector2Norm.append(vector2[i] * reciprocal_planck_length)
        
            
        dot_product = BigPreciseNum.BigPreciseNum(self.zero)
        for i in range(0, len(vector1)):
            dot_product += vector1Norm[i] * vector2Norm[i]  
            

        if(dot_product > self.one):
            return BigPreciseNum.BigPreciseNum(self.zero)
        if(dot_product < self.negOne):
            return BigPreciseNum.BigPreciseNum(self.pi)
        return self.arccos(dot_product)
    

        
    def getNormalizedVector(self, vector):
        length = len(vector)
        magnitude = BigPreciseNum.BigPreciseNum(self.zero)
        for i in range(0, length):
            magnitude += vector[i] * vector[i]

        magnitude = self.sqrt(magnitude)
        
        norm_vector = []
        for i in range(0, length):
            norm_vector.append(vector[i] / magnitude)
        return norm_vector

    def normalizeAndScale(self, vector, scalar):
        magnitude = self.getMagnitude(vector)
        adjustment = scalar / magnitude
        
        vector_cpy = []
        for i in range(0, len(vector)):
            vector_cpy.append(BigPreciseNum.BigPreciseNum(vector[i]))
        
        for i in range(0, len(vector_cpy)):
            vector_cpy[i] *= adjustment
        return vector_cpy

    def getMagnitude(self, vector):
        magnitude = BigPreciseNum.BigPreciseNum(self.zero)
        for i in range(0, len(vector)):
            magnitude += vector[i] * vector[i]
            
        return self.sqrt(magnitude)
        
    def arccos(self, BigPreciseNum):
        return ((self.pi / self.two) - self.arcsin(BigPreciseNum))
    
    #arcsin is found to an accuracy of 150 decimal places. Typically, most 
    #computers store the trig function values to an accuracy of 8 decimal 
    #places via LUT(look up tables) for an execution time of O(1) and then
    #intelligently approximate the remaining decimal places. However, these
    #approximations are close to the true value but still technically incorrect.
    #this project needs this value to be incredibly accurate and precise.
    #
    #this function uses the series expansion and keeps calculating terms until
    #the new term is less than self.precision. If self.precision is 1e-150, 
    #that means arcsin is accurate to 150 places past the decimal place.
    def arcsin(self, bpn):
         if((bpn > (self.one + self.trig_precision)) or (bpn < (self.negOne - self.trig_precision))):
             exceptionStr = str(bpn.getStr())
             exceptionStr += "arcsin called out of range"
             raise Exception(exceptionStr)
             
         
         if(bpn > self.one):
             return BigPreciseNum.BigPreciseNum(self.piOverTwo)
         
         if(bpn < self.negOne):
             return self.negOne * self.piOverTwo
         
             
         zTerm = BigPreciseNum.BigPreciseNum(bpn)
         newTerm = BigPreciseNum.BigPreciseNum(bpn)
         sumBpn = BigPreciseNum.BigPreciseNum(bpn)
         previousTerm = BigPreciseNum.BigPreciseNum(zTerm)

         iteration = BigPreciseNum.BigPreciseNum(self.one)
         

         
         factorialNumeratorIdx = BigPreciseNum.BigPreciseNum(self.one)
         factorialNumerator = BigPreciseNum.BigPreciseNum(self.one)
         
         twoExponentDenominator = BigPreciseNum.BigPreciseNum(self.one)
         
         
         factorialDenominatorIdx = BigPreciseNum.BigPreciseNum(self.one)
         factorialDenominator = BigPreciseNum.BigPreciseNum(self.one)


         oddDenomTerm = BigPreciseNum.BigPreciseNum(self.one)
         
         precision = BigPreciseNum.BigPreciseNum(self.precision)
         

         previousTerm = None
         


         while(newTerm.internalNumber > precision.internalNumber):
             
             if(previousTerm is not None):
                 previousTerm *= BigPreciseNum.BigPreciseNum(self.two)
                 if(newTerm.internalNumber >= previousTerm.internalNumber):

                     break
             
             previousTerm = BigPreciseNum.BigPreciseNum(newTerm)
             
             zTerm *= bpn
             zTerm *= bpn
             
             while(factorialNumeratorIdx <= (iteration * self.two)):
                 factorialNumerator *= factorialNumeratorIdx
                 factorialNumeratorIdx += self.one
             
             numerator = factorialNumerator * zTerm
             
             twoExponentDenominator *= self.two
             
             while(factorialDenominatorIdx <= iteration):
                 factorialDenominator *= factorialDenominatorIdx
                 factorialDenominatorIdx += self.one
        
             denomPiece1 = factorialDenominator * twoExponentDenominator
             denomPiece1 *= denomPiece1
             
             oddDenomTerm += self.two
             
             denominator = denomPiece1 * oddDenomTerm

             newTerm = numerator / denominator

             
             sumBpn += newTerm

             
             iteration += self.one
             
         if(sumBpn > self.piOverTwo):
             sumBpn = BigPreciseNum.BigPreciseNum(self.piOverTwo)
         if(sumBpn < self.negOne * self.piOverTwo):
             sumBpn = BigPreciseNum.BigPreciseNum(self.piOverTwo * self.negOne)
                   
            
         return sumBpn
             
             
         
    def cos(self, bpn):
        return self.sin((self.pi / self.two) - bpn)
    
    #sin is found to an accuracy of 150 decimal places. Typically, most 
    #computers store the trig function values to an accuracy of 8 decimal 
    #places via LUT(look up tables) for an execution time of O(1) and then
    #intelligently approximate the remaining decimal places. However, these
    #approximations are close to the true value but still technically incorrect.
    #this project needs this value to be incredibly accurate and precise.
    #
    #this function uses the series expansion and keeps calculating terms until
    #the new term is less than self.precision. If self.precision is 1e-150, 
    #that means arcsin is accurate to 150 places past the decimal place.
    def sin(self, bpn):
        
         a = BigPreciseNum.BigPreciseNum(bpn)
         
         sumBpn = BigPreciseNum.BigPreciseNum(a)
         newTerm = BigPreciseNum.BigPreciseNum(a)
         
         denominator = BigPreciseNum.BigPreciseNum(self.one)
         oneTerm = BigPreciseNum.BigPreciseNum(self.one)
         counter = BigPreciseNum.BigPreciseNum(self.one)

         
         numerator = BigPreciseNum.BigPreciseNum(a)
         precision = BigPreciseNum.BigPreciseNum(self.precision)
         
         previousTerm = None

         while(newTerm.internalNumber > precision.internalNumber):
             
             if(previousTerm is not None):
                 previousTerm *= BigPreciseNum.BigPreciseNum(self.two)
                 if(newTerm.internalNumber >= previousTerm.internalNumber):
                     break
             
             previousTerm = BigPreciseNum.BigPreciseNum(newTerm)
             numerator *= a
             numerator *= a
             

             counter += self.one
             denominator *= counter
             counter += self.one
             denominator *= counter


             oneTerm *= self.negOne
             newTerm = (oneTerm * numerator) / denominator

             sumBpn += newTerm

             
             
         
         if(sumBpn > self.one):
             sumBpn = BigPreciseNum.BigPreciseNum(self.one)
         if(sumBpn < self.negOne):
             sumBpn = BigPreciseNum.BigPreciseNum(self.negOne)
              
         return sumBpn
     
    #binary search for sqrt
    def sqrt(self, bpn):

        if(bpn > self.maxNumForSqrt):
            raise Exception("number too large to take sqrt " + bpn.getStr())

        if(bpn == self.one):
            return BigPreciseNum.BigPreciseNum(self.one)
        minimum = BigPreciseNum.BigPreciseNum(self.zero)
        maximum = BigPreciseNum.BigPreciseNum(bpn)
        if(maximum < self.one):
            maximum = BigPreciseNum.BigPreciseNum(self.one)
        middle = BigPreciseNum.BigPreciseNum(self.precision)
        prevMiddle = None
        
        diff = (middle * middle) - bpn
        while(diff.internalNumber > self.precision.internalNumber):

            middle = (minimum + maximum) / self.two
            
            if prevMiddle is not None and prevMiddle == middle:
                return middle
            prevMiddle = middle
            
            squareValue = middle * middle
            
            if(squareValue == bpn):
                return middle
            
            if(squareValue > bpn):
                maximum = middle
            else:
                minimum = middle

            diff = (middle * middle) - bpn
            
        return middle
