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
This is the light charge simulator class. Light charges are accumulated in the
initialization stage by getting the light charges from electron or photon
structures. Thereafter, the light charges are updated at each delta time 
against every other light charge in the system since this hypothesis is 
strictly non-local. The delta time, dt, variable should be made as small as is
reasonably possible since ideally the limit of dt should go to zero.

In terms of setup, you typically want to setup the initial system in terms of
particles, get the light charges from the particles, and then run the 
simulation. It is important to note that new variables should only be 
initialized in the beginning since the runtime of initializing something like
BigPreciseNum("1.242424e-8") is rather slow. During runtime, you should
update these variables rather than initialize them.

In terms of usage, you want to run the LightChargeSimulator.py class in order
to generate the positionsOutput.json file and the tdataOutput.json file. 
Thereafter, you can extract the two json files from the raspberry pi via the 
scp command and plot it with the PLotLightCharges.py file. Make sure to alter
the ssh and scp commands and TIME_DATA_LOCATION_STR, POSITION_DATA_LOCATION_STR,and
EXCEPTION_LOCATION_STR variables to match your username and location setup.

    1. send files to raspberry pi with git bash. make sure the username, 
        device name, and final location are corrected for your setup.
        $>  scp BigInt.py BigPreciseNum.py BpnMath.py Calculator.py Electron.py Log.py LightChargeIdxSingleton.py LightCharge.py LightChargeSimulator.py Particle.py Photon.py PlotLightCharges.py Singleton.py silvermagnet2@raspberrypi:/home/silvermagnet2/light

    2. run the program on the raspberry pi through putty or your ssh client
        $> nohup python3 LightChargeSimulator.py &
        $> disown
        
    3. check the process is running in the background in putty
        $> ps aux
        
    4. after the simulation finishes, retrieve the files with git bash
        $> scp silvermagnet2@raspberrypi:/home/silvermagnet2/light/positionsOutput.json positionsOutput.json
        $> scp silvermagnet2@raspberrypi:/home/silvermagnet2/light/tdataOutput.json tdataOutput.json
        
    5. after making sure that the json files are located in the same directory
        as PlotLightCharges.
        $> python3 PlotLightCharges.py

'''

import json
import BigPreciseNum
import BpnMath
import Photon
import Electron
import traceback
import sys
import Log
import LightCharge


TIME_DATA_LOCATION_STR = "/home/silvermagnet2/light/tdataOutput.json"
POSITION_DATA_LOCATION_STR = "/home/silvermagnet2/light/positionsOutput.json"
EXCEPTION_LOCATION_STR = "/home/silvermagnet2/light/exception.txt"



log = Log.Log()
  
bpnMath = BpnMath.BpnMath()


time = BigPreciseNum.BigPreciseNum("0.0")


lightCharges = []


#photon = Photon.Photon(bpn, bpnMath, log)
#lightCharges = photon.addLightCharges(lightCharges)




electron = Electron.Electron(bpnMath)
electron.electron_period.printStr()
lightCharges = electron.addLightCharges(lightCharges)



total_time = BigPreciseNum.BigPreciseNum(electron.electron_period)

#photon time
#total_time = bpn.getNum("5.39e-38")

total_iterations = BigPreciseNum.BigPreciseNum("1000")

dt = total_time / total_iterations

print("total_time is")
total_time.printStr()
print("total_iterations is")
total_iterations.printStr()
print("dt is ")
dt.printStr()




tdata = []

tdata.append(float(time.getStr()))



'''
photon = Photon.Photon(bpn, bpnMath, 
                [bpnMath.zero, bpnMath.zero, bpnMath.zero, bpnMath.zero],
                bpn.getNum("1.855e37"), 
                [bpnMath.zero, bpnMath.zero, bpnMath.planck_length, bpnMath.zero],
                lightChargeIdxCounter, Photon.Y_ROTATION_AXIS)


lightCharges = photon.addLightCharges(lightCharges)
'''

mappedPositions = []
for lightCharge in lightCharges:
    mappedPositions.append([])
    position = []
    for i in range(0, len(lightCharge.position)):
        position.append(float(lightCharge.position[i].getStr()))
    mappedPositions[lightCharge.index].append(position)

i = 0

try:
    #time <= total_time rather than time < total_time so we can analyze results
    #at the beginning of the next cycle
    while(time <= total_time):
    
        i += 1
       
        addPtToGraph = True
        #if(i % ie2 == 0):
        #   addPtToGraph = True
        #else:
        #   addPtToGraph = False
        if(addPtToGraph):
            log.log('.')
            log.log("[current time, total_time]")
            log.log(time.getStr())
            log.log(total_time.getStr())
            addPtToGraph = True
    
        
        nextLightCharges = []
    
        for lightCharge in lightCharges:  
            updatedLightCharge = lightCharge.getUpdatedLightCharge(lightCharges, dt)
            if(addPtToGraph):
                position = []
                for i in range(0, len(updatedLightCharge.position)):
                    position.append(float(updatedLightCharge.position[i].getStr()))
                mappedPositions[updatedLightCharge.index].append(position)
            nextLightCharges.append(updatedLightCharge)

    
    
        for i in range(0, len(lightCharges)):
            lightCharges[i] = nextLightCharges[i]
    
        time += dt

        
    
        if(addPtToGraph):  
            tdata.append(float(time.getStr()))
            
        with open(TIME_DATA_LOCATION_STR, "w") as outfile:
            json.dump(tdata, outfile)
            
            
        with open(POSITION_DATA_LOCATION_STR, "w") as outfile:
            json.dump(mappedPositions, outfile)
        

    
        

except Exception as inst:
    error = ""
    error += str(type(inst))
    error += str(inst.args)
    error += str(inst)
    error += str(traceback.format_exc())
    error += str(sys.exc_info()[2])
    f = open(EXCEPTION_LOCATION_STR, "w")
    f.write(error)
    f.close()


    


