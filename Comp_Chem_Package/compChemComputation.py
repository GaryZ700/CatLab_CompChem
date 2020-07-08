#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Abstract class that specifies the methods all Computational Chemistry Calculations must contain and support

#Also imports the compChemGlobal class here to allow its constants and functions to be accessed from all the derviving 
#child subclasses

from abc import ABC, abstractmethod
from compChemGlobal import *

class compChemComputation(ABC):
    
    def __init__(self):
        super().__init__()
    
    ###################################################################################
    
    #Menu of ipython widgets for calculation input
    @abstractmethod
    def menu(self):
        pass
    
    ###################################################################################
    
    #Allows for manual inputing of data to to the computation
    @abstractmethod
    def inputData(self):
        pass
    
    ###################################################################################
    
    #Graphs the computation onto the screen
    @abstractmethod
    def graph(self):
        pass
    
    ###################################################################################
    
    #Function that computes the calculation and returns an expected output object
    #given the nature of the calculation
    @abstractmethod
    def compute(self):
        pass
    
    ###################################################################################
    
    #Function to return the output of the program once the compute method has been 
    #called
    @abstractmethod
    def getOutput(self):
        pass