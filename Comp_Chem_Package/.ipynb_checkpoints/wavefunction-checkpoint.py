#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Class that represents the wavefunction that is a solutoin from solving the schrodinger equation

from graphable import *

#Wavefunction derives from basis function as a wavefunction can also be used as a basis set as well
class wavefunction(Graphable):
    
    
    #Declare global variables here
    function = None
    energy = 0
    scalingFactor = 1
    squared = False
    
    def __init__(self, eigenVector, energy, basis, n, squared=False):
        self.graphTitle = "Wavefunction n=" + str(n)
        if(squared):
            self.graphTitle = "Squared " + self.graphTitle
            
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavefunction Output"
        
        self.energy = energy
        self.function = lambda r : sum( [ eigenVector[i]*basis[i](r) for i in range(basis.size)] )
        
        self.squared = squared

###################################################################################

    def value(self, r):
        value = self.function(r)
        return (pow(value, 2) if self.squared else value) * self.scalingFactor + self.energy

###################################################################################

    def scale(self, scalingFactor=900):
        self.scalingFactor = scalingFactor
        return self
