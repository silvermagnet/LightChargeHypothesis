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
LightCharge is the key class of the simulation. It has a single charge, which
is close to the planck charge. It also has two velocity vectors. The c velocity
vector maintains a constant magnitude of c, but swivels. The variable velocity
vector changes its magnitude, however the nature of this change is as of yet
undetermined. It also swivels its direction. It is worth noting that these two
vectors swivel without being tied or locked to each other as was previously
considered. When updating its internal characteristics at each delta time, dt,
it needs to know the information of all the other light charges. This hypothesis
is explicitely non-local.
'''
import BigPreciseNum
import BpnMath
import Log





bpnMath = BpnMath.BpnMath()


#light_charge_value = (bpnMath.electric_permittivity * bpnMath.planck_constant * bpnMath.speed_of_light)
#light_charge_value = bpnMath.sqrt(light_charge_value)
        
electron_mass = BigPreciseNum.BigPreciseNum("9.1093837015e-31")
electron_radius = bpnMath.planck_constant / (electron_mass * bpnMath.speed_of_light * bpnMath.two * bpnMath.pi)

electron_circumference = electron_radius * bpnMath.two * bpnMath.pi 
electron_period = electron_circumference / bpnMath.speed_of_light


        



class LightCharge:
   
    log = None
    
    position = None
    velocity = None
    velocity_direction_unit_vector = None
    positive_charge = None
    index = None
    map_color_str = None
    c_direction_unit_vector = None 
    charge = None
    
    
    
    
    def __init__(self, position, velocity, velocity_direction_unit_vector,
                 positive_charge, index, map_color_str,
                 c_direction_unit_vector):
       
        self.log = Log.Log()
        
        self.position = self.copyVector(position)
        
        self.velocity = BigPreciseNum.BigPreciseNum(velocity)
        
        self.velocity_direction_unit_vector = self.copyVector(velocity_direction_unit_vector)
        
        self.positive_charge = positive_charge
        
        self.index = index
        
        self.map_color_str = map_color_str
       
        self.c_direction_unit_vector = self.copyVector(c_direction_unit_vector) 
        
        self.charge = (bpnMath.electric_permittivity * bpnMath.planck_constant * bpnMath.speed_of_light)
        self.charge = bpnMath.sqrt(self.charge)
        

    def copyVector(self, vector):
        copiedVector = []
        for i in range(0, len(vector)):
            copiedVector.append(BigPreciseNum.BigPreciseNum(vector[i]))
        return copiedVector
            
    def printVector(self, vector):
        output = "["
        
        for bpn in vector:
            output += bpn.getStr()
            output += " "
            
        output += "]"
        self.log.log(output)
        print(output)
        
    def getDistanceBtwnPoints(self, P1, P2):
        p = self.copyVector(P1)
        q = self.copyVector(P2)
        
        if(len(p) != len(q)):
            raise Exception("invalid position vectors")
            exit()
            
            
        sumElements = BigPreciseNum.BigPreciseNum(bpnMath.zero)
        for i in range(0, len(p)):
            sumElements += ((p[i] - q[i]) * (p[i] - q[i]))

        val = bpnMath.sqrt(sumElements)
        return val
        
    def getCopy(self, lightCharge):
        
        newPosition = self.copyVector(lightCharge.position)
        newVelVector = self.copyVector(lightCharge.velocity_direction_unit_vector)
        newCVector = self.copyVector(lightCharge.c_direction_unit_vector)
            
        return LightCharge(newPosition, BigPreciseNum.BigPreciseNum(lightCharge.velocity), newVelVector,
                      lightCharge.positive_charge, lightCharge.index, lightCharge.map_color_str,
                      newCVector)
     
    

    
    def getDistanceBtwnLightCharges(self, lightCharge):
        p = self.copyVector(self.position)
        q = self.copyVector(lightCharge.position)
        
        return self.getDistanceBtwnPoints(p, q)
        

       

    

    #get delta phi for c vector
    #TODO currently assumes all light charges attract even though like charges 
    #should repel
    def getDeltaPhi2(self, dt, lightCharge):
            
        r = self.getDistanceBtwnLightCharges(lightCharge)        

        theta = bpnMath.getAngleBetweenPlanckLengthUnitVectors(lightCharge.c_direction_unit_vector, self.c_direction_unit_vector)
        sinTheta = bpnMath.sin(theta / bpnMath.two)

        phi = bpnMath.speed_of_light * (bpnMath.two / r) * dt * sinTheta


        return phi
    
    #delta phi for variable velocity vector
    #TODO currently assumes all light charges attract even though like charges 
    #should repel
    def getDeltaPhi1(self, dt, lightCharge):

        r = self.getDistanceBtwnLightCharges(lightCharge)

        theta = bpnMath.getAngleBetweenPlanckLengthUnitVectors(lightCharge.velocity_direction_unit_vector, self.velocity_direction_unit_vector)
        sinTheta = bpnMath.sin(theta / bpnMath.two)

        phi = lightCharge.velocity * (bpnMath.two / r) * dt * sinTheta

        return phi 
    
    def getRotatedVector(self, P0, P1, P2, phi):

        

        '''a, b, and c represent the sides of the triangle created in 2d space
        from the significant points between the light charges determined via
        vector magnitudes'''
        #a = self.getDistanceBtwnPoints(P1, P0)
        b = self.getDistanceBtwnPoints(P1, P2)
        #c = self.getDistanceBtwnPoints(P0, P2)
       


        v1 = []
        for i in range(len(P0)):
            v1.append(P0[i] - P2[i])
        v2 = []
        for i in range(len(P1)):
            v2.append(P1[i] - P2[i])
        try:
            angleBtwnV0andV1 = bpnMath.getAngleBetweenVectors(v1, v2)
        except:
            angleBtwnV0andV1 = BigPreciseNum.BigPreciseNum(bpnMath.zero)
        
        if(angleBtwnV0andV1 == bpnMath.zero):
            return v1


        '''
        map the 4d coords to 2d coord unit circle. P0 is always (0,1), and
        then we use the magnitudes of the vectors between P0, P1, and P2  and
        geometry to determine how to map the other points
        '''
        if(angleBtwnV0andV1 <= (bpnMath.pi / bpnMath.two)):
            x_P1 = b*bpnMath.cos(angleBtwnV0andV1)
            y_P1 = b*bpnMath.sin(angleBtwnV0andV1)
           
        elif(angleBtwnV0andV1 <= bpnMath.pi):
            x_P1 = bpnMath.negOne * b*bpnMath.cos(bpnMath.pi - angleBtwnV0andV1)
            y_P1 = b*bpnMath.sin(bpnMath.pi - angleBtwnV0andV1)

        elif(angleBtwnV0andV1 <= (bpnMath.three * (bpnMath.pi / bpnMath.two))):
            x_P1 = bpnMath.negOne * b*bpnMath.sin((bpnMath.three * (bpnMath.pi /bpnMath.two)) - angleBtwnV0andV1)
            y_P1 = bpnMath.negOne * b*bpnMath.cos((bpnMath.three * (bpnMath.pi /bpnMath.two)) - angleBtwnV0andV1)
        else:
            x_P1 = b*bpnMath.cos((bpnMath.two * bpnMath.pi) - angleBtwnV0andV1)
            y_P1 = bpnMath.negOne * b*bpnMath.sin((bpnMath.two * bpnMath.pi) - angleBtwnV0andV1)
            

                  
        '''
        find the rotated vector when rotated by phi
        '''
        '''
        https://en.wikipedia.org/wiki/Rotation_matrix
        the velocity unit vector for this light charge is being mapped by the
        rotation matrix as [1,0] for [u,x]. Therefore, we can use the 2d
        rotation matrix to rotate the vector
        '''

        V3 = [bpnMath.cos(phi), bpnMath.negOne * bpnMath.sin(phi)]

        x_P0 = BigPreciseNum.BigPreciseNum(bpnMath.planck_length)
        y_P0 = BigPreciseNum.BigPreciseNum(bpnMath.zero)
        m1 = ((y_P0 - y_P1) / (x_P0 - x_P1))
        b1 = y_P0 - (m1 * x_P0)
        m2 = (V3[1])/(V3[0])

        
        x_P4 = (bpnMath.zero - b1)/(m1 - m2)
        y_P4 = m2 * x_P4
       
        P0_2d = [x_P0, y_P0]
        P4 = [x_P4, y_P4]
        
        d = None 

        try:
            d = self.getDistanceBtwnPoints(P0_2d, P4)
        except:
            d = BigPreciseNum.BigPreciseNum(bpnMath.zero)


        '''
        now that we know the distance btwn P0 and P1, we can take the 4d vector
        from P0 to P1, normalize it, and scale/multiply by d to get P4
        '''

        direction_vector_btwn_P0_and_P1 = []
        for i in range(len(P0)):
            direction_vector_btwn_P0_and_P1.append(P1[i] - P0[i])
            
        dVec = bpnMath.normalizeAndScale(direction_vector_btwn_P0_and_P1, d)
        

        #getting P4 in 4d
        P4 = []  
        for i in range(0, len(dVec)):
            P4.append(dVec[i] + P0[i])
            
        V4 = []
        for i in range(0, len(P4)):
            V4.append(P4[i] - P2[i])
        
    

        return bpnMath.normalizeAndScale(V4, BigPreciseNum.BigPreciseNum(bpnMath.planck_length))

    
        
    def getVelocityVectorDisplacement(self, lightCharge, dt):
        phi = self.getDeltaPhi1(dt, lightCharge)

        vectorToRotate = self.copyVector(self.velocity_direction_unit_vector)

        P0 = []
        for i in range(0, len(self.position)):
            P0.append(BigPreciseNum.BigPreciseNum(self.position[i]) + vectorToRotate[i])
        
        P1 = []
        for i in range(0, len(lightCharge.position)):
            P1.append(BigPreciseNum.BigPreciseNum(lightCharge.position[i]))
        P2 = []
        for i in range(0, len(self.position)):
            P2.append(BigPreciseNum.BigPreciseNum(self.position[i]))
            
        new_vector = self.getRotatedVector(P0, P1, P2, phi)


        if(bpnMath.getMagnitude(new_vector) == bpnMath.zero):
            old_vector = []
            for i in range(0, len(self.velocity_direction_unit_vector)):
                old_vector.append(BigPreciseNum.BigPreciseNum(self.velocity_direction_unit_vector[i]))
            return old_vector


        return new_vector
    
    def getCVectorDisplacement(self, lightCharge, dt):
        phi = self.getDeltaPhi2(dt, lightCharge)

        vectorToRotate = []
        for i in range(0, len(self.c_direction_unit_vector)):
            vectorToRotate.append(BigPreciseNum.BigPreciseNum(self.c_direction_unit_vector[i]))
            
        if(phi == bpnMath.zero):
            return vectorToRotate
        
        P0 = []
        for i in range(0, len(self.position)):
            P0.append(BigPreciseNum.BigPreciseNum( self.position[i]) + vectorToRotate[i])
            
        P1 = []
        for i in range(0, len(lightCharge.position)):
            P1.append(BigPreciseNum.BigPreciseNum(lightCharge.position[i]))
        P2 = []
        for i in range(0, len(self.position)):
            P2.append(BigPreciseNum.BigPreciseNum(self.position[i]))
            
        new_vector = self.getRotatedVector(P0, P1, P2, phi)
        

            
        if(bpnMath.getMagnitude(new_vector) == bpnMath.zero):
            old_vector = []
            for i in range(0, len(self.c_direction_unit_vector)):
                old_vector.append(BigPreciseNum.BigPreciseNum(self.c_direction_unit_vector[i]))
            return old_vector


        return new_vector
    


    
    

    #TODO check v is self.velocity or lightCharge.velocity

      

            
    def getUpdatedLightCharge(self, lightCharges, dt):  
        
        velocity_displacement = bpnMath.normalizeAndScale(self.velocity_direction_unit_vector, (self.velocity * dt))
        mag_force_displacement = bpnMath.normalizeAndScale(self.c_direction_unit_vector, (bpnMath.speed_of_light * dt))
        
        new_position = []
        for i in range(0, len(self.position)):
            new_position.append(self.position[i] + velocity_displacement[i] + mag_force_displacement[i])
       
        net_electric_displacement = []
        for i in range(0, len(self.position)):
            net_electric_displacement.append(BigPreciseNum.BigPreciseNum(bpnMath.zero))
            
        net_mag_displacement = []
        for i in range(0, len(self.position)):
            net_mag_displacement.append(BigPreciseNum.BigPreciseNum(bpnMath.zero))

       
        for lightCharge in lightCharges:
            lightChargeCpy = lightCharge.getCopy(lightCharge)

            if(lightChargeCpy.index != self.index):
                electricDisplacement = self.getVelocityVectorDisplacement(lightCharge, dt)
                    
                for i in range(0, len(net_electric_displacement)):
                    net_electric_displacement[i] += electricDisplacement[i]
                
                magDisplacement = self.getCVectorDisplacement(lightCharge, dt)
                    
                for i in range(0, len(net_mag_displacement)):
                    net_mag_displacement[i] += magDisplacement[i]
                    
                
                

        #TODO, update velocity_magnitude
        
        
        new_velocity_direction_unit_vector = bpnMath.normalizeAndScale(net_electric_displacement, BigPreciseNum.BigPreciseNum(bpnMath.planck_length))

        new_c_direction_vector = bpnMath.normalizeAndScale(net_mag_displacement, BigPreciseNum.BigPreciseNum(bpnMath.planck_length))


        return LightCharge(new_position, BigPreciseNum.BigPreciseNum(self.velocity),
                      new_velocity_direction_unit_vector, self.positive_charge,
                      self.index, self.map_color_str,
                      new_c_direction_vector)
   
    def __repr__(self):
         return "LightCharge(idx:" + str(self.index) + " position:" + str(self.position) + " velocity unit vector:" + str(self.velocity_direction_unit_vector) + " positive charge:" + str(self.positive_charge) + " velocity magnitude:" + str(self.velocity)