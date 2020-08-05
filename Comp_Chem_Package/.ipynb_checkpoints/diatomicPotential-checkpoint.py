#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Abstract Class to define the properties of a diatomic potential used to fit a PES 

from abc import ABC, abstractmethod
from compChemGlobal import *

class DiatomicPotential(ABC):
    
    #Declare all global variables here
    #Need to provide a value for name in the deriving class by declaring the same variable
    name = "Potential Energy Surface Fitter"
    
    #used to determine if the fitter has been fit to data
    fit = False
    
    diatomicConstants = None
    
    #data must be the dictionary output from a PES Method Computation
    def __init__(self, diatomicConstants, data=None):
        self.diatomicConstants = diatomicConstants
        
        if(data != None):
            self.fit(method)

###################################################################################
    
    def compute(self, r):
        if(self.fit):
            return self.implementation(r)
        else:
            print("Please fit the " + self.name + ", using the 'fit' method.")
            
###################################################################################

    #data must be data dictionary from a PES Method object from its getResult method
    def fit(self, data):
        self.internalFit(data)
        self.fit = True
        
###################################################################################

    @abstractmethod
    def implementation(self, r):
        pass

###################################################################################

    #data will be a data dictionary from a PES Method object from its getResult method
    #must be overridden with code for the fitting logic
    @abstractmethod
    def internalFit(self, data):
        pass