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
    pes = None
    maxWaveFunctions = None
    scaleFactor = None
    pesLocations = []
    wavefunctions = []

    def __init__(self, arg1=None, basis=None, pes=None):
        
        #Set up Graphing Properties
        self.graphableObjects = []
        self.graphableData = []
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavenumbers"
        self.isGraphable = False
        self.wavefunctions = []
        self.pesLocations = []
        
        if(type(arg1) == operators.HOperator and basis != None):
            self.solve(arg1, basis, pes)

###################################################################################

    def solve(self, H, basis, pes=None):
        
        self.graphTitle = basis.diatomicConstants["name"] + " Schrödinger Solution"
        
        ev, evc = eigh(H.matrix)
        
        self.wavefunctions = []
        self.eigenVectors = evc 
        self.eigenValues = ev
        self.basis = basis
        self.pes = pes
        
        if(basis.size == 1):
            self.scaleFactor = 500
        else: 
            self.scaleFactor = (ev[1] - ev[0]) * 0.12

       #All this code here is used soley for graphing and should probably be refactored elsewhere
       #Thinking of updating graphing module so that there is a separate location to make graphing calls and setup
        
        if(self.maxWaveFunctions == None):
            self.maxWaveFunctions = len(evc)    
        
        for index, vector in enumerate(evc[:self.maxWaveFunctions]):
            
            #Allow objects to return two simultaneous traces at the same time
            wf = wavefunction(vector, ev[index], basis, index).scale(self.scaleFactor)
            wf2 = wavefunction(vector, ev[index], basis, index, squared=True).scale(self.scaleFactor)
            
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
            self.pesLocations.append(len(self.graphableObjects) - 1)
        else:
            self.pesLocations = [-1]
            
                    
###################################################################################

    def value(self, r):
        return False

###################################################################################

    def getWaveFunctions(self):
        return self.wavefunctions

###################################################################################

    #combines this objects solution with the solution of another solved schrodinger object
    #sol refers to the other solved schordinger object
    #nameModifier refers to a string value that will be used to distingish the first solution from the second solution
    def combineSolutions(self, sol, nameModifier):
        if(type(sol) != schrod):
            print("Warning! Object passed to conmbine meethod of the Schrodinger class is not a Schrodinger object.\n Method will quit now.")
            return 

        self.graphableObjects.extend( [obj.setGraphVariables(graphTitle = obj.graphTitle + nameModifier) for obj in sol.graphableObjects] )
        
        if(len(sol.graphableObjects) % 2 != 0):
            self.pesLocations.append(len(self.graphableObjects) - 1)

###################################################################################

    def getWidgets(self, traces, widgetD):
                
        traces = list(traces)[::-1]
        if(self.pesLocations[0] !=  -1):
            for offSet, pesIndex in enumerate(self.pesLocations): 
                del traces[pesIndex - offSet]
        revTraces = traces
        traces = traces[::-1]
        
        #for trace in revTraces: 
        #    print(trace["name"])
        
        pesLocationsSize = len(self.pesLocations) 
        
        #Scale Wavefunctions up or down to better be viewed when bound by the PES
        scaleWidget = widgets.BoundedIntText(
            value = self.scaleFactor, 
            min = 0, 
            max = pow(10, 10),
            step = 1, 
            description = '<p style="font-family:verdana;font-size:15px">Scale</p>'
        )
        
        #textbox used to show or hide wavefunctions
        visibleWavefunctions = widgets.Text(
            value = "0-" + str(len(traces) // ( (2 * pesLocationsSize) if (pesLocationsSize != 0) else 2) - pesLocationsSize),
            description = '<p style="font-family:verdana;font-size:15px">Visible Ψs</p>'
        )
        
        probability = widgets.Dropdown( options = ["Standard", 
                                                   "Probability Distribution", 
                                                   "Standard & Probability"],
        description = '<p style="font-family:verdana;font-size:15px">Mode</p>')
        
        def scaleUpdate(value):
            
            #remove pes objects
            pesLocations = [val - self.pesLocations[0] for val in self.pesLocations] if self.pesLocations[0] != -1 else []
            graphableObjects = [obj for index, obj in enumerate(self.graphableObjects) if (index not in pesLocations)]
                
            self.scaleFactor = value["new"] / value["old"]
            for index, wavefunction in enumerate(graphableObjects): 
                traces[index].update(
                    {"y" : [ (y - wavefunction.energy) * self.scaleFactor + wavefunction.energy for y in traces[index].y]}
                )
        def visibleWavefunctionsUpdate(value, modeValue):
         
            visibility = []
            
            try:
                for startEnd in value.split(";"):
                    if("-" in startEnd):
                        startEnd = [int(value) for value in startEnd.split("-")]
                        for offset in self.pesLocations: 
                            offset -= self.pesLocations[0]
                            visibility.extend(range(startEnd[0] + offset, startEnd[1]+1+offset))
                    else:
                        value = int(startEnd)
                        visibility.extend([value + offset - self.pesLocations[0] for offset in self.pesLocations])
            except:
                return 
            
            if (modeValue == "Standard"):
                mode = 1
            elif (modeValue == "Probability Distribution"):
                mode = 0
            else:
                mode = 2

          
            pesOffset = 0
            offsetIndex = 0
            for index, trace in enumerate(revTraces):
                if(pesLocationsSize != offsetIndex and index == self.pesLocations[offsetIndex]):
                    pesOffset += self.pesLocations[offsetIndex]
                    offsetIndex += 1
                index -= pesOffset

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