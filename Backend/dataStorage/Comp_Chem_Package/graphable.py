#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University

#Graphable Abstract class to provide a common interface for all graphable objects in the CompChem Library

from abc import ABC, abstractmethod
from compChemGlobal import plot
from plot import graphingParameters
from plot import parallelGraphing
from plot import cpu_count
from plot import graphObjects

class Graphable(ABC):
    
    #Declare all global variables here that should be modified in the child class 
    #to better reflect the actual titles
    
    #Graph/Trace Information
    graphTitle = "Generic & Unoriginal Graph Name"
    xTitle = "x"
    yTitle = "y"
    dash = "solid"
    group = ""
    fill = "none"
    yEqualsCutoff = None
    
    #Graphing Parameters
    #for default widgets
    precision = 2
    resolution = "Medium"
    start = 0 
    end = 5

    #Graphing data
    #Objects refer to other graphable objects, 
    #while graphableData refers to raw data to graph
    #lastly, graphedData refers to data that has been alreadly graphed but is stored here
    #to speed up graphing changes that are made
    graphableObjects = []
    graphableData = []
    graphedData = []
    highestResData = []
    firstGraph = True
    
    #Graphable Settings
    #is graphable refers to weather this object itself has the abillity to graph, or 
    #is simply a container object to allow other objects to be graphed
    isGraphable = True
    
    #Provide appropriate values for the global variables here in the child class
    #Make sure to call super in order or include the below two lines 
    #to avoid issues with Python's memory mangement system
    @abstractmethod
    def __init__(self):
        
        #add in all objects that are graphable to this list in order to add their graphs to the graph  generated by this object
        #Need to make sure to clear this in the init in the child class to avoid memory issues with Python
        self.graphableObjects = []
        self.graphableData = []
        
    
###################################################################################

    #compute method that must be somewhere in the parent class in order to allow for graphing to occur
    #if object is not graphable, then still must be included but simply put pass for the return value
    #and set isGraphable to false
    @abstractmethod
    def value(self, r):
        pass

###################################################################################

    #method to return a list of widgets for this graphable object
    #if the graphable object is to have widgets beyond those which normally 
    #come with graphable objects
    #traces refers to the traces of the figure
    #widgets refers to the other widgets on the figure
    def getWidgets(self, traces = None, widgets = None):
        return False
    
###################################################################################

    #showGraph: if True, graph wil be generated, if False, graph trace will be returned instead
    #showGraph: if false, dictionary of x,y data will be returned instead
    #getGraph refers to weather or not a reference to the graph object is returned
    #**kwargs refers to parameters that can modify the graph settings, and are run 
    #through setGraphVariables
    def graph(self, showGraph=True, getGraph=False, **kargs):
        
        if(bool(kargs)):
            self.setGraphVariables(_dictData_ = kargs)
        
        if(self.isGraphable and self.firstGraph):
             self.graphableObjects.append(self)
             self.firstGraph = False
        
        traces, functions = graphObjects(self.graphableObjects, precision = self.precision, resolution = plot.resolutionValue[self.resolution], start = self.start, end = self.end)
        print("graph objects called")
        
        
        #Add graphable data
        traces.extend(self.graphableData)
        
        if(not showGraph):
            return traces[0]
        
        return self.buildGraph(traces, functions, getGraph) 
    
###################################################################################

    #This is a private function that should not be overriden in the child class
    #get graph refers to weather or not a reference to the graph object should be returned as well
    def buildGraph(self, data, functions, getGraph=False):
         
        fig = plot.go.FigureWidget(layout = dict( xaxis_title = self.xTitle, 
                                                  yaxis_title = self.yTitle, 
                                                  title_text = self.graphTitle
                                                ), 
                                   data = data
                                  )
        
        widgetData = plot.getGraphFunctionWidgets(fig, fig.data, functions, 
                                             start=self.start, end=self.end, precision=self.precision, returnWidgets=True, graphableData=len(self.graphableData), graphableObjects = self.graphableObjects)
        
        graph = widgetData[0]
        
        parentWidgets = self.getWidgets(graph.children[0].data, widgetData[1])
        print(len(graph.children[0].data))
        if(parentWidgets != False):
            for widgetList in parentWidgets:
                if(widgetList == False):
                    continue

                if(type(widgetList[-1]) == int):
                    index = widgetList.pop() + 1
                else:
                    index = -1
                
                if(index == -1):
                    graph.children += tuple([plot.widgets.HBox([])])
                
                graph.children[index].children += tuple(widgetList)
        
        if(getGraph):
            return graph
        else:
            display(graph)
            return self
        
###################################################################################

    def addGraphableObject(self, graphableObjects):
        
        if(type(graphableObjects) != list):
            graphableObjects = [graphableObjects]
            
        graphableObjects.extend(self.graphableObjects)
        self.graphableObjects = graphableObjects
        
###################################################################################

    def addGraphableData(self, graphableData, title):
        graphableData = [plot.buildTrace(x=graphableData["x"], y=graphableData["y"], title=title, 
                                                  precision=self.precision, xTitle=self.xTitle, 
                                                  yTitle=self.yTitle, mode="markers")]
        graphableData.extend(self.graphableData)
        self.graphableData = graphableData
        
###################################################################################
    
    def setGraphVariables(self, **kargs):
        
        if ("_dictData_" in kargs): 
            kargs = kargs["_dictData_"]
        
        for name in kargs: 
            try:
                getattr(self, name)
                setattr(self, name, kargs[name])
            except:
                print("'" + name + "' is not present in the current object and can not be modified.")
              
        return self