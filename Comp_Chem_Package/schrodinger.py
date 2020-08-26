#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University

#Class to solve the Schrodinger Equation and provide a solution to said equation

from compChemGlobal import *
import operators
from graphable import *
import numpy as np
from wavefunction import *

class schrod(Graphable):
    
    #declare global variables here
    eigenValues = None 
    eigenVectors = None
    basis = None
    
    def __init__(self, arg1=None, basis=None, pes=None):

        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavenumbers"
        self.isGraphable = False
        
        if(type(arg1) == operators.HOperator):
            self.solve(arg1, basis, pes)

###################################################################################

    def solve(self, H, basis, pes=None):
        
        self.graphTitle = basis.diatomicConstants["name"] + " Schrödinger Solution"
        
        ev, evc = eigh(H.matrix)
        
        self.wavefunctions = []
        self.eigenVectors = evc 
        self.eigenValues = ev
        self.basis = basis
        
        for index, vector in enumerate(evc):
            wf = wavefunction(vector, ev[index], basis, index).scale()            
            wf.forcedEnd = None if pes == None else 3
            self.addGraphableObject(wf)
        
        if(pes != None):
            self.start = pes.start
            self.addGraphableObject(pes)
        
###################################################################################

    def value(self, r):
        return False

###################################################################################

    def getWaveFunctions(self):
        return [wavefunction(vector, self.eigenValues[index], self.basis, index) for index, vector in enumerate(self.eigenVectors)]
            