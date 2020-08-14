#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Abstract class that specifies the methods all individual wavefunctions must have

#Also imports the compChemGlobal class here to allow its constants and functions to be accessed from all the derviving child subclasses

from abc import ABC, abstractmethod
from compChemGlobal import *

class basisFunction(ABC):
    
    #Declare all global variables here
    functionName = ""
    
    @abstractmethod
    def __init__(self, diatomicConstants, n):
        super().__init__()
        self.functionName = "Basis Function Name"
    
   ###################################################################################
    
    #computes the value of the wavefunction at the specified value of r
    #r will be in units of Angstroms
    #output must be in units of 1 / Sqrt(Angstroms)
    @abstractmethod
    def compute(self, r):
        pass
    
    ###################################################################################

    def computeSquare(self, r):
        return self.compute(r) ** 2
    
    ###################################################################################
    
    #graphs the wavefunction
    #figure bool that represents weather or not the graph or figure trace should be added to a figure object
    def graph(self, showGraph=True, squared=False, resolution=100, start=0.8, end=1.5, precision=2):
        
        if(showGraph):
            figure = plot.go.FigureWidget(layout = dict(
                                       title_text = self.functionName + " Basis Function",
                                       xaxis_title = "r in Angstroms", 
                                       yaxis_title = "Basis Function Output"),
                                       data = [self.internalGraph(resolution=resolution, precision=precision, 
                                                                  start=start, end=end), 
                                               self.internalGraph(resolution=resolution, precision=precision, 
                                                                  start=start, end=end, squared=True)], 
                                       layout_showlegend = True 
                                       )
            figure.data[-1].visible = False
            
            display(self.getFigureWidgets(figure, [figure.data[-2], figure.data[-1]], 
                                         resolution=resolution, start=start, end=end, precision=precision))
            
        else:
            return self.internalGraph(squared=squared, resolution=resolution, start=start, end=end, precision=precision)
        
    ###################################################################################
    
    def internalGraph(self, resolution=100, precision=2, start=1, end=3, squared=False):
        
        traces = []
        
        if(squared):
            func = lambda r: self.compute(r) ** 2
            titleModifier = " Squared"
        else:
            func = self.compute
            titleModifier = ""
        
        return plot.graphFunction(func, 
                                  resolution = resolution,  precision = precision, 
                                  start = start, end = end, 
                                  xTitle = "r", yTitle = "Ψ(r)", 
                                  title = self.functionName + titleModifier)
        
    ###################################################################################
    
    def getFigureWidgets(self, figure, traces, functions=[], resolution=100, start=.25, end=3, precision=2):
        
            if(len(functions) == 0):
                functions = [self.compute, lambda r: self.compute(r) ** 2]
        
            figureWidgets = plot.getGraphFunctionWidgets(figure, traces, functions,
                                                         resolution=resolution, start=start,
                                                         end=end, precision=precision
                                                        )
            
            probability = widgets.Dropdown(
                options = ["Standard", "Probability Distribution", "Standard & Probability"],
                description = '<p style="font-family:verdana;font-size:15px">Mode</p>'
            )
            
            figureWidgets.children[2].children += tuple([probability])
            
            widgetUpdate = lambda change: self.widgetUpdate(traces, probability.value)
            probability.observe(widgetUpdate, "value")
            
            return figureWidgets
        
    ###################################################################################
    
    def widgetUpdate(self, traces, value):
        
        for index, trace in enumerate(traces):
              
            if("!" not in trace["uid"]):
                if(index % 2 == 0):
                    if("Standard" in value):
                         trace.visible = True
                         trace["uid"] = trace["uid"].replace("mode", "") 
                    elif("mode" not in trace["uid"]):
                        trace.visible = False
                        trace["uid"] += "mode"
                else:
                    if("Probability" in value):
                        trace.visible = True
                        trace["uid"] = trace["uid"].replace("mode", "")
                    elif("mode" not in trace["uid"]):
                        trace.visible = False
                        trace["uid"] += "mode"
                        
    ###################################################################################
    
    def __call__(self, r):
        return self.compute(r)