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

        #Set up Graphing Properties
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
            wf = wavefunction(vector, ev[index], basis, index).scale(1).setGraphVariables(
                              startBoundary=pes.value if pes != None else None, 
                              endBoundary= lambda r : pes.value(r + pow(10, 5)) if pes != None else None)
            
            self.addGraphableObject(wf)
        
        if(pes != None):
            self.start = pes.start
            self.end = pes.end
            self.addGraphableObject(pes)
        
###################################################################################

    def value(self, r):
        return False

###################################################################################

    def getWaveFunctions(self):
        return [wavefunction(vector, self.eigenValues[index], self.basis, index) for index, vector in enumerate(self.eigenVectors)]

###################################################################################

    def getWidgets(self, traces, widgetD):
        scaleWidget = widgets.BoundedIntText(
            value = 5, 
            min = 0, 
            step = 1, 
            description = "Scale"
        )
        
        def observationFunction():
            for index, trace in enumerate(traces[:-1]): 
                trace.update(plot.graphFunction(functions[index],
                                                                                title = trace.name,
                                                                                resolution = widgetD[0].value,
                                                                                precision = widgetD[3].value,
                                                                                start = widgetD[1].value, end = widgetD[2].value, startBoundary = self.graphableObjects[index].startBoundary, endBoundary = self.graphableObjects[index].endBoundary))
                                                                                                                    
        scaleWidget.observe(observationFunction, "value")
        
        return [scaleWidget]