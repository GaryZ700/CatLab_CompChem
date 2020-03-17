#Written by Gary Zeri, Computer Science Major at Chapman University and Member of the LaRue CatLab

from tqdm import tqdm 
import numpy as np
from diatomicConstants import diatomicConstants as dc

#RKR Class to Allow for Simple RKR Calcuations as needed
#All diatamic constants must in units of wavenumbers, (inverse CM)
#Resulting energy is in wavenumbers and bond distance is in Angstroms
class rkr:
    
    #Declare All Global Variables Here
    
    #Is the distance from v that the integration stops at
    delta = pow(10, -15)

    #Reduced Molecular Mass
    #In Non Hartree Atomic Units, each proton has an amu of 1
    u = 0

    #Diatomic Constants, must be in Wavenumbers (1 / cm)
    diatomicConstants = 0
    
    turningPoints = []
    energy = []
    
    dataGraphed = False
    createdWidgets = False

    #DC: Refers to the Diatomic Constants Named Tuple containg diatomic constants
    def __init__(self, DC=None):
        if(DC != None):
            self.setDiatomicConstants(DC)
    
###################################################################################

    def setDiatomicConstants(self, DC):
    
        self.diatomicConstants = DC
        
        self.u = DC.u
        self.dataGraphed = False
        self.turningPoints = []
        self.energy = []
        
###################################################################################

    def setReducedMass(self, u):
        self.u = u
        
        self.dataGraphed = False
        self.turningPoints = []
        self.energy = []
        
###################################################################################

    def setDelta(self, delta):
        self.delta = delta
    
###################################################################################

    def E(self, v):
        term = v + 0.5 
        return (self.diatomicConstants.w * term) - (self.diatomicConstants.wx*pow(term, 2)) + (self.diatomicConstants.wy*pow(term, 3)) + (self.diatomicConstants.wz*pow(term,4))

###################################################################################
    
    def integralRadical(self, v, vPrime):
        return np.sqrt( self.E(v) - self.E(vPrime) )

###################################################################################       
    
    def B(self, v):
        term = v + 0.5
        return self.diatomicConstants.B - (self.diatomicConstants.a * term)  + self.diatomicConstants.y*pow(term, 2)

###################################################################################       

    def Q(self, v):
        term = v + 0.5
        return self.diatomicConstants.w - (2*self.diatomicConstants.wx*term) + (3*self.diatomicConstants.wy*pow(term, 2)) + (4*self.diatomicConstants.wz*pow(term,3))
    
###################################################################################           

    def correctionFactor(self, v):
        return 2 * np.sqrt(self.delta / self.Q(v))

###################################################################################           

    def f(self, v):
        
        from scipy.integrate import quad as integrate
        
        integrand = lambda vPrime: 1 / self.integralRadical(v, vPrime)
        return integrate(integrand, -0.5, v-self.delta,)[0] + self.correctionFactor(v)
    
###################################################################################

    def g(self, v):
        
        from scipy.integrate import quad as integrate
        
        integrand = lambda vPrime : self.B(vPrime) / self.integralRadical(v, vPrime)
        return integrate(integrand, -0.5, v-self.delta)[0] + (self.B(v)*self.correctionFactor(v))
    
################################################################################### 

    #v refers to the specided energy level for which the turning points should be computed for
    def compute(self, v):
        
        #Check that reduced mass is not zero and that an exception will not be thrown when 
        #division by zero occurs
        if(self.u == 0):
            print("Warning!! The reduced mass $\mu$ must be greater than 0!")
            print("Please use the setReducedMass(muValue) method on the RKR class instance to fix this issue.")
            print("RKR method is now aborting.")
            return
   
        c0 = 4.1058045 * self.f(v) / np.sqrt(self.u)
    
        #automatically return NAN since V was larger than the RKR method could handle
        if(np.isnan(c0)):
            return [c0, c0]
    
        radicand = 1 / ( self.f(v) * self.g(v) )
        c1 = np.sqrt(1 + radicand)

        self.energy.extend( [self.E(v)] * 2 )
        self.turningPoints.append( c0 * (c1 + 1) )  
        self.turningPoints.append( c0 * (c1 - 1) )
        
        return ( (self.turningPoints[-1], self.turningPoints[-2], self.energy[-1]) )
    
###################################################################################

    def graphData(self, resolution=0.01, startPoint=-0.499, endPoint=1000):

        if(not self.dataGraphed):
            
            self.dataGraphed = True
            self.turningPoints = []
            self.energy = []
            
            #Derivative Lists & Cutoff Computation Variables
            ddX = []
            ddX2 = []
            ddx = []
            ddx2 = []
            leftAsympCutOff = False
            
            print("\nGenerating RKR Potential")
            for v in tqdm(np.arange(startPoint, endPoint, resolution)):
                
                if(np.isnan(self.compute(v))[0]):
                    break
                
                if(not leftAsympCutOff and len(self.turningPoints) >= 3):
                    #Compute First Derivative
                    ddX.append( (self.turningPoints[-1] + self.turningPoints[-3]) / 2 ) 
                    slope = (self.energy[-1]-self.energy[-3]) / (self.turningPoints[-1] - self.turningPoints[-3]) 
                    ddx.append( slope )
        
                    if(len(ddx) > 1):
                        #Compute 2nd Derivative
                        ddX2.append( (ddX[-2] + ddX[-1]) / 2 )
                        ddx2.append( (ddx[-1] - ddx[-2]) / (ddX[-1] - ddX[-2]) )

                        #Determine if Cutoff should be used
                        if(ddx2[-1] <= 0):
                            leftAsympCutOff = True
                
                #cutoff the uneeded values to allow the asymptote on the left side to 
                #continue to infinity instead of flattening out
                if(leftAsympCutOff):
                    self.energy.pop()
                    self.turningPoints.pop()
                    
        return self.turningPoints, self.energy