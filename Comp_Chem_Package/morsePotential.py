#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Morse Potential Implementation, is a child of the PESFitter abstract class

#All code in this file based upon theory from Diatomic Molecules According to the Wave Mechanics. II. Vibrational Levels, by Philip M. Morse, and Franck-Condon Factors, R-Centroids, Electronic Transition Moments, and Einstein Coefficients for Many Nitrogen and Oxygen Band Systems, by F.R. Gilmore, R.R. Laher, and P.J. Espy

from diatomicPotential import *

class morsePotential(DiatomicPotential):
    
    #Declare and override global variables as needed here
    name = "Morse Potential"
    a = []
    PESData = []
    
    def implementation(self, r):
        a = self.a[self.a.index(min(self.PESData["r"], key = lambda i : abs(self.PESData["r"][i] - r)))]
        return self.PESData["D"] * ( pow(1 - exp(-a * (r - self.diatomicConstants.re)), 2) - 1)

###################################################################################

    #Fitting method based on the method described in 
    #Franck-Condon Factors, R-Centroids, Electronic Transition Moments, 
    #and Einstein Coefficients for Many Nitrogen and Oxygen Band Systems, 
    #by F.R. Gilmore, R.R. Laher, and P.J. Espy
    def internalFit(self, data):
        
        self.PESData = data
        
        for index, r in enumerate(data["r"]):
            
            squareRoot = sqrt(data["E"][index] / self.D)
            if(r > self.diatomicConstants.re and squareRoot != 1):
                squareRoot *= -1
            
            self.a.append( -log(1 + squareRoot) / (r - self.diatomicConstants.re) ) 

###################################################################################

    def getWidgets(self):
        return False