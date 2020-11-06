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
    
    #Graphing Variables
    graphTitle = ""
    start = 0 
    end = 0
    
    def __init__(self, diatomicConstants, basisFunctionClass=how, size=10):
        
        self.size = size
        self.basisFunctionClass = basisFunctionClass
        self.diatomicConstants = diatomicConstants
        
        self.buildBasisSet()
        
 ###################################################################################
    
    def buildBasisSet(self):
        
        self.basisFunctions = []
        
        for n in range(self.size):
            self.basisFunctions.append(self.basisFunctionClass(self.diatomicConstants, n))  
        
        #get needed graphing data
        function =  self.basisFunctions[-1]
        self.graphTitle = function.name + " Basis Set"
        self.start = function.start 
        self.end = function.end
   
    ###################################################################################
    
    #computes the value of the nth basisfunction at position r
    def value(self, n, r):
        
        if(n >= self.size):
            print("Warning! Basis function n=" + str(n) + " can not be found. Max n is " + str(n-1) + ".")
        elif(n < 0):
            print("Warning! Can retrive basis function n=" + str(n) + " lowest n is 0.")
        else:
            return self.basisFunctions[n].value(r)
   
    ###################################################################################
  
    #returns the list of basis functions within the basisSet
    def getBasisSet(self):
        return self.basisFunctions
    
    ###################################################################################

    #returns the nth specified basis function
    def getBasisFunction(self, n):
        return self.basisFunctions[n]
    
    ###################################################################################
    
    def graph(self, showGraph=True, resolution=200, start=None, end=None, precision=2):
                
        if(start == None):
            start = self.start 
        if(end == None):
            end = self.end
    
        fig = plot.go.FigureWidget(layout=dict(
                                               title=self.graphTitle, 
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
                functions.append(basisFunction.value)
                functions.append(basisFunction.squaredValue)
        
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
    
###################################################################################

    class _iterator:
        
        basisSetSelf = None
        index = 0
        
        def __init__(self, basisSetSelf):
            self.basisSetSelf = basisSetSelf
            
        #---------------------------------------------------
        
        def __next__(self):
            if(self.index == self.basisSetSelf.size):
                raise StopIteration
            self.index += 1
            return self.basisSetSelf.basisFunctions[self.index-1]

    def __iter__(self):
        return self._iterator(self)

###################################################################################

    def __len__(self):
        return self.size
    
###################################################################################

    def __getitem__(self, key):
        return self.basisFunctions[key]