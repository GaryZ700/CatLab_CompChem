#Written by Gary Zeri, Computer Science Major at Chapman University and Member of the LaRue CatLab

#RKR Class to Allow for Simple RKR Calcuations as needed
class RKR:
    
    #All Imports Done Here
    import math
    import numpy as np
    from scipy.integrate import quad as integrate
    
    #Declare All Global Variables Here
    
    #Is the distance from v that the integration stops at
    delta = pow(10, -5)

    #Reduced Molecular Mass
    #In Non Hartree Atomic Units, each proton has an amu of 1
    u = 0

    #Diatomic Constants, must be in Wavenumbers (1 / cm)
    we = 0
    wxe = 0
    wye = 0
    wze = 0
    Be = 0
    alphae = 0
    ye = 0
    
    solutions = []

###################################################################################

    def setDiatomicConstants(self, alphae, Be, we, wxe, wye, wze, ye):
        
        self.alphae = alaphe
        self.Be = Be
        self.we = we
        self.wxe = wxe
        self.wye = wye
        self.wze = wze
        self.ye = ye
        
        self.solutions = []
        
###################################################################################

    def setReducedMass(self, u):
        self.u = u
        self.solutions = []
        
###################################################################################

    def setDelta(self, delta):
        self.delta = delta
        
################################################################################### 

    #v refers to the specided energy level for which the turning points should be computed for
    def compute(self, v):
        
        