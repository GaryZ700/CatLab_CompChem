#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Abstract Class to define the properties of a method that computes a potential energy surface

from abc import ABC, abstractmethod
from compChemGlobal import *

class PESMethod(ABC):
    
    #Declare all global variables here
    #E must be in 1/cm and r must be in angstroms
    name = "Potential Energy Surface Method"
    
    @abstractmethod
    def __init__(self):
        super().__init__()
        self.name = "Abstract Potential Energy Surface Method"
        
###################################################################################

    @abstractmethod
    def compute(self, r):
        pass

###################################################################################

    def graph(self, showGraph=False):
        pass
        
potentialEnergySurface(method=HF, fitter=morsePotential)