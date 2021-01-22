#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University

#Graphable Abstract class to provide a common interface for all graphable objects in the CompChem Library

from abc import ABC, abstractmethod
from compChemGlobal import plot
from plot import graphingParameters
from plot import parallelGraphing
from plot import cpu_count

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
    
    #Graphing Parameters
    #for default widgets
    precision = 2
    resolution = 200
    start = 0 
    end = 5

    #Graphing data
    #Objects refer to other graphable objects, 
    #while data refers to raw data to graph
    graphableObjects = []
    graphableData = []
    
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
    #x refers to 
    #y refers to 
    def getWidgets(self, x=None, y=None):
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
        
        if(self.isGraphable):
             self.graphableObjects.append(self)
               
        if(len(self.graphableObjects) > 4 and cpu_count() > 1):
            traces, widgetObjs, functions = parallelGraphing(self.graphableObjects, self.precision, self.resolution, self.start, self.end)
        else: 
            traces = []
            widgetObjs = []
            functions = []
            
            for graphableObject in self.graphableObjects: 
                traces.append(plot.graphFunction(graphableObject.value, title = graphableObject.graphTitle, precision = self.precision, xTitle = graphableObject.xTitle, 
                                            yTitle = graphableObject.yTitle, dash = graphableObject.dash, group = graphableObject.group, 
                                            start = self.start, end = self.end, fill = graphableObject.fill))
                widgetObjs.append(graphableObject.getWidgets(0, 0))
                functions.append(graphableObject.value)
           

        if(not showGraph):
            return traces[0]
        
        return self.buildGraph(traces, widgetObjs, functions, getGraph) 
    
###################################################################################

    #This is a private function that should not be overriden in the child class
    #get graph refers to weather or not a reference to the graph object should be returned as well
    def buildGraph(self, data, widgetObjs, functions, getGraph=False):

        #data, functions, widgetObjs = self.getGraphData(trace, self.value)
         
        fig = plot.go.FigureWidget(layout = dict( xaxis_title = self.xTitle, 
                                                  yaxis_title = self.yTitle, 
                                                  title_text = self.graphTitle
                                                ), 
                                   data = data
                                  )

        widgetData = plot.getGraphFunctionWidgets(fig, fig.data, functions, resolution=self.resolution, 
                                             start=self.start, end=self.end, precision=self.precision, returnWidgets=True, graphableData=len(self.graphableData), graphableObjects = self.graphableObjects)
        
        graph = widgetData[0]
        
        parentWidgets = self.getWidgets(graph.children[0].data, widgetData[1])

        if(parentWidgets != False):
            if(type(parentWidgets[0]) == list):
                for sublist in parentWidgets: 
                    widgetObjs.append(sublist)
            else: 
                widgetObjs.append(parentWidgets)
        
        index = 1
        for widgetList in widgetObjs:
            if(widgetList == False):
                continue
            
            if(index > len(graph.children)-1):
                graph.children += tuple([plot.widgets.HBox([])])
            graph.children[index].children += tuple(widgetList)
            index += 1
        
        if(getGraph):
            return graph
        else:
            display(graph)
            return self
        
###################################################################################

    #This is private function that should not be overriden in the child class
    def getGraphData(self, trace=None, function=None, graph=None):
        
        if(trace == None):
            traces = []
            functions = [] 
        else: 
            traces = [trace]
            functions = [function]
            boundaries = [startBoundary, endBoundary]

        traces.extend(parallelGraphing(self.graphableObjects, self.start, self.end))
        widgets = []
        
        for graphableObject in self.graphableObjects:
            
           # traces.append(graphableObject.graph(showGraph=False, 
   #start=self.start if graphableObject.forcedStart == None else graphableObject.forcedStart,      end=self.end if graphableObject.forcedEnd == None else graphableObject.forcedEnd,          
   #precision=self.precision, startBoundary=graphableObject.startBoundary, endBoundary=graphableObject.endBoundary))
            
            functions.append(graphableObject.value)
            widgets.append(graphableObject.getWidgets(0, 0))

        traces.extend(self.graphableData)
        return (traces, functions, widgets)
        
###################################################################################

    def addGraphableObject(self, graphableObject):
        graphableObjects = [graphableObject]
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