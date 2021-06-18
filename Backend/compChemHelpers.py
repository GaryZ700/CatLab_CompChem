#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#File to contain general helper functions for the CompChem Library, 
#such as functions that convert strings to the appropriate constructor

#import statements go here
from how import * 
from morsePotential import * 
from howPotential import * 

#used to convert data, such as a string, into the class definition of the 
#associated basis function
def dataToBasisFunction(data):
    if(type(data) == str):
        if(data == "Harmonic Oscillator"):
            return how
        else: 
            return None
    else:
        return data
    
#Used to convert data, such as a string, into the class definition of the 
#associated diatomic potential
def dataToDiatomicPotential(data):
    if(type(data) == str):
        if(data == "Harmonic Oscillator PES"):
            return howPotential
        elif(data == "Morse Potential"):
            return morsePotential
        else: 
            return None
    else: 
        return data