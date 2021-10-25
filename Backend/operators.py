#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University

from compChemGlobal import *
from schrodinger import *
from basisSet import *
from abc import ABC, abstractmethod
import numpy as np
from multiprocess import Pool
from multiprocess import cpu_count

#----------------------------------------------------------------------------------


#All operators are in units of 1/cm
class Operator(ABC):
    
    #Declare global variables here
    matrix = None
    integrationStart = 0
    
    @abstractmethod
    def __init__(self, integrationStart=-np.inf):
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
    
###################################################################################

    def __eq__(self, obj):
        if(type(obj) == type(self)):
            return self.matrix == obj.matrix
        else:
            return False

#----------------------------------------------------------------------------------

#Kinetic Energy 
class TOperator(Operator):

    def __init__(self, basisSet=None, integrationStart=-inf):

        self.integrationStart = integrationStart
        
        if(basisSet != None):
            self.operatesOn(basisSet)
            
###################################################################################
    
    def operatesOn(self, basisSet, precision=5):
        
        #check if basisset has a pre-built calculation for the KE
        T = basisSet.kineticEnergy()
        if(type(T) != bool):
            self.matrix = T
            return self
        
        print("Calculating KE")
        #Declare variables needed for the calculation
        self.matrix = np.zeros( [basisSet.size, basisSet.size] )
        
        constant = -hbar*hbar*jToWavenumbers / (2*basisSet.diatomicConstants["u"]*a2ToM2*amuToKg)
        
        for i, b1 in enumerate(basisSet):
            for j, b2 in enumerate(basisSet):

                if(abs(i-j) == 2 or i == j):
                    self.matrix[i, j] = round(integrate( lambda r : b1.value(r) * constant * ddx(b2.value, r, n=2), self.integrationStart, inf), precision)
                    #self.matrix[i, j] = integrate( lambda r : b1.value(r) * constant * ddx(b2.value, r, n=2), self.integrationStart, inf)
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
        
        #Decide if multiprocessing or single processing should be used
        #based on number of cpus availble
        cpuCount = cpu_count()
        if(cpuCount >= minNumCPUs):
            p = Pool(cpu_count())
            integrationFunction = lambda index : integrate(lambda r : basisSet[index[0]].value(r) * potentialFunction(r) * basisSet[index[1]].value(r), -0.4, 3)
            basisPairs = []
            for i in range(basisSet.size):
                for j in range(i, basisSet.size):
                    basisPairs.append([i, j]) 

            results = p.map(integrationFunction, basisPairs)
            for resultsIndex, matrixIndex in enumerate(basisPairs):
                
                self.matrix[matrixIndex[0], matrixIndex[1]] = round(results[resultsIndex], 8)
                self.matrix[matrixIndex[1], matrixIndex[0]] = round(results[resultsIndex], 8)
        else:
            for i, b1 in enumerate(basisSet):
                for j, b2 in enumerate(basisSet):   
                    if(i > j):
                        self.matrix[i, j] = self.matrix[j,i]
                    else:
                        
                        self.matrix[i, j] = round(integrate(lambda r : b1.value(r) * potentialFunction(r) * b2.value(r), self.integrationStart, inf), 5)
        
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
    
    def __init__(self, arg1=None, arg2=None, precision=5):
        
        if(arg1 != None):
            self.operatesOn(arg1, arg2, precision)

###################################################################################
        
    def operatesOn(self, arg1, arg2, precision=5):
        
        #T + V 
        if(type(arg1) == VOperator or type(arg1) == TOperator):
                self.matrix = (arg1 + arg2).matrix
                
        #Assume one is basis and other is pes
        else: 
            if(type(arg1) == basisSet):
                basis = arg1
                pes = arg2
            else: 
                pes = arg1 
                basis = arg2
            
            self.matrix = np.zeros([basis.size, basis.size])
            constant = -hbar*hbar*jToWavenumbers / (2*basis.diatomicConstants["u"]*a2ToM2*amuToKg)

           # basisPairs = []
           # for i in range(basis.size):
           #     for j in range(i, basis.size):
           #         basisPairs.append([i, j]) 
                
            #        if(abs(i - j) == 2): 
            #            basisPairs.append([j, i])
                    
            #checkif integration is required for KE
            #if yes, build full integration lamabda function 
            #otherwise just integrate for the potential energy of the system
            T = basis.kineticEnergy()
            if(type(T) == bool):
                #integrationFunction = lambda index : round(integrate( lambda r : basis[index[0]].value(r) * constant * ddx(basis[index[1]].value, r, n=2), 0, inf), precision) + round(integrate(lambda r : basis[index[0]].value(r) * pes.value(r) * basis[index[1]].value(r), self.integrationStart, inf), precision)
                integrationFunction = lambda index : integrate( lambda r : basis[index[0]].value(r) * constant * ddx(basis[index[1]].value, r, n=2), 0, inf) + integrate(lambda r : basis[index[0]].value(r) * pes.value(r) * basis[index[1]].value(r), self.integrationStart, inf)
            else: 
                self.matrix += T 
                #integrationFunction = lambda index : round(integrate(lambda r : basis[index[0]].value(r) * pes.value(r) * basis[index[1]].value(r), self.integrationStart, inf), precision)
                integrationFunction = lambda index : integrate(lambda r : basis[index[0]].value(r) * pes.value(r) * basis[index[1]].value(r), self.integrationStart, inf)
                
            p = Pool(cpu_count())
            results = p.map(integrationFunction, [(i,j) for j in range(basis.size) for i in range(basis.size)]) 
            
            #for resultsIndex, basisIndex in enumerate(basisPairs):            
            #    self.matrix[basisIndex[0], basisIndex[1]] += results[resultsIndex]
                
            #    if(abs(basisIndex[0]-basisIndex[1]) != 2):
            #        self.matrix[basisIndex[1], basisIndex[0]] += results[resultsIndex]
            
            for i in range(basis.size):
                offset = basis.size * i
                for j in range(basis.size):
                    self.matrix[i, j] += results[j + offset]
            
    
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