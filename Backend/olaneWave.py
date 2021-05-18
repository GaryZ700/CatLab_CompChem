#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Concrete implementation of the plane wave basis function

from basisFunction import *

class planeWave(basisFunction):
    
    #Declare all global variables here
    name = "Plane Wave"
    
    @abstractmethod
    def __init__(self, diatomicConstants, n):
        super().__init__()
    
###################################################################################
    
    #computes the value of the wavefunction at the specified value of r
    #r will be in units of Angstroms
    #output must be in units of 1 / Sqrt(Angstroms)
    @abstractmethod
    def value(self, r):
        pass