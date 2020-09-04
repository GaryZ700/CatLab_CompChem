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
    integrationStart = 0
    
    @abstractmethod
    def __init__(self, integrationStart=0):
        self.integrationStart = integrationStart
        
    
###################################################################################  
    @abstractmethod
    def operatesOn(self, other):
        pass

###################################################################################

    def __getitem__(self, coord):
        return self.matrix[coord[0],coord[1]]
    
###################################################################################

    def __str__(self):
        return str(self.matrix)
    
#----------------------------------------------------------------------------------

#Kinetic Energy 
class TOperator(Operator):

    def __init__(self, basisSet=None, integrationStart=0):

        self.integrationStart = integrationStart
        
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
                    self.matrix[i, j] = round(integrate( lambda r : b1.value(r) * constant * ddx(b2.value, r, n=2), 0, inf), precision)
                else: 
                    self.matrix[i, j] = 0
        return self

###################################################################################

    def __add__(self, other):
        
        if(type(other) == VOperator):
            return HOperator()._setMatrix(self.matrix + other.matrix)
        
#----------------------------------------------------------------------------------

#Potential Energy
class VOperator(Operator):
    
    #Declare global variables here
    matrix = None
    
    def __init__(self, basisSet=None, pes=None, potentialFunction=None, integrationStart=0):
        
        self.integrationStart = integrationStart
        
        if(basisSet != None):
            if(pes != None):
                self.operatesOn(basisSet, pes)
            elif(potentialFunction != None):
                self.operatesOn(basisSet, potentialFunction=potentialFunction)
    
    def operatesOn(self, basisSet, pes=None, potentialFunction=None):
        
        #Declare variables needed for the computation
        self.matrix = np.zeros([basisSet.size, basisSet.size])
        
        if(potentialFunction == None):
            potentialFunction = lambda r : pes.value(r)
        
        for i, b1 in enumerate(basisSet):
            for j, b2 in enumerate(basisSet):
                
                if(i > j):
                    self.matrix[i, j] = self.matrix[j,i]
                else:
                    self.matrix[i, j] = integrate(lambda r : b1.value(r) * potentialFunction(r) * b2.value(r), self.integrationStart, inf)
        
        return self
    
###################################################################################

    def __add__(self, other):
        if(type(other) == TOperator):
            return HOperator()._setMatrix(self.matrix + other.matrix)
        else: 
            return 0
        
#----------------------------------------------------------------------------------

#Hamiltonian
class HOperator(Operator):
    
    #Declare global variables here
    matrix = None
    
    def __init__(self, arg1=None, arg2=None, precision=pow(10,10)):
        
        if(arg1 != None):
            self.operatesOn(arg1, arg2, precision)

###################################################################################
        
    def operatesOn(self, arg1, arg2, precision=pow(10,10)):
        if(type(arg1) == VOperator or type(arg1) == TOperator):
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
                    self.matrix[i,j] = round(integrate( lambda r : b1.value(r) * constant * ddx(b2.value, r, n=2), 0, inf), precision) + integrate(lambda r : b1.value(r) * pes.value(r) * b2.value(r), self.integrationStart, inf)
    
###################################################################################

    def _setMatrix(self, matrix):
        self.matrix = matrix
        return self

###################################################################################

    def __mul__(self, basis):
        return schrod(self, basis)
        
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