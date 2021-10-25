#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Concrete class to implement the Harmonic Oscillator Wavefunction

from basisFunction import *
from compChemGlobal import np

class how(basisFunction):

    #Global variables
    n = 0
    re = 0
    alpha = 0
    constant = 0
    expConstant = 0
    zeroCutoff = 1e-5
    
    #Private Variables
    startR = -1.8
    endR = 3.4
    
    def __init__(self, diatomicConstants, n):
        self.graphableData = []
        self.graphableObjects = []
        self.n = n
        self.re = diatomicConstants["re"]
        
        self.name = "Harmonic Oscillator"
        self.graphTitle = "Harmonic Oscillator n=" + str(n)
        self.xTitle = "Angstroms"
        self.yTitle = "Inverse Square Root Angstrom"
        
        #calculate alpha and then the constant for the wavefunction
        self.alpha = (diatomicConstants["w"] * 200 * pi * c * diatomicConstants["u"]) / (hbar * 6.022 * pow(10, 46))
        
        self.constant = (pow(self.alpha/pi, 0.25)) / (superSqrt( pow(2, n) * factorial(n)))
        self.expConstant = -self.alpha / 2
        
        #self.start = round(diatomicConstants["re"] - sqrt(-2 * log(pow(10, -10-n)) / self.alpha), 2)
        #self.end = round(-self.start + 2*diatomicConstants["re"], 2)
    
###################################################################################
    
    def value(self, r):
        
        if(r >= self.endR or r <= self.startR):
            return 0
        
        r = r-self.re
        return self.constant * hermitePolynomials(self.n, superSqrt(self.alpha)*r) * exp(self.expConstant * pow(r,2))
    
###################################################################################
    
    #KE analytic equation originates from Dr. Jerry LaRue's Matematica Notebook for Diatomic Molecules
    def kineticEnergy(self, basisSet):
        T = np.zeros([basisSet.size, basisSet.size])
        for i in range(basisSet.size):
            T[i, i] = diagTerm = 2*i + 1
            if(i + 2 < basisSet.size):
                T[i, i + 2] = -sqrt( (i + 1) * (i + 2))
            if(i >= 2):
                T[i, i - 2] = -sqrt( i * (i - 1)) 
                
        return T * basisSet.diatomicConstants["w"] / 4