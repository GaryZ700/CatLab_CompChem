#Written by Gary Zeri 
#Computer Science Student at Chapman University

#Includes various basis sets that can be used in other molecular computations, such as the Harmonic Oscillator

class harmonicOscillator():
    
    import numpy as np
    import math
    
    #Declare all Global Variables Here
    basisSize = 0
    basisSet = []
    
    #u is the reduced mass
    #w is the ground state vibrational frequency
    #Re is the optimal bond distance
    u = 0
    w = 0 
    Re = 0
    
    def __init__(self, basisSize, u, w, Re):
        
        self.basisSize = basisSize
        self.u = u
        self.w = w 
        self.Re = Re
        
        for n in range(basisSize):
            
            self.basisSet.append(self.newHO(n))
        
###################################################################################
        
    #Returns a lambda function of the nth hermite polynomial
    def hermite(self, n, k):
    
        c = pow(-1, k) * self.math.factorial(n) / ( self.math.factorial(k) * self.math.factorial(n - 2*k) )
        
        if(k == 0):
            return lambda r : c * pow(2*self.np.sqrt(self.u * self.w)*( r-self.Re ), n-(2*k))
        else:
            return lambda r : c * pow(2*self.np.sqrt(self.u * self.w)*( r-self.Re ), n-(2*k)) + self.hermite(n, k-1)(r) 
        
###################################################################################

    #Constructs the nth hermite polynomial function, and returns the specified lambda function
    def buildHermite(self, n):
        return self.hermite(n, n // 2)
    
###################################################################################

    #returns the normalization constant for the nth Harmonic Oscillator Function
    def C(self, n):    
        return self.np.sqrt( self.np.sqrt(self.u * self.w) /  (pow(2, n) * self.math.factorial(n) * self.np.sqrt(self.np.pi) )) 

###################################################################################

    #Creates a new Harmonic Oscillator function
    #and returns it as a lambda function
    def newHO(self, n):
        return lambda r : self.C(n) * self.buildHermite(n)(r) * self.np.exp(-self.u * self.w * pow(r-self.Re,2) / 2)  
    
###################################################################################    