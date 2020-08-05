#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Abstract Class to define the properties of all methods used to generate a Potential Energy Surface

from ABC import abc, abstractmethod
from compChemGlobal import * 
from graphable import * 
from sys import maxint

class PESMethod(abc, Graphable):
    
    #Declare all global variables here that need to be overridden in the child class
    name = "Potential Energy Surface Method"
    
    #Global private variables
    data = None
    diatomicConstants = None

    #if no widgets are desired for the child class, then have this function return False
    @abstractmethod
    def getWidgets(self):
        return False

###################################################################################

    #for a given r, returns the specified PES value
    @abstractmethod
    def implementation(self, r):
        pass
    
###################################################################################

    def __init__(self, diatomicConstants):
        
        self.diatomicConstants = diatomicConstants
        
        #Set up the Graphable class here
        self.graphTitle = name
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavenumbers"

###################################################################################

    #Override the graph function to account for the fact that PESMethods will compute
    #data all at once instead of in real time due to speed issues
    def graph(self, showGraph=True, title=graphTitle, precision=precision, xTitle=XTitle, yTitle=yTitle):
        
        if(self.data == None):
            print("Please run the compute method on the " + self.name + " object before graphing the object.")
            return
        
        trace = plot.buildTrace(self.data["r"], self.data["E"], 
                                title, precision, xTitle, yTitle)
        
        if(not showGraph):
            return trace
                                                  
        self.buildGraph(trace)
        
###################################################################################

    def compute(self, start=start, end=end, resolution=resolution):
        
        r, E = plot.graphFunction(self.implementation, start=start, end=end, 
                                  resolution=resolution, rawData=True)
        
        self.data = dict(r=r, E=E)
        self.data["D"] = max(self.data[""], key=lambda i: self.data["E"] if self.data["r"] > self.diatomicConstants.re else -maxint) - min(self.data["E"]) 
        
        return self.data

###################################################################################

    def getData(self):
        return self.data