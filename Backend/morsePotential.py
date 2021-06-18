#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Morse Potential Implementation, is a child of the PESFitter abstract class

#All code in this file based upon theory from Diatomic Molecules According to the Wave Mechanics. II. Vibrational Levels, by Philip M. Morse, and Franck-Condon Factors, R-Centroids, Electronic Transition Moments, and Einstein Coefficients for Many Nitrogen and Oxygen Band Systems, by F.R. Gilmore, R.R. Laher, and P.J. Espy

from diatomicPotential import *

class morsePotential(DiatomicPotential):
    
    #Declare and override global variables as needed here
    name = "Morse Potential"
    a = None
    pesData = []
    end = 20
    
    def implementation(self, r):
        aValue = self.a[self.pesData["r"].index(min(self.pesData["r"], key = lambda rTest : abs(rTest - r)))]
        
        return self.pesData["D"] if aValue == 0 else self.pesData["D"] * pow(1 - exp(-aValue * (r - self.diatomicConstants["re"])), 2) 
    
###################################################################################
             
    def invert(self, r, answer):
        return 

###################################################################################

    #Fitting method based on the method described in 
    #Franck-Condon Factors, R-Centroids, Electronic Transition Moments, 
    #and Einstein Coefficients for Many Nitrogen and Oxygen Band Systems, 
    #by F.R. Gilmore, R.R. Laher, and P.J. Espy
    def internalFit(self, data):
        
        self.pesData = data
        self.a = []
        
        for index, r in enumerate(data["r"]):
            
            if(data["E"][index] == 0):
                self.a.append(1)
                continue
            
            squareRoot = sqrt(data["E"][index] / self.pesData["D"])
            if(squareRoot == 1):
                self.a.append(0)
                continue
                
            if(r > self.diatomicConstants["re"]):
                squareRoot *= -1

            self.a.append( -log(1 + squareRoot) / (r - self.diatomicConstants["re"]) )

###################################################################################

    def getWidgets(self, a, b):
        return False
    
###################################################################################

    def save(self):
        if (not super().save()):
            return False
        
        globalDB.connect()
        globalDB.write("morse_potentials", "(molecule, method, a)", "(?, ?, ?)", 
                       (self.diatomicConstants["name"], self.pesData["method"], 
                        globalDB.flatArrayToDB(self.a)))
        globalDB.close()
        
        return True
    
###################################################################################

    def load(self, molecule, method):
        if(not super().load(molecule, method)):
            return False
        
        globalDB.connect()
        
        data = globalDB.getData("morse_potentials", ["molecule", "method"], [molecule, method])
        if(data == []):
            return False
        self.a = list(globalDB.dbToFlatArray(data[0][2]))
        globalDB.close()
        
        return True