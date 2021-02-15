#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University

#Graphable Data Abstract class to provide a common interface for all graphable data objects in the Comp Chem Library

from abc import ABC, abstractmethod
from compChemGlobal import plot

class GraphableData(ABC):
    
    #Declare all global variables here
    graphTitle = ""
    xTitle = ""
    yTitle = ""
    precision = 2
    
    #Can be "markers", "lines" or "lines+markers"
    mode = "markers"
    
    @abstractmethod
    def __init__(self):
        
        #Use this to override global variables in the Graphable Class
        self.graphTitle = "Data Title"
        self.xTitle = "Data X Title"
        self.yTitle = "Data Y Title"
        self.precision = 2
        self.mode = "markers"

###################################################################################

    @abstractmethod
    def getGraphData(self):
        return [["x Data List"], ["y Data List"]]
    
###################################################################################

    def graph(self, showGraph=True, precision=precision, returnGraph=False):
        
        data = self.getGraphData()
       
        
        if(showGraph):
            fig = plot.go.FigureWidget(layout = dict( xaxis_title = self.xTitle, 
                                                      yaxis_title = self.yTitle, 
                                                      title_text = self.graphTitle
                                                    ), 
                                       data = [plot.buildTrace( x=data[0], y=data[1], 
                                                                title = self.graphTitle, 
                                                                xTitle = self.xTitle, 
                                                                yTitle = self.yTitle,
                                                                precision = precision,
                                                                mode = self.mode
                                                               )]
                                      )
            
            precisionWidget = plot.widgets.BoundedIntText( value = precision, 
                                                           min = 0, 
                                                           max = 20, 
                                                           step = 1, 
                                                           description = '<p style="font-family:' + plot.fontFamily + ';font-size:15px">Precision</p>'
                                                         )
            
            trace = fig.data[0]
            precisionWidget.observe(lambda change : trace.update(plot.buildTrace( x=data[0], y=data[1], 
                                                                                  title = self.graphTitle, 
                                                                                  xTitle = self.xTitle, 
                                                                                  yTitle = self.yTitle,
                                                                                  precision = precisionWidget.value,
                                                                                  mode = self.mode
                                                                                )))
            display(plot.widgets.VBox([fig, precisionWidget]))
            
        else: 
            return trace