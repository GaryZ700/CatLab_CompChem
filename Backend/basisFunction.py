#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Abstract class that specifies the methods all individual wavefunctions must have

#Also imports the compChemGlobal class here to allow its constants and functions to be accessed from all the derviving child subclasses

from compChemGlobal import *
from squaredBasisFunction import *

class basisFunction(Graphable):
    
    #Declare all global variables here
    name = None
    
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
    
###################################################################################

    #shortcut method to make computation of the kinetic energy computationally
    #easier if the basisfunction in question allows for an analytical solution
    #must return a numpy matrix of the kinetic energy operator for the wavefunction, 
    #and the given basis function
    #can return false if not analytical method exists for the basis function
    def kineticEnergy(self, basisSet):
        return False

###################################################################################

    def squaredValue(self, r):
        return self.value(r) ** 2
    
    ###################################################################################
    
    #graphs the wavefunction
    #figure bool that represents weather or not the graph or figure 
    #trace should be added to a figure object
    def graph(self, showGraph=True, getGraph=False, **kargs):
        self.addGraphableObject(squaredBasisFunction(self))
        return super().graph(showGraph = showGraph, getGraph = getGraph, **kargs)
        
    ###################################################################################
    
    def getWidgets(self, traces, widgetsData):
        
        #Show only the standard wavefunction
        traces[0].visible = False
        
        probabilityWidget = plot.widgets.Dropdown(
                options = ["Standard", "Probability Distribution", "Standard & Probability"],
                description = '<p style="font-family:verdana;font-size:15px">Mode</p>', 
                value = "Standard"
            )
        
        probabilityWidget.observe(lambda change : self.widgetUpdate(probabilityWidget.value, traces), "value")
    
        return [[probabilityWidget, 1]]
        
    ###################################################################################
   
    def widgetUpdate(self, probability, traces):
    
        if(probability == "Standard"):
            traces[0].visible = False
            traces[1].visible = True
        elif(probability == "Probability Distribution"):
            traces[0].visible = True
            traces[1].visible = False
        else:
            traces[0].visible = True
            traces[1].visible = True       
                        
    ###################################################################################
    
    def __call__(self, r):
        return self.value(r)