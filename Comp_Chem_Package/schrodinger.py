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
    
    def __init__(self, arg1=None, basis=None, pes=None):

        #Set up Graphing Properties
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavenumbers"
        self.resolution = 100
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
        
        startBoundary =  lambda r : pes.value(r-1) if pes != None else None
        endBoundary = lambda r : pes.value(r + 1000) if pes != None else None
        
        for index, vector in enumerate(evc):
            
            group = self.graphTitle + str(index)
            groupSquared = group + "S"
            graphCondition = None if pes == None else lambda x, y : (abs(y - 7) > 1)

            
            startBoundary =  None
            endBoundary = None
            
            #!!!TO DO TASK HERE!!
            #Allow objects to return two simultaneous traces at the same time
            wf = wavefunction(vector, ev[index], basis, index).scale(1).setGraphVariables(group = group, 
                                                                                          graphCondition=graphCondition).scale(5)
            
            wf2 = wavefunction(vector, ev[index], basis, index, squared=True).scale(1).setGraphVariables( group = groupSquared, 
                                                                                                    graphCondition = graphCondition).scale(5)
            
            lineGraphCondition = None if pes == None else lambda x, y : abs(wf.value(x) - y) > 0.00001 or wf.value(x) > pes.value(x)

            self.addGraphableObject(line(m = 0, b = ev[index]).setGraphVariables(graphTitle=wf.graphTitle + " Energy", startBoundary = startBoundary, 
                                                                                 endBoundary = endBoundary, group = group, graphCondition = lineGraphCondition))            
            self.addGraphableObject(wf)
            
            self.addGraphableObject(line(m=0, b=ev[index]).setGraphVariables(graphTitle=wf2.graphTitle + " Energy", startBoundary = startBoundary, graphCondition = lineGraphCondition))
                                    
            self.addGraphableObject(wf2)
        
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
        
        #remove the pes from the list of traces
        completeTraces = traces[1::]
        traces = traces[1::2]
        
        #Scale Wavefunctions up or down to better be viewed when bound by the PES
        scaleWidget = widgets.BoundedIntText(
            value = 5, 
            min = 0, 
            max = pow(10, 10),
            step = 1, 
            description = '<p style="font-family:verdana;font-size:15px">Scale</p>'
        )
        
        #textbook used to show or hide wavefunctions
        visibleWavefunctions = widgets.Text(
            value = "0-" + str(len(traces) // 2),
            description = '<p style="font-family:verdana;font-size:15px">Visible Ψs</p>'
        )
        
        probability = widgets.Dropdown( options = ["Standard", 
                                                   "Probability Distribution", 
                                                   "Standard & Probability"],
        description = '<p style="font-family:verdana;font-size:15px">Mode</p>')
        
        def scaleUpdate(value):
            index = 1
            for trace in completeTraces: 
            
                #check if dealing with an actual wavefunction or an energy line
                if(index % 2 == 1):
                    self.graphableObjects[index].scale(scaleWidget.value).value
                
                trace.update(plot.graphFunction(self.graphableObjects[index].value,
                                                title = trace.name,
                                                resolution = widgetD[0].value,
                                                precision = widgetD[3].value,
                                                start = widgetD[1].value, 
                                                end = widgetD[2].value, 
                                                startBoundary = self.graphableObjects[index].startBoundary, 
                                                endBoundary = self.graphableObjects[index].endBoundary))
                index += 1
                                                            
        
        def visibleWavefunctionsUpdate(value, modeValue):               
            visibility = []
            revCompleteTraces = completeTraces[::-1]
            
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
            
            for index, trace in enumerate(traces[::-1]):     
                visibleType = index % 2
                index2 = index - visibleType - index // 2
                
                if index2 in visibility and visibleType ^ mode: 
                    trace.visible = True
                    
                else:
                    trace.visible = False
                
                #change visib of energy line
                revCompleteTraces[2*index].visible = trace.visible
            
        scaleWidget.observe(scaleUpdate, names=["value"])
        
        vsfWrapper = lambda value : visibleWavefunctionsUpdate(visibleWavefunctions.value, 
                                                               probability.value)

        vsfWrapper(0)
        visibleWavefunctions.observe(vsfWrapper)
        probability.observe(vsfWrapper)
        
        
        return [[visibleWavefunctions, scaleWidget], [probability]]
    
#  def getFigureWidgets(self, figure, traces, functions, resolution, start, end, precision):
                
#         figureWidgets = self.basisFunctions[0].getFigureWidgets(figure, traces, functions, 
#                                                                 resolution=resolution, 
#                                                                 start=start, end=end, 
#                                                                 precision=precision)
        
#         visibleWavefunctions = widgets.Text(
#             value = "0-" + str(len(functions) // 2),
#             description = '<p style="font-family:verdana;font-size:15px">Visible Ψs</p>'
#         )
#         visibleWavefunctions.observe(
#             lambda change: self.figureWidgetUpdate(visibleWavefunctions.value, traces, figure, change),
#                                                    "value"
#         )
        
#         figureWidgets.children[1].children += tuple([visibleWavefunctions])
        
#         return figureWidgets
    
#     ###################################################################################
    
#     def figureWidgetUpdate(self, value, traces, figure, change):
                        
#         visibility = []
                
#         try:
#             for startEnd in value.split(";"):
#                 if("-" in startEnd):
#                     startEnd = [int(value) for value in startEnd.split("-")]
#                     visibility.extend( range(startEnd[0], startEnd[1]+1))
#                 else:
#                     visibility.append(int(startEnd))
#         except:
#             visibility = [False] * len(traces)
        
#         for index, trace in enumerate(traces):     
#             index -= (index % 2) + (index // 2)

#             if index in visibility: 
#                 if("mode" not in trace["uid"]):
#                     trace.visible = True
#                 trace["uid"] = trace["uid"].replace("!", "")
#             elif("!" not in trace["uid"]):
#                 trace.visible = False
#                 trace["uid"] += "!"