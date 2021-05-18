#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

from diatomicPotential import *
from scipy.optimize import curve_fit

#Extended Rydberg Potential, is a child of the PESFitter abstract class
class extendedRydberg(DiatomicPotential):
    
    #Modify global variables here
    name = "Extended Rydberg Potential"
    
    #Declare local variables here
     
    #D: represents the well depth
    #Re: Equblibrium well depth
    #a1, a2, a3: constants that determine the curvature and shape of the potential
    #c: represent constant to be added to shift the potential up or down
    #curveFitted, bool that represents whether or not the curve has been fitted and used to 
    #avoid user caused errors
    D = 0 
    a1 = 0 
    a2 = 0 
    a3 = 0
    
    def implementation(self, r):
        p = r-self.diatomicConstants["re"]
        eTerm = exp(-self.a1 * p)
        return (-self.D * ( 1 + (self.a1*p) + (self.a2*pow(p, 2)) + (self.a3*pow(p, 3)) ) * eTerm) + self.D

###################################################################################

    #data will be a data dictionary from a PES Method object from its getResult method
    #must be overridden with code for the fitting logic
    def internalFit(self, data):
        self.D = data["D"]
        #print(self.D)
        self.c = min(data["E"])
        
        optimizedParameters = curve_fit(self.optimizationFunction, data["r"], data["E"], p0 = [self.D, 1, -1, 1], bounds = [[0, 0, -inf, 0], [inf, inf, 0, inf]]) [0]
        
        #print("OP", optimizedParameters)
        
###################################################################################        
        
    def optimizationFunction(self,r, D, a1, a2, a3):
        self.D = D
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        
        return self.implementation(r)
        