#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Abstract Class to define the properties of all methods used to generate a Potential Energy Surface

from compChemGlobal import * 
from graphableData import * 

class PESMethod(GraphableData):
    
    #Declare all global variables here that need to be overridden in the child class
    name = "Potential Energy Surface Method"
    
    #Global private variables
    data = None
    diatomicConstants = None
    start = 0.5
    end = 5

    #if no widgets are desired for the child class, then have this function return False
    @abstractmethod
    def getWidgets(self):
        return False

###################################################################################

    #for a given r, returns the specified PES value
    #r will be passed in units of angstroms
    #PES value must be returned in units of wavenumbers
    @abstractmethod
    def implementation(self, r):
        pass
    
###################################################################################

    def __init__(self, diatomicConstants):
        
        self.diatomicConstants = diatomicConstants
        
        #Set up the Graphable class here
        self.graphTitle = self.name + " for " + diatomicConstants["name"] 
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavenumbers"

###################################################################################

    #Override the graph function to account for the fact that PESMethods will compute
    #data all at once instead of in real time due to speed issues
    def graph(self, showGraph=True, precision=None):
        
        if(self.data == None):
            print("Please run the compute method on the " + self.name + " object before graphing the object.")
            return
        
        super().graph()
            
###################################################################################

    def compute(self, start=None, end=None, resolution=None):
        
        if(start == None):
            start = self.start
        if(end == None):
            end = self.end
        if(resolution == None):
            resolution = self.resolution
        
        r, E = plot.graphFunction(self.implementation, title=self.graphTitle, 
                                  start=start, end=end, resolution=resolution, rawData=True)
        
        #force PES to be positive
        minE = min(E)
        if(minE < 0):
            minE *= -1
            for i in range(len(E)):
                E[i] += minE
            
        
        self.data = dict(r=r, E=E, D = minE, method = this.name)

        return self.data

###################################################################################

    def getData(self):
        return self.data

###################################################################################

    def getGraphData(self):
        return [self.data["r"], self.data["E"]]
    
###################################################################################