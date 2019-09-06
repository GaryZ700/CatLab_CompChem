#Morse Potential Class used to derive a Morse Potential from a Hartree-Computed 
#Potential Energy Surface for a diatomic molecule

import math

class morsePotential:
    
    #Declare all global variables here
    potentialEnergy = {}
    bondLength = []
    morseEnergy = []
    r0 = 0
    D = 0
    dIndex = 0
    a = 0
    da = 0
    switchMax = 0
    
    #bondLength is an array of bond lengths that matches up to an array of 
    #potential energies at the specified bond length
    #bond length, list of bond lengths from 
    def __init__(self, bondLength, potentialEnergy, a=0.5, da=0.00001, switchMax=5):
        
        self.bondLength = bondLength
        self.potentialEnergy = potentialEnergy.copy()
        
        self.a = a
        self.da = da
        self.switchMax = int(switchMax)
        
        self.D = abs(min(potentialEnergy))
        self.dIndex = potentialEnergy.index(min(potentialEnergy))
        self.r0 = bondLength[self.dIndex]
        
#--------------------------------------------------------------------------------

    #Given a specifed bond length r, will return the approximation's potential energy
    def morseEquation(self, r):
        return (self.D * math.exp(-2 * self.a * ( r - self.r0 )) - (2 * self.D * math.exp(-self.a * ( r - self.r0 ))))
                
#-------------------------------------------------------------------------------
                
    def buildPotential(self, bondLength=False):
        
        self.morseEnergy = []
                
        #check whether to use classe's bondLengths or the parameter passed into the function
        if(not bondLength):
            bondLength = self.bondLength
        
        for r in self.bondLength:
            self.morseEnergy.append( self.morseEquation(r) )
            
        return self.morseEnergy
                
#--------------------------------------------------------------------------------
   
    #computes the distance between two points using the pythagorean theorem
    def distance(self, a, b):
        return math.sqrt( pow(a[0] - a[1], 2) + pow(b[0] - b[1], 2) )
                
#--------------------------------------------------------------------------------                
    def meanDifference(self):
        
         distances = []
            
         for r in range(len(self.bondLength)):
                distances.append( self.distance(
                    [self.morseEnergy[r], self.morseEnergy[r]],
                    [self.potentialEnergy[r], self.morseEnergy[r]]
                ))
                
         return sum(distances) / len(distances)
                
#--------------------------------------------------------------------------------
                
    #computes the morse potential given the potential energy surface 
    #unable to analytically determimne the a value, and use a form 
    #of the variational principle in order to estimate the a, and 
    #generate the potential data
    def computePotential(self):
        
        meanDifferences = []
        meanDiffDelta = []
        switchCounter = 0
        counter = 0
        addSwitch = True
        
        while(True):
                
           self.buildPotential()
             
           meanDifferences.append( self.meanDifference() )
           
           #check if there is enough mean data in order to compute the differnces between the means
           if(counter > 0):
               meanDiffDelta.append(abs(meanDifferences[counter] - meanDifferences[counter - 1]))
            
               #checck if there is enough difference data in order to verify effectiveness 
               #of the a adjustments
               if(len(meanDiffDelta) > 1):
                   if(meanDiffDelta[counter - 1] < meanDiffDelta[counter - 2]):
                       if(switchCounter >= self.switchMax):
                           print("Morse Potential Computation Complete\n")
                           return self.morseEnergy
                   else:
                       addSwitch = not addSwitch
                       switchCounter += 1
                       self.da *= 0.5
                       print("Morse Potential Computation: " + str(switchCounter * 100 // self.switchMax) + "%")
           
            #check whether the a value should be incremented or decremented by the da value
           if(addSwitch):
               self.a += self.da
           else:
               self.a -= self.da
          
           counter += 1