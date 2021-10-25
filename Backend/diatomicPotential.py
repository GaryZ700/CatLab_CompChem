#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Abstract Class to define the properties of a diatomic potential used to fit a PES 

from compChemGlobal import * 
from nistScraper import getDiatomicConstants

class DiatomicPotential(Graphable):
    
    #Declare all global variables here
    #Need to provide a value for name in the deriving class by declaring the same variable
    name = "Potential Energy Surface Fitter"
    
    #Local Global Variables
    
    #used to determine if the fitter has been fit to data
    isFit = False
    
    pesData = []
    diatomicConstants = None
    
    #has implementation of the diatomic potential provides a value in 1/cm for each 
    #r in angstroms
    @abstractmethod
    def implementation(self, r):
        pass

###################################################################################

    #data will be a data dictionary from a PES Method object from its getResult method
    #must be overridden with code for the fitting logic
    @abstractmethod
    def internalFit(self, data):
        pass
    
###################################################################################

    def getWidgets(self, traces = None, widgets = None):
        return False
    
###################################################################################

    #Inverts the wavefunction equation to get the r values for a specified E value
    #Is optional to implement but is recomended
    #Answer will be either 0 or 1 and if 0 will return the smaller answer, and if 1 will return the larger answer
    def invert(self, E, answer):
        if (answer == 0):
            return -2
        else: 
            return 2

###################################################################################

    #data must be the dictionary output from a PES Method Computation
    def __init__(self, diatomicConstants=None, data=None):
        self.diatomicConstants = diatomicConstants
        self.graphableData = []
        self.graphableObjects = []
        self.graphedData = []
        self.highestResData = []
    
        if(data != None):
            self.fit(data)
            
        #set up graphable parent class
        self.graphTitle = self.name
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavenumbers"
    
###################################################################################
    
    def value(self, r):
        if(self.isFit):
            if(r < -100):
                return 0
            return self.implementation(r)
        else:
            print("Please fit the " + self.name + ", using the 'fit' method.")
            exit()
            
            
###################################################################################

    #data must be data dictionary from a PES Method object from its getResult method
    def fit(self, data):
        
        self.addGraphableData(dict(x=data["r"], y=data["E"]), "Fitting Data")
        self.start = floor( (min(data["r"]) - 0.025) * 100) / 100 
        self.end = ceil(max(data["r"]) + 1)
        self.internalFit(data)
        self.isFit = True
        return self

###################################################################################

    def save(self):
        
        if(not self.isFit):
            return False
        
        globalDB.connect()
        globalDB.write("pes_methods", "(molecule, method, r, E, D, start, end)", "(?,?,?,?,?,?,?)", (self.diatomicConstants["name"], 
                        self.pesData["method"], globalDB.flatArrayToDB(self.pesData["r"]), 
                        globalDB.flatArrayToDB(self.pesData["E"]), self.pesData["D"], self.start, self.end))
        
        globalDB.close()
        
        return True
    
###################################################################################

    def load(self, molecule, method):
        
        globalDB.connect()
        
        data = globalDB.getData("pes_methods", ["molecule", "method"], [molecule, method])
        if(data == []):
            return False
        
        data = data[0]
        self.name = data[1]
        self.pesData = dict(method = data[1], r = list(globalDB.dbToFlatArray(data[2])), E = list(globalDB.dbToFlatArray(data[3])), D = float(data[4]))
        self.start = data[5]
        self.end = data[6]
        self.isFit = True
        
        self.diatomicConstants = globalDB.getDiatomicConstants(molecule)

        self.fit(self.pesData)        
        
        globalDB.close()
        return True