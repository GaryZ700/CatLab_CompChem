#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University

#Class to solve the Schrodinger Equation and provide a solution to said equation

from compChemGlobal import *
import operators
from graphable import *
import numpy as np
from wavefunction import *
from line import *
from basisSet import * 
from diatomicPotential import * 
from compChemHelpers import dataToDiatomicPotential

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

    def __init__(self, arg1=None, basis=None, pes=None, maxWaveFunctions=None):
        
        #Set up Graphing Properties
        self.graphableObjects = []
        self.graphableData = []
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavenumbers"
        self.isGraphable = False
        self.wavefunctions = []
        self.pesLocations = []
        self.maxWaveFunctions = maxWaveFunctions
        
        if(type(arg1) == operators.HOperator and basis != None):
            self.solve(arg1, basis, pes)

###################################################################################

    def solve(self, H, basis, pes=None):
                
        ev, evc = eigh(H.matrix)
        
        self.wavefunctions = []
        self.eigenVectors = evc 
        self.eigenValues = ev
        self.basis = basis
        self.pes = pes

        self.buildWavefunctions()
        
###################################################################################

    def buildWavefunctions(self):        
        self.graphTitle = self.basis.diatomicConstants["name"] + " Schrödinger Solution"

        #check if scale factor is provided or if it needs to be computed from scratch
        if(self.scaleFactor == None):
            if(self.basis.size == 1):
                self.scaleFactor = 500
            else: 
                self.scaleFactor = (self.eigenValues[1] - self.eigenValues[0]) * 0.12

       #All this code here is used soley for graphing and should probably be refactored elsewhere
       #Thinking of updating graphing module so that there is a separate location to make graphing calls and setup
        
        if(self.maxWaveFunctions == None):
            self.maxWaveFunctions = len(self.eigenVectors)    
        
        for index, vector in enumerate(self.eigenVectors[:self.maxWaveFunctions]):
            
            #Allow objects to return two simultaneous traces at the same time
            wf = wavefunction(vector, self.eigenValues[index], self.basis, index).scale(self.scaleFactor)
            wf2 = wavefunction(vector, self.eigenValues[index], self.basis, index, squared=True).scale(self.scaleFactor)
            
            if(self.pes != None):
                wf.setGraphVariables(yEqualsCutoff =  self.eigenValues[index], color = self.color)
                wf2.setGraphVariables(yEqualsCutoff = [self.eigenValues[index]], color = self.color)
            
            self.addGraphableObject(wf)

            self.addGraphableObject(wf2)
            self.wavefunctions.append(wf)
        
        if(self.pes != None):
            self.start = self.pes.start
            self.end = self.pes.end
            self.addGraphableObject(self.pes)
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
            print("Warning! Object passed to conmbine meethod of the Schrodinger class is not a Schrodinger object.\nMethod will quit now.")
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
    
###################################################################################

    def save(self): 
        
        if(self.basis == None):
            print("Can not save an empty Schrödinger solution. Please run the solve method on this object and then run the save method.\n")
            return False
        
        globalDB.connect()
        globalDB.write("schrodinger_solutions", "(molecule, basis, size, eigen_values, eigen_vectors, max_wavefunctions, pes, method)", "(?,?,?,?,?,?,?,?)", 
                       (self.basis.diatomicConstants["name"], self.basis[0].name, self.basis.size, 
                        globalDB.flatArrayToDB(self.eigenValues), globalDB.arrayToDB(self.eigenVectors),
                        self.maxWaveFunctions, "None" if self.pes == None else self.pes.name, 
                        "None" if self.pes == None else self.pes.pesData["method"]
                       )
                      )
        globalDB.close()
        
        globalDB.writeDiatomicConstants(self.basis.diatomicConstants)
        if(self.pes != None):
            self.pes.save()

        return True
    
###################################################################################

    def load(self, molecule, basis, size, pes, method, scaleFactor = None, color = None):
        globalDB.connect()
        print("MOLECULE", molecule)
        data = globalDB.getData("schrodinger_solutions", ["molecule", "basis", "size", "pes", "method"], [molecule, basis, size, pes, method])
        
        if(data == []):
            print("A Schrödinger solution for " + molecule + " with a " + basis + " basis set of size " + str(size) + " was not found in the database.")
            return False
        else: 
            #load data from database into the schrod solution object
            data = data[0]
            self.eigenValues = globalDB.dbToFlatArray(data[3])
            self.eigenVectors = globalDB.dbToArray(data[4])
            self.basis = basisSet(globalDB.getDiatomicConstants(molecule), basisFunctionClass = basis, size = data[2])
            self.pes = dataToDiatomicPotential(data[6])
            self.maxWaveFunctions = data[5]

        globalDB.close()
        if(self.pes != None):
            self.pes = self.pes()
            self.pes.load(molecule, data[7])
            self.pes.color = color
    
        self.scaleFactor = scaleFactor
        self.color = color
        self.buildWavefunctions()
        return True