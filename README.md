In this setup, the raspberry pi 2b is connected to an alchitry au+ fpga over SPI. Specifically, the wires that need to be connected to the raspberry pi 2 are specified in the spi.acf file.


pin sdi B49;
pin sdo B46;
pin cs B40;
pin sck B43;
The wires are twisted in order to prevent crosstalk and there’s a common ground between the boards. There is also an alchitry bromium prototype board on top to access the pinouts. The usb cable from the raspberry pi 2 to the fpga board actually provides the fpga board power. The raspberry pi has its own power cord and is hooked into an ethernet cable so the user can use ssh and scp commands to access files. Additionally, the raspberry pi 2 has to be setup to enable SPI functionality. The setup is fairly standard and available via online tutorials.
It is worth noting, that for anyone who would like to replicate the results, that before any parts are ordered, one should try to get a software license from alchitry to check that one can obtain it due to the recent regulations about the chips act. Additionally, at the time I downloaded the license, it was free. It may now require a business license because it has new ML functionality. If people are interested in replication, I would consider revising the setup to work with an alchitry Cu which is cheaper and may not require an expensive license. Appendix C has the raspberry pi 2 python files, and Appendix D has the files required to emulate an ALU on the alchitry au+ fpga. Appendix E has the simulation results of positionsOutput.json and tdataOutput.json.
Appendix B - analysis and future directions
In the simulation output of positionsOutput.json, the very first and very last values should be equal to each other since they both are the first values during the cycle. In practice, these values of [] and [] differ ever so slightly. There are some limitations of the simulation, namely some precision is lost during the register operations, and the delta time value, dt, can not actually go to zero in the simulation. Regardless, I found the simulation results to be as good as could be expected.
In the future, in order to keep the runtime down, I may try to modify the system to have a great number of ALUs such that during runtime, there would be an ALU per light charge that could be accessed sequentially. Rather than simply having an op code for the calculation, there would additionally be a light charge ALU index per calculation such that there would effectively be one light charge per ALU. Some sort of handling would have to be added such that the ALUs would run in parallel. Since the code is effectively running such that each light charge has to calculate the net effects of all the other light charges at every delta time, this would cause a large speedup. Obviously this would limit the number of light charges in the simulation. However, there’s only 2 light charges in a photon, 2 light charges in an electron, and if the Robinson models are correct, about 14 charges for a proton. 
Other ways to improve runtime are considered. Although an obvious step would be to get the emulated ALU fabricated into an actual chip, this process is expensive and unlikely to happen. Another approach might include using higher quality but shorter wires which would allow one to use one of the higher speeds specified in Calculator.py. It would be worth double checking the accuracy of the operations at higher speeds since SPI transactions are not guaranteed to be correct unlike slower UART transactions. However, the simulations have been checked against fibonacci, catalan, and factorial tests with no loss of accuracy at the lower speed, and this isn’t a critical piece of code working for a heart monitor that must never fail.
Another alternative route would be to get access to a supercomputer to use the standard BigInt.cpp class with a proper wrapper for decimal numbers to calculate sin(theta) and arcsin(theta) to an accuracy of a hundred digits past the decimal point. On most computers, the cost of calculating sin(theta) is usually O(1). However, these values are only accurate to 8 digits past the decimal point and are saved on internal LUTs(Look up tables). Any ‘precision’ past this point in code is usually just intelligent approximations that aren’t technically accurate. If these values were pre-calculated and stored in a database or a simple file, the code wouldn’t need the fpga to run at all. This option should make it possible to simply run the modified simulation python files on a standard computer which would make the setup much more accessible to most physicists. However, getting access to a supercomputer is also both unlikely and expensive.

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