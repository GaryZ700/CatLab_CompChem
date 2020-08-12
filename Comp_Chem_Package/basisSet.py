#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Class that specifies the methods and functionality of a basis set composed of basisfunctions

from compChemGlobal import plot, widgets
from how import *

class basisSet():
    
    #Declare all global variables here
    basisFunctionClass = 0
    size = 0
    basisFunctions = []
    diatomicConstants = 0
    
    def __init__(self, diatomicConstants, basisFunctionClass=how, size=10):
        
        self.size = size
        self.basisFunctionClass = basisFunctionClass
        self.diatomicConstants = diatomicConstants
        
        self.buildBasisSet()

    ###################################################################################
    
    def buildBasisSet(self):
        
        self.basisSet = []
        
        for n in range(self.size):
            self.basisFunctions.append(self.basisFunctionClass(self.diatomicConstants, n))  
   
    ###################################################################################
    
    #computes the value of the nth basisfunction at position r
    def compute(self, n, r):
        return self.basisFunctions[n].compute(r)
   
    ###################################################################################
  
    #returns the list of basis functions within the basisSet
    def getBasisSet(self):
        return self.basisFunctions
    
    ###################################################################################

    #returns the nth specified basis function
    def getBasisFunction(self, n):
        return self.basisFunctions[n]
    
    ###################################################################################
    
    def graph(self, showGraph=True, resolution=100, start=0.8, end=1.5, precision=2):
                
        fig = plot.go.FigureWidget(layout=dict(
                                               title="Basis Set", 
                                               xaxis_title = "r in Angstroms", 
                                               yaxis_title = "Basis Function Output",
                                               showlegend = True
                                              ))
        
        traces = [] 
        functions = []
        
        for n in range(self.size):     
            
                #Add regular trace
                fig.add_trace(self.basisFunctions[n].graph(showGraph=False, resolution=resolution, 
                                                           start=start, end=end, precision=precision))
                traces.append(fig.data[-1])
                
                #Add Squared Trace
                squaredTrace = self.basisFunctions[n].graph(showGraph=False, squared=True, resolution=resolution, 
                                                            start=start, end=end, precision=precision)
                squaredTrace.visible = False
                fig.add_trace(squaredTrace)
                traces.append(fig.data[-1])
                
                basisFunction = self.basisFunctions[n]
                functions.append(basisFunction.compute)
                functions.append(basisFunction.computeSquare)
        
                traces[-1]["uid"] = ""
                traces[-2]["uid"] = ""
        
        if(showGraph):
            display(self.getFigureWidgets(
                    fig, traces, functions, resolution, start, end, precision))
        else:
            return traces
        
     ###################################################################################
    
    def getFigureWidgets(self, figure, traces, functions, resolution, start, end, precision):
                
        figureWidgets = self.basisFunctions[0].getFigureWidgets(figure, traces, functions, 
                                                                resolution=resolution, 
                                                                start=start, end=end, 
                                                                precision=precision)
        
        visibleWavefunctions = widgets.Text(
            value = "0-" + str(len(functions) // 2),
            description = '<p style="font-family:verdana;font-size:15px">Visible Ψs</p>'
        )
        visibleWavefunctions.observe(
            lambda change: self.figureWidgetUpdate(visibleWavefunctions.value, traces, figure, change),
                                                   "value"
        )
        
        figureWidgets.children[1].children += tuple([visibleWavefunctions])
        
        return figureWidgets
    
    ###################################################################################
    
    def figureWidgetUpdate(self, value, traces, figure, change):
                        
        visibility = []
                
        try:
            for startEnd in value.split(";"):
                if("-" in startEnd):
                    startEnd = [int(value) for value in startEnd.split("-")]
                    visibility.extend( range(startEnd[0], startEnd[1]+1))
                else:
                    visibility.append(int(startEnd))
        except:
            visibility = [False] * len(traces)
        
        for index, trace in enumerate(traces):     
            index -= (index % 2) + (index // 2)

            if index in visibility: 
                if("mode" not in trace["uid"]):
                    trace.visible = True
                trace["uid"] = trace["uid"].replace("!", "")
            elif("!" not in trace["uid"]):
                trace.visible = False
                trace["uid"] += "!"
 ###################################################################################
    
    def __iter__(self):
        self._index=0
        return self

###################################################################################

    def __next__(self):
        if(self._index == self.size):
            raise StopIteration
        
        self._index += 1
        return self.basisFunctions[self._index-1]