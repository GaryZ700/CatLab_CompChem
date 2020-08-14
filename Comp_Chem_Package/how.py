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
        
        self.functionName = "Harmonic Oscillator n=" + str(n)
        
        #calculate alpha and then the constant for the wavefunction
        self.alpha = (diatomicConstants["w"] * 200 * pi * c * diatomicConstants["u"]) / (hbar * 6.022 * pow(10, 46))
        
        self.constant = (pow(self.alpha/pi, 0.25)) / (superSqrt( pow(2, n) * factorial(n)))
    
    ###################################################################################
    
    def compute(self, r):
        r = r-self.re
        return self.constant * hermitePolynomials(self.n, sqrt(self.alpha)*r) * exp(-self.alpha * pow(r,2) / 2)