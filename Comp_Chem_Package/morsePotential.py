#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Morse Potential Implementation, is a child of the PESFitter abstract class

#All code in this file based upon theory from Diatomic Molecules According to the Wave Mechanics. II. Vibrational Levels, by Philip M. Morse, and Franck-Condon Factors, R-Centroids, Electronic Transition Moments, and Einstein Coefficients for Many Nitrogen and Oxygen Band Systems, by F.R. Gilmore, R.R. Laher, and P.J. Espy

from PESFitter import *

class morsePotential(PESFitter):
    
    #Declare and override global variables as needed here
    name = "Morse Potential"
    a = []
    D = 0
    
    def implementation(self, r):
        return self.D * ( pow(1 - exp(-self.a * (r - self.diatomicConstants.re)), 2) - 1)

###################################################################################

    #Fitting method based on the method described in 
    #Franck-Condon Factors, R-Centroids, Electronic Transition Moments, 
    #and Einstein Coefficients for Many Nitrogen and Oxygen Band Systems, 
    #by F.R. Gilmore, R.R. Laher, and P.J. Espy
    def internalFit(self, data):
        
        #Get the Well Depth
        self.D = data["E"][data["r"].index(max(data["r"]))] - min(data["E"])
        
        for index, r in enumerate(data["r"]):
            
            E = data["E"][index]
            
            