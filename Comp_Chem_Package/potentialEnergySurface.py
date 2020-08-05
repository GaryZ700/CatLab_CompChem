#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Class to create a potential energy surface given a computation and fitting method

from compChemComputation import *
from graphable import *
from morsePotential import *
from rkr import *

class potentialEnergySurface(Graphable):
    
    #Declare all global variables here
    fitting = 0
    
    def __init__(self, diatomicConstants, method=rkr, fitting=morsePotential):
        
        method = method(diatomicConstants)
        
        self.fitting = fitting()
        self.fitting.fit(method.getResult())
        
        #Set up graphable variables
        self.graphTitle = "Potential Energy Surface using " + method.name + " and " + fitting.name 
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavenumbers"
        
        self.graphableObjects = [method, self.fitting]
        
###################################################################################

    def compute(self, r):
        return self.fitting.compute(r)

###################################################################################

    def getWidgets(self):
        Return False