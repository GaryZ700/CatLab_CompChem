#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Class to create a potential energy surface given a computation and fitting method

from compChemComputation import *

class potentialEnergySurface():
    
    #Declare all global variables here
    fitting = 0
    
    def __init__(self, method=rkr, fitting=morse):
        self.fitting = fitting
        
        self.fitting.fit(method)
        
###################################################################################

    def graph(self, showGraph=True):
        
        title = self.fitting.name + " fit " + self.method.name + "PES"
        trace = plot.graphFunction(self.compute, title)
        
        if(showGraph):
            fig = plot.Figure(title, layout_showlegend=True)
            fig.add_trace(trace)
            
            display(plot.getGraphFunctionWidgets(fig, [trace], [self.compute]))
            
        else:
            return trace
        
###################################################################################

    def compute(self, r):
        return self.fitting(r)
        