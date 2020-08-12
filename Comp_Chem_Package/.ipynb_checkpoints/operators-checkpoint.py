#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University

from compChemGlobal import *
import numpy as np

#All operators are in units of 1/cm

#Kinetic Energy 
class T:
    
    #Delcare global variables here
    matrix = None
    
    def __init__(self, basisSet=None):
        if(basisSet != None):
            self.operatesOn(basisSet)
            
###################################################################################
    
    def operatesOn(self, basisSet):
        
        #Declare variables needed for the calculation
        matrix = np.matrix( [basisSet.size, basisSet.size] )
        constant = -hbar*hbar*jToWavenumbers / (2*basisSet.diatomicConstants["u"]*aToM2)
        
        for i, b1 in enumerate(basisSet):
            for j, b2 in enumerate(basisSet):
                self.matrix[i, j] = integrate( lambda r : b1(r) * constant * ddx(b2, r, n=2), 0, inf)
                
#Potential Energy
class V:
    
    #Declare global variables here
    matrix = None
    
    def operatesOn(self, basisSet, pes):
        
        #Declare variables needed for the computation
        matrix = np.matrix([basisSet.size, basisSet.size])
        
        for i, b1 in enumerate(basisSet):
            for j, b2 in enumerate(basisSet):
                
                if(i > j):
                    V[i, j] = V[j,i]
                else:
                    V[i, j] = integrate(lambda r : b1(r) * pes.compute(r) * b2(r), 0, inf)
        
        
#Hamiltonian
class H:
    pass


# Tmatrix = T.operatesOn(basisSet)
# Vmatrix = V.operatesOn(basisSet, pes)

# H = T + V

# H(T,V)

# T|basisSet>
# pes|basisSet>
# T*basisSet
# *basisSet*pes

# [
#     [  ],
#     [],
#     [],
# ]


# H|basisSet>

# schrod("H2", )

# Wavefunction.eigVals
# .eigFuncs
# .graph()