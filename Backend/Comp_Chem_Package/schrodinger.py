#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University

#Class to solve the Schrodinger Equation and provide a solution to said equation

from compChemGlobal import *
import operators
from graphable import *
import numpy as np
from wavefunction import *
from line import *

class schrod(Graphable):
    
    #declare global variables here
    eigenValues = None 
    eigenVectors = None
    basis = None
    maxWaveFunctions = None
    wavefunctions = []
    
    def __init__(self, arg1=None, basis=None, pes=None):
        
        #Set up Graphing Properties
        self.graphableObjects = []
        self.graphableData = []
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavenumbers"
        self.isGraphable = False
        self.wavefunctions = []
        
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
        
        if(basis.size == 1):
            scaleFactor = 500
        else: 
            scaleFactor = (ev[1] - ev[0]) * 0.12

       #All this code here is used soley for graphing and should probably be refactored elsewhere
       #Thinking of updating graphing module so that there is a separate location to make graphing calls and setup
        
        if(self.maxWaveFunctions == None):
            self.maxWaveFunctions = len(evc)    
        
        for index, vector in enumerate(evc[:self.maxWaveFunctions]):
            
            #Allow objects to return two simultaneous traces at the same time
            wf = wavefunction(vector, ev[index], basis, index).scale(scaleFactor)
            wf2 = wavefunction(vector, ev[index], basis, index, squared=True).scale(scaleFactor)
            
            if(pes != None):
                wf.setGraphVariables(yEqualsCutoff = ev[index])
                wf2.setGraphVariables(yEqualsCutoff = ev[index])
            
            self.addGraphableObject(wf)

            self.addGraphableObject(wf2)
            self.wavefunctions.append(wf)
        
        if(pes != None):
            self.start = pes.start
            self.end = pes.end
            self.addGraphableObject(pes)
                    
###################################################################################

    def value(self, r):
        return False

###################################################################################

    def getWaveFunctions(self):

        return self.wavefunctions

###################################################################################

    def getWidgets(self, traces, widgetD):
        
        #remove the pes from the list of traces
        if(len(traces) % 2 != 0):
            traces = traces[1::]
        revTraces = traces[::-1]
        
        #Scale Wavefunctions up or down to better be viewed when bound by the PES
        scaleWidget = widgets.BoundedIntText(
            value = 5, 
            min = 0, 
            max = pow(10, 10),
            step = 1, 
            description = '<p style="font-family:verdana;font-size:15px">Scale</p>'
        )
        
        #textbox used to show or hide wavefunctions
        visibleWavefunctions = widgets.Text(
            value = "0-" + str(len(traces) // 2),
            description = '<p style="font-family:verdana;font-size:15px">Visible Ψs</p>'
        )
        
        probability = widgets.Dropdown( options = ["Standard", 
                                                   "Probability Distribution", 
                                                   "Standard & Probability"],
        description = '<p style="font-family:verdana;font-size:15px">Mode</p>')
        
        def scaleUpdate(value):
            graphableObjects = self.graphableObjects if len(self.graphableObjects) % 2 == 0 else self.graphableObjects[1::]
            scaleFactor = value["new"] / value["old"]
            for index, wavefunction in enumerate(graphableObjects): 
                traces[index].update(
                    {"y" : [ (y - wavefunction.energy) * scaleFactor + wavefunction.energy for y in traces[index].y]}
                )
            
        def visibleWavefunctionsUpdate(value, modeValue):
         
            visibility = []
            
            try:
                for startEnd in value.split(";"):
                    if("-" in startEnd):
                        startEnd = [int(value) for value in startEnd.split("-")]
                        visibility.extend( range(startEnd[0], startEnd[1]+1))
                    else:
                        visibility.append(int(startEnd))
            except:
                return 
            
            if (modeValue == "Standard"):
                mode = 1
            elif (modeValue == "Probability Distribution"):
                mode = 0
            else:
                mode = 2

            for index, trace in enumerate(revTraces):    
                #evens are squared
                #odds are normal
                visibleType = index % 2
                
                #maps square and normal function to a single index
                index2 = index - visibleType - index // 2
        
                if index2 in visibility and visibleType ^ mode: 
                    trace.visible = True
                else:
                    trace.visible = False
            
        scaleWidget.observe(scaleUpdate, names=["value"])
        
        vsfWrapper = lambda value : visibleWavefunctionsUpdate(visibleWavefunctions.value, 
                                                               probability.value)

        vsfWrapper(0)
        visibleWavefunctions.observe(vsfWrapper)
        probability.observe(vsfWrapper)
        
        return [[visibleWavefunctions, scaleWidget, 0], [probability, 1]]