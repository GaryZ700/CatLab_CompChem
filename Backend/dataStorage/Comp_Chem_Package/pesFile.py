#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Concrete class that allows for reading PES files generated outside of the this computational package
#Files must be formatted as follows below in order to use this class: 
#r-value    energy value
#There can be any number of spaces between the bond distance and the energy value,
#but the r-value must be in the left column while the energy values must be in the right column
#Any units can be used for the r-values, and the energy value as long as they 
#are specified in the distance and energy units parameter when the class is created

from pesMethod import *

class pesFile(PESMethod):
    
    def __init__(self, file, distanceUnits, energyUnits):
        
        #check that file can be opened
        try: 
            f = open(file, 'r')
        except: 
            print("Warning! Could not load '" + file + "', and could not properly create PESFile object.")
            return
        
        #parse data
        data = dict(r=[], E=[])
        for lineNumber, line in enumerate(f): 
            line = line.split(" ")
            try: 
                data["r"].append(float(line[0]))
                data["E"].append(float(line[-1]))
            except: 
                print("Error on Line " + str(lineNumber + 1) + ", unable to parse data.")
                print("Please ensure the file is formatted correctly.")
                f.close()
                return
        
        #check if curve is above or below the y-axis
        #and ensure curve is always positive
        minE = min(data["E"])
        if(minE < 0):
            shiftedE = []
            for E in data["E"]:
                shiftedE.append(E - minE)
            data["E"] = shiftedE
            
        data["D"] = max(data["E"])
        self.data = data
        f.close()
        
        #set up graphing variables
        self.graphTitle = f.name.split("\\")[-1].split("/")[-1]
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavenumbers"
            
###################################################################################

    def implementation(self, r):
        return 0

###################################################################################

    def getWidgets(self):
        return False
                             
###################################################################################

    def compute(self, start=None, end=None, resolution=None):
        return self.data
                             
###################################################################################

    def getData(self):
        return self.data