#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Concrete Class to define the properties of a Harmonic Oscillator Potential Energy Surface

from diatomicPotential import * 

class howPotential(DiatomicPotential):
    
    #Global public variables
    name = "Harmonic Oscillator PES"
    
    #Global private variables
    isFit = True
    start = -4
    end = 4
    
    #re in units of meters
    #k in units of kg/s
    re = None
    k = None

###################################################################################

    #for a given r, returns the specified PES value
    #r will be passed in units of angstroms
    #PES value must be returned in units of wavenumbers
    def implementation(self, r):
        return self.k * ((r - self.re) ** 2) * a2ToM2 * jToWavenumbers
    
###################################################################################

    def __init__(self, diatomicConstants):
        
        self.graphableData = []
        self.graphableObjects = []
        self.graphedObjects = []
        self.graphedData = []
        self.diatomicConstants = diatomicConstants
        

        #unit analysis
        #K should be in units of Kg/s^2 A^2->M^2
        #why 2pi^2 and not 4pi^2
        self.k = diatomicConstants["u"] * pow(diatomicConstants["w"] * c * pi, 2) * 20000 * amuToKg         
        self.re = diatomicConstants["re"] 
        
        #Set up the Graphable class here
        self.graphTitle = self.name + " for " + diatomicConstants["name"] 
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavenumbers"

###################################################################################

    def internalFit(self, data):
        pass