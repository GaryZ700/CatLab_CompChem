#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University

from compChemGlobal import *
from schrodinger import *
from abc import ABC, abstractmethod
import numpy as np


#All operators are in units of 1/cm
class Operator(ABC):
    
    #Declare global variables here
    matrix = None
    
    @abstractmethod
    def operatesOn(self, other):
        pass

###################################################################################

    def __getitem__(self, i, j):
        return self.matrix[i,j]

#----------------------------------------------------------------------------------

#Kinetic Energy 
class T(Operator):

    def __init__(self, basisSet=None):
        if(basisSet != None):
            self.operatesOn(basisSet)
            
###################################################################################
    
    def operatesOn(self, basisSet, precision=pow(10, 10)):
        
        #Declare variables needed for the calculation
        self.matrix = np.zeros( [basisSet.size, basisSet.size] )
        
        constant = -hbar*hbar*jToWavenumbers / (2*basisSet.diatomicConstants["u"]*aToM2*amuToKg)

        for i, b1 in enumerate(basisSet):
            for j, b2 in enumerate(basisSet):
                
                if(abs(i-j) == 2 or i == j):
                    self.matrix[i, j] = round(integrate( lambda r : b1.compute(r) * constant * ddx(b2.compute, r, n=2), 0, inf), precision)
                else: 
                    self.matrix[i, j] = 0
        return self

###################################################################################

    def __add__(self, other):
        
        if(type(other) == V):
            return H()._setMatrix(self.matrix + other.matrix)
        
#----------------------------------------------------------------------------------

#Potential Energy
class V(Operator):
    
    #Declare global variables here
    matrix = None
    
    def operatesOn(self, basisSet, pes):
        
        #Declare variables needed for the computation
        self.matrix = np.zeros([basisSet.size, basisSet.size])
        
        for i, b1 in enumerate(basisSet):
            for j, b2 in enumerate(basisSet):
                
                if(i > j):
                    self.matrix[i, j] = self.matrix[j,i]
                else:
                    self.matrix[i, j] = integrate(lambda r : b1.compute(r) * pes.compute(r) * b2.compute(r), 0, inf)
        
        return self
    
###################################################################################

    def __add__(self, other):
        if(type(other) == T):
            return H()._setMatrix(self.matrix + other.matrix)
        else: 
            return 0
        
#----------------------------------------------------------------------------------

#Hamiltonian
class H():
    
    #Declare global variables here
    matrix = None
    
    def __init__(self, arg1=None, arg2=None, precision=pow(10,10)):
        
        if(arg1 != None):
            self.operatesOn(arg1, arg2, precision)

###################################################################################
        
    def operatesOn(arg1, arg2, precision=pow(10,10)):
        if(type(arg1) == V or type(arg1) == T):
                self.matrix = (arg1 + arg2).matrix
        else: 
            if(type(arg1) == basisSet):
                basis = arg1
                pes = arg2
            else: 
                pes = arg1 
                basis = arg2

            self.matrix = np.zeros([basis.size, basis.size])
            constant = -hbar*hbar*jToWavenumbers / (2*basis.diatomicConstants["u"]*aToM2*amuToKg)

            for i, b1 in enumerate(basis):
                for j, b2 in enumerate(basis):
                    self.matrix[i,j] = round(integrate( lambda r : b1.compute(r) * constant * ddx(b2.compute, r, n=2), 0, inf), precision) + integrate(lambda r : b1.compute(r) * pes.compute(r) * b2.compute(r), 0, inf)
    
###################################################################################

    def _setMatrix(self, matrix):
        self.matrix = matrix
        return self

###################################################################################

    def __mul__(self, basis):
        return schrod(H)
        
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