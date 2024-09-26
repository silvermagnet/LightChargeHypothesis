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
This is the electron class that generates the proper two light charges for 
generating an electron in code. Currently, this class only works for an 
electron at rest. In the future, it needs to be modified to handle different
positiions and net velocity vectors as initial conditions
'''

import Particle
import LightChargeIdxSingleton
import LightCharge
import BpnMath 
import BigPreciseNum


#TODO, this constructor is only valid for an electron at rest

ELECTRON_MASS_STR = "9.1093837015e-31"
REST_VELOCITY_ZERO_STR = "0.0"

class Electron(Particle.Particle):
    lightCharges = None
    
    electron_period = None
    
    def __init__(self, bpnMath):#, position, velocity, direction, lightChargeSingleton):
        
        self.lightCharges = []
        
        indexGetter = LightChargeIdxSingleton.LightChargeIdxSingleton()

        
        electron_mass = BigPreciseNum.BigPreciseNum(ELECTRON_MASS_STR)

        #r_o = h/(2 * pi * m * c)
        rest_electron_radius = bpnMath.planck_constant / (electron_mass * bpnMath.speed_of_light * bpnMath.two * bpnMath.pi)
        electron_circumference = rest_electron_radius * bpnMath.two * bpnMath.pi 
        self.electron_period = electron_circumference / bpnMath.speed_of_light
        
        net_velocity = BigPreciseNum.BigPreciseNum(REST_VELOCITY_ZERO_STR)
        net_velocity *= net_velocity
        net_velocity /= BigPreciseNum.BigPreciseNum(bpnMath.speed_of_light)
        net_velocity /= BigPreciseNum.BigPreciseNum(bpnMath.speed_of_light)
        
        #r_v = r_o * sqrt(1 - (v^2/c^2))
        electron_radius = rest_electron_radius * bpnMath.sqrt(bpnMath.one - net_velocity)
        
        net_velocity = BigPreciseNum.BigPreciseNum(REST_VELOCITY_ZERO_STR)
        
        #v_c = (1/h) * 2 * pi * planck_length * m * c^3 * sqrt(1/(c^2 - v_net^2))
        velocity = bpnMath.sqrt(bpnMath.one / (bpnMath.speed_of_light * bpnMath.speed_of_light - net_velocity * net_velocity))
        velocity *= (bpnMath.one / bpnMath.planck_constant) * bpnMath.two * bpnMath.pi * bpnMath.planck_length * electron_mass * bpnMath.speed_of_light * bpnMath.speed_of_light * bpnMath.speed_of_light
        

        


        
        self.lightCharges.append(LightCharge.LightCharge([BigPreciseNum.BigPreciseNum(bpnMath.planck_length) / bpnMath.two,
                                            BigPreciseNum.BigPreciseNum(bpnMath.zero), 
                                            BigPreciseNum.BigPreciseNum(electron_radius), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.zero)], 
                                          BigPreciseNum.BigPreciseNum(velocity), 
                                          [BigPreciseNum.BigPreciseNum(bpnMath.negOne) * BigPreciseNum.BigPreciseNum(bpnMath.planck_length), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.zero), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.zero), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.zero)], 
                                          True, indexGetter.getCurrentIdx(), 'r', 
                                          [BigPreciseNum.BigPreciseNum(bpnMath.zero), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.one * BigPreciseNum.BigPreciseNum(bpnMath.planck_length)), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.zero), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.zero)]))
                            
        self.lightCharges.append(LightCharge.LightCharge([BigPreciseNum.BigPreciseNum(bpnMath.negOne) * BigPreciseNum.BigPreciseNum(bpnMath.planck_length) / bpnMath.two,
                                           BigPreciseNum.BigPreciseNum(bpnMath.zero), 
                                           BigPreciseNum.BigPreciseNum(bpnMath.negOne) * BigPreciseNum.BigPreciseNum(electron_radius), 
                                           BigPreciseNum.BigPreciseNum(bpnMath.zero)], 
                                          BigPreciseNum.BigPreciseNum(velocity), 
                                          [BigPreciseNum.BigPreciseNum(bpnMath.one) *BigPreciseNum.BigPreciseNum(bpnMath.planck_length), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.zero), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.zero), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.zero)], 
                                          False, indexGetter.getCurrentIdx(), 'b', 
                                          [BigPreciseNum.BigPreciseNum(bpnMath.zero), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.negOne) *BigPreciseNum.BigPreciseNum(bpnMath.planck_length), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.zero), 
                                            BigPreciseNum.BigPreciseNum(bpnMath.zero)]))


        
                            

       

        Particle.Particle.__init__(self, self.lightCharges)

       
        
        

        


        
