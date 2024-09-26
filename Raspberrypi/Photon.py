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
The photon particle class generates the light charges necessary to construct
a photon. There are 2 light charges needed for a photon 
to propagate in a forward helix. In order to calculate the velocity of the
light charges it is necessary to use the equation 
2 * pi * planck_length * f = v_c.
'''
import Particle
import LightChargeIdxSingleton
import LightCharge
#import BpnMath

#PHOTON
#period = dt * total_iterations
#period = (planck_time / 100 ) * total_iterations
#period = (planck_time / 100 ) * 100000000
#period = 5.39 * 10^-38
#frequency = 1/period = 1.855 * 10^37 = 1.855e37
#lambda = c / f = 1.616e-29

#2 * pi * r * f = v
#v = 2 * pi * planck_length * 1.855 * 10^37
#v = 1883.78
#TODO make this work for various photon's of different frequencies and
#orientations
class Photon(Particle.Particle):
    
    lightCharges = []
    
    def __init__(self, bpnGen, bpnMath, log):#position, frequency, direction):
        
        indexGetter = LightChargeIdxSingleton.LightChargeIdxSingleton()
        '''
        if(len(position) != LightCharge.NUM_SPATIAL_DIMENSIONS):
            raise Exception("wrong dimenstions for position")
            
        if(frequency <= bpnMath.zero):
            raise Exception("frequency of photon can't be <= 0")
            
        if(axisOfRotation < 0 or axisOfRotation >= LightCharge.NUM_SPATIAL_DIMENSIONS):
            raise Exception("invalid axis of rotation for photon")
            
        if(len(direction) != LightCharge.NUM_SPATIAL_DIMENSIONS):
                raise Exception("wrong dimenstions for direction")
            
        velocity = bpnMath.two * bpnMath.pi * bpnMath.planck_length * frequency
        
        positive_charge_position = []
        negative_charge_position = []
        for i in range(0, len(position)):
            if(i == axisOfRotation):
                positive_charge_position.append(position[i] + bpnMath.planck_length)
                negative_charge_position.append(position[i] - bpnMath.planck_length)
            else:
                positive_charge_position.append(position[i])
                negative_charge_position.append(position[i])

        '''
        print("about to append light charges")
        self.lightCharges.append(LightCharge.LightCharge([bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.planck_length), 
                       bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.zero)], 
                      bpnGen.getNum("1883.78"), 
                      [bpnGen.getBpnCopy(bpnMath.planck_length), 
                       bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.zero)], 
                      True, indexGetter.getCurrentIdx(), 'r', 
                      [bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.planck_length), 
                       bpnGen.getBpnCopy(bpnMath.zero)], 
                      [bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnMath.negOne * bpnMath.planck_length, 
                       bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.zero)],
                      log))

        self.lightCharges.append(LightCharge.LightCharge([bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.negOne * bpnMath.planck_length), 
                       bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.zero)], 
                      bpnGen.getNum("1883.78"), 
                      [bpnGen.getBpnCopy(bpnMath.negOne * bpnMath.planck_length), 
                       bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.zero)], 
                      False, indexGetter.getCurrentIdx(), 'b', 
                      [bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.planck_length), 
                       bpnGen.getBpnCopy(bpnMath.zero)], 
                      [bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnMath.negOne * bpnMath.planck_length, 
                       bpnGen.getBpnCopy(bpnMath.zero), 
                       bpnGen.getBpnCopy(bpnMath.zero)],
                      log))

        


        Particle.Particle.__init__(self, self.lightCharges)
