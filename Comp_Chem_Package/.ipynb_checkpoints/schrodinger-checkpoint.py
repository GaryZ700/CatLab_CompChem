#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University

#Class to solve the Schrodinger Equation and provide a solution to said equation

from compChemGlobal import plot
from operators import *
from graphable import *
import numpy as np

class schrod():
    
    #declare global variables here
    wavefunctions = None
    eigenValues = None 
    eigenVectors = None
    
    def __init__(self, arg1, basis):
        
        if(type(arg1) == str):
            pass
        elif(type(arg1) == H):
            self.solve(arg1, basis)

###################################################################################

    def solve(self, H, basis):
        
        print(H.matrix)
        ev, evc = eigh(H.matrix)
        
        self.wavefunctions = []
        self.eigenVectors = evc 
        self.eigenValues = ev
        self.basis = basis
            
###################################################################################

    def graph(self):
        
        data = []
        
        for index, vector in enumerate(self.eigenVectors):
            data.append(plot.graphFunction(lambda r: sum([self.basis[i](r) * vector[i] for i in range(len(vector))]) + index * 5, title = "Wavefunction"))
        
        fig = plot.go.FigureWidget(data=data)
        
        display(fig)