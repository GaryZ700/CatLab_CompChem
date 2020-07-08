#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University
#Class that acts as a Quantum Mechanical Wavefunction Object as well as computing the Wavefunctions

import numpy as np
from tqdm import tqdm
from rkr import rkr as RKR
from ipywidgets import HTMLMath
from scipy.misc import derivative as ddx
from scipy.integrate import quad as integrate

class wavefunction:
    
    #Declare All Global Variables Here
    basisSet = []
    coeffs = []
    energies = []
    scaling = []
    maxN = 0
    diatomicConstants = 0
    
    def __init__(self, diatomicConstants=0, V=00, basis=0):
        
        if(diatomicConstants == 0 or V == 0 or basis == 0):
            return
        
        self.buildWavefunction(diatomicConstants, V, basis)
        
#--------------------------------------------------------------------------------

    #Steps to Computing the Wavefunctions
    #Compute Kinetic Energy Matrix Analytically
    #Compute half of Potential Enerrgy Matrix to speed up calculation
    #Compute the Hamiltonian
    #Compute the eigensystem for H
    #Save the values as the desired terms for the basis set
    def buildWavefunction(self, diatomicConstants, V, basis):
        
        self.basisSet = basis
        
        energies, coeffs = np.linalg.eigh( self.buildH(diatomicConstants, V) )
        
        self.energies = energies
        self.coeffs = coeffs.transpose()
    
        self.scaling = [350, energies]
    
        self.maxN = self.basisSet.size
        
        self.diatomicConstants = diatomicConstants
        
#--------------------------------------------------------------------------------    

    #r refers to the value to evaluate the wavefunction at, can be either a list or a single value
    #while n refers to the wavefunction number
    def compute(self, r, n):
        
        #Error Checking
        if(self.maxN == 0):
            print("Warning! Please build the wavefunctions first by using the 'buildWaveFunction(diatomicConstants, V, basis)' method!!")
            return
        if(n < 0 or n > self.maxN):
            print("The specified wavefunction does not exist, ensure your n value is between 0 and " + str(self.maxN) + "!")
            return 
        
        if(type(r)==list):
            
            psiValues = []
            for rValue in r:
                psiValues.append(float(self.internalEquation(rValue, n)))
            return psiValues
        
        else:
            return float(self.internalEquation(r, n))
            
#--------------------------------------------------------------------------------

    #Internally Computes the value of psi for the psi method
    def internalEquation(self, r, n):
        
        value = 0
        
        for index, b in enumerate(self.basisSet.basis):
            value += self.coeffs[n, index] * b(r)
        
        return value * self.scaling[0] + self.scaling[1][n]

#--------------------------------------------------------------------------------

    def buildH(self, diatomicConstants, V):
        
        H = np.zeros([self.basisSet.size]*2)
        
        basisRange = list(range(self.basisSet.size))
        
        for index1 in tqdm(range(self.basisSet.size)):
            b1 = self.basisSet.basis[index1]
            for index2, b2 in enumerate(self.basisSet.basis):
                
                #used to build only the lower triangular portion of the matrix
                if(index2 > index1):
                    continue
                
                #Compute t
                if(index1 == index2):
                    t = 2*index1 + 1
                elif(index1 == index2 + 2):
                    t = -np.sqrt(index1 * (index1-1))
                else:
                    t = 0
                t *= diatomicConstants.w / 4
                
                #Compute v
                integrand = lambda r : b1(r) * V(r) * b2(r)
                v = integrate(integrand, 0, np.inf, epsabs = pow(10, -200), limit = 200)[0]
                
                H[index1, index2] += t + v
                    
        H += np.triu(H.transpose(), 1)
        
        return H
    
#--------------------------------------------------------------------------------

    def graphData(self, resolution=0.01, startPoint=0, endPoint=4, scaleWavefunction=True):
        
        r = list(np.arange(startPoint, endPoint, resolution))
        wavefunctionData = []
        
        print("\nGenerating Wavefunctions")
        for n in tqdm(range(self.maxN)):
            wavefunctionData.append( self.compute(r, n) )
            
        return r, wavefunctionData
    
#--------------------------------------------------------------------------------

    #Displays a table with the Wavefunction energy 
    #and the the percent difference from the Taylor Series approximation for the energy
    def displayEnergy(self):

        rkr = RKR()
        rkr.setDiatomicConstants(self.diatomicConstants)
        
        mathString = "<font size='5'>Energy Levels</font><br>"
        mathString += "<font size='3'>Energy Levels $(n) \qquad$ Energy in $cm^{-1} \qquad$ Difference from Taylor Series Energy <br>"

        for n, energy in enumerate(self.energies):
            mathString += "$\qquad\:" + "{:02d}".format(n) + " \qquad\qquad\quad\;\;\:"
            mathString += "{:.2f}".format(round(energy, 2)) + "\qquad\qquad\quad"
            mathString +=  "{:.4f}".format(round( abs(rkr.E(n) - energy) / rkr.E(n) * 100, 4)) + "$%<br>"

        mathString += "</font>"
        display(HTMLMath(mathString))