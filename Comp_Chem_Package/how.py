#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Concrete class to implement the Harmonic Oscillator Wavefunction

from basisFunction import *

class how(basisFunction):

    #Global variables
    n = 0
    re = 0
    alpha = 0
    constant = 0
    
    def __init__(self, diatomicConstants, n):
        self.n = n
        self.re = diatomicConstants["re"]
        
        self.name = "Harmonic Oscillator"
        self.graphTitle = "Harmonic Oscillator n=" + str(n)
        self.xTitle = "Angstroms"
        self.yTitle = "Wavenumbers"
        
        #calculate alpha and then the constant for the wavefunction
        self.alpha = (diatomicConstants["w"] * 200 * pi * c * diatomicConstants["u"]) / (hbar * 6.022 * pow(10, 46))
        
        self.constant = (pow(self.alpha/pi, 0.25)) / (superSqrt( pow(2, n) * factorial(n)))
        
        self.start = round(diatomicConstants["re"] - sqrt(-2 * log(pow(10, -10-n)) / self.alpha), 2)
        self.end = round(-self.start + 2*diatomicConstants["re"], 2)
    
    ###################################################################################
    
    def value(self, r):
        r = r-self.re
        return self.constant * hermitePolynomials(self.n, sqrt(self.alpha)*r) * exp(-self.alpha * pow(r,2) / 2)