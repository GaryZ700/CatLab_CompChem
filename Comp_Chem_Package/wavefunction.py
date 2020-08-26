#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Class that represents the wavefunction that is a solutoin from solving the schrodinger equation

from graphable import *

class wavefunction(Graphable):
    
    #Declare global variables here
    function = None
    energy = 0
    scalingFactor = 1
    
    def __init__(self, eigenVector, energy, basis, n):
        self.graphTitle = "Wavefunction n=" + str(n)
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavefunction Output"
        
        self.energy = energy
        self.function = lambda r : sum( [ eigenVector[i]*basis[i](r) for i in range(basis.size)] )

###################################################################################

    def value(self, r):
        return self.function(r) * self.scalingFactor + self.energy

###################################################################################

    def scale(self, scalingFactor=900):
        self.scalingFactor = scalingFactor
        return self