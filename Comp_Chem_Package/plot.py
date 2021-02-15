#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#This Python file sets up Plotly graphing specifically for Computational Chemical Calculations

import plotly.graph_objects as go
import plotly.io as pio
import ipywidgets as widgets
from multiprocess import Pool
from multiprocess import cpu_count

pio.renderers.default = "notebook+plotly_mimetype"

#ser up renderers configuration
config = {
  'modeBarButtonsToAdd':['drawline',
                                        'drawopenpath',
                                        'drawclosedpath',
                                        'drawcircle',
                                        'drawrect',
                                        'eraseshape'
]}
pio.renderers["notebook"].config = config
pio.renderers["plotly_mimetype"].config = config
pio.renderers["jupyterlab"].config = config

#set up comp chem visual template
pio.templates.default = "simple_white"

fontFamily = "Verdana"
cutoffLimit = pow(10, -12)

#modify the default template to better fit into the program
pio.templates[pio.templates.default].layout.update(dict(
    
    font_family = fontFamily,
    
    title_x = 0.5, 
    title_font_size = 23,
    
    yaxis_showgrid = True,
    xaxis_showgrid = True,

    yaxis_title_font_size = 17,
    xaxis_title_font_size = 17,   
))

#Global parameter for graphing structure
graphingParameters = { "showGraph"      : False, 
                       "forcedStart"    : None, 
                       "forcedEnd"      : None,
                       "precision"      : None, 
                       "startBoundary"  : None, 
                       "endBoundary"    : None}


#internal resolution dictionary
resolutionValue = { "High"   : 800, 
                    "Medium" : 400, 
                    "Low"    : 200}

###################################################################################

#Global Plot Helper Functions Declared Here
#Returns a line trace from a given function
<<<<<<< HEAD
def graphFunction(function, title="", resolution=100, start=0, end=5, precision=2, 
                 xTitle="x", yTitle="y", hoverTemplate=None, rawData=False, dash="solid", group="", fill = "none", yEqualsCutoff = None):
=======
def graphFunction(function, title, resolution=100, start=0, end=5, precision=2, 
                 xTitle="x", yTitle="y", hoverTemplate=None, rawData=False, startBoundary=None, endBoundary=None, dash="solid", group="", graphCondition=None):
    
    #print("Graph Function Called!")
>>>>>>> parent of 917e0bd (Adds working version for Dr. LaRue Lab)
    
    x = []
    y = []
    dx = 1 / resolution 
   
    if(yEqualsCutoff != None):
        leftSide = True
        for step in range(int(abs( (end-start)/dx ))):

            xValue = start + step * dx
            yValue = function(xValue)
<<<<<<< HEAD
            
            if(abs(yValue - yEqualsCutoff) <= cutoffLimit):
                if(leftSide):
                    continue
                    leftSide = False 
                else:
=======
            print(startBoundary)
            if(xValue >= startBoundary):
                if(yValue <= endBoundary(xValue)):
                    x.append(xValue)
                    y.append(yValue)
                else: 
>>>>>>> parent of 917e0bd (Adds working version for Dr. LaRue Lab)
                    break
            x.append(xValue)
            y.append(yValue)

    else:
        for step in range(int(abs( (end-start)/dx ))):
            x.append(start + step * dx)
            y.append(function(x[-1]))

    if(rawData):
        return (x, y)
    else:
        return buildTrace(x, y, title, precision, xTitle, yTitle, hoverTemplate, dash=dash, group=group, fill = fill)

###################################################################################

#move this into a part of the graphable class,
#maybe can take advatage of dict like props of trace to speed up graphing?
def buildTrace(x, y, title, precision, xTitle, yTitle, mode="lines", legendgroup=None, dash="solid", group="", fill = "none"):
    
    precision = "0." + str(precision)
    return go.Scatter(
        x = x, y = y,
        name = title,
        
        hovertemplate = "<b>" + xTitle + " = %{x:" + precision + "f}</b><br>" + 
                        "<b>" + yTitle + " = %{y:" + precision + "f}</b>",
        hoverlabel_font_size = 16, 
        mode = mode, 
        line_dash = dash, 
        legendgroup = group, 
        fill = fill
    )

###################################################################################

<<<<<<< HEAD
#returns the general ipython widgets that all graphable objects have
#and connects them to all of the figure's traces
#figure refers to the plotly figure widget object to which the widgets should associated with
def getGraphFunctionWidgets(figure, traces, functions, graphableObjects, returnWidgets=False,
=======
#returns the ipython widgets needed f
def getGraphFunctionWidgets(figure, traces, functions, returnWidgets=False,
>>>>>>> parent of 917e0bd (Adds working version for Dr. LaRue Lab)
                            resolution=100, start=0, end=5, precision=2, graphableData=0, endBoundary=None, startBoundary=None):
    
    fontFamily = pio.templates[pio.templates.default]["layout"]["font"]["family"]
    startDescription = '<p style="font-family:' + fontFamily + ';font-size:15px">'
    endDescription = '</p>'

    
    resolutionWidget = widgets.Dropdown(
        options = ['Low', 'Medium', 'High'],
        value = 'Medium',
        description = startDescription + "Resolution" + endDescription,
    )
    
    precisionWidget = widgets.BoundedIntText(
        value = precision, 
        min = 0, 
        max = 20, 
        step = 1, 
        description = startDescription + "Precision" + endDescription
    )
    
    startWidget = widgets.FloatText(
        value = start, 
        step = 0.1,
        description = startDescription + "Start" + endDescription
    )
    
    endWidget = widgets.FloatText(
        value = end, 
        step = 0.1, 
        description = startDescription + "End" + endDescription
    )
    
    if(graphableData > 0):
        functionTraces = traces[:graphableData]     
<<<<<<< HEAD
=======

        observationFunctionWrapper = lambda change : [trace.update(buildTrace( x = trace.x, y = trace.y, 
                                                                               title = trace.name,
                                                                               precision = precisionWidget.value,
                                                                               xTitle = trace.hovertemplate.split("<b>")[0].split("=")[0],
                                                                               yTitle = trace.hovertemplate.split("<b>")[1].split("=")[0 ],
                                                                               mode = "markers", group = trace.legendgroup)) 
                                                      for trace in traces[graphableData:]]
        precisionWidget.observe(observationFunctionWrapper, "value")

>>>>>>> parent of 917e0bd (Adds working version for Dr. LaRue Lab)
    else: 
        functionTraces = traces
        
    resolutionWidget.observe(lambda change : resolutionWidgetUpdate(functionTraces, graphableObjects, change["new"], change["old"], precisionWidget.value, startWidget.value, endWidget.value), "value")
    precisionWidget.observe(lambda change : widgetUpdates(traces, lambda trace : trace.update( 
                                                         hovertemplate = "<b>" + "test"  + " = %{x:0." + 
                                                                         str(precisionWidget.value) + "f}</b><br>" + "<b>" +
                                                                         "cat" + " = %{y:0." + str(precisionWidget.value) + 
                                                                         "f}</b>")), "value")
    
<<<<<<< HEAD
    startWidget.observe(lambda change : endPointWidgetUpdate(functionTraces, resolutionValue[resolutionWidget.value], startWidget.value, endWidget.value, graphableObjects), "value")
    endWidget.observe(lambda change : endPointWidgetUpdate(functionTraces, resolutionValue[resolutionWidget.value], startWidget.value, endWidget.value, graphableObjects), "value")      
        
=======
    observationFunctionWrapper = lambda change : [trace.update(graphFunction(functions[index],
                                                                            title = trace.name,
                                                                            resolution = resolutionWidget.value,
                                                                            precision = precisionWidget.value,
                                                                            start = startWidget.value, end = endWidget.value, startBoundary = startBoundary, endBoundary = endBoundary, group = trace.legendgroup
                                                                           )) 
                                                for index, trace in enumerate(functionTraces)]
    
    resolutionWidget.observe(observationFunctionWrapper, "value")
    precisionWidget.observe(observationFunctionWrapper, "value")
    startWidget.observe(observationFunctionWrapper, "value")
    endWidget.observe(observationFunctionWrapper, "value")      
    
>>>>>>> parent of 917e0bd (Adds working version for Dr. LaRue Lab)
    graphObject = widgets.VBox([
        figure,
        widgets.HBox([resolutionWidget, precisionWidget]),
        widgets.HBox([startWidget, endWidget])
    ])

    for graphableObject in graphableObjects: 
        graphableObject.oldStart = startWidget.value
        graphableObject.oldEnd = endWidget.value
    
    if(returnWidgets):
        return (graphObject, [resolutionWidget, startWidget, endWidget, precisionWidget])
    else:
        return graphObject

###################################################################################

def resolutionWidgetUpdate(traces, graphableObjects, newResolution, oldResolution, precision, start, end):

    for index, trace in enumerate(graphObjects(graphableObjects, precision, resolutionValue[newResolution], start, end)[0]):
        traces[index].update(trace)

###################################################################################

def cutoffCheck(yEqualsCutoff, start, end, minX, maxX):
    return False if yEqualsCutoff == None else (start >= minX and end <= maxX)
        
###################################################################################

def endPointWidgetUpdate(traces, resolution, start, end, graphableObjects):
    
    #exit if invalid start, end values were provided
    if(start >= end):
        return
    
    if(graphableObjects[0].oldStart != start):
        if(start < graphableObjects[0].oldStart):
            for index, graphableObject in enumerate(graphableObjects):
                if(cutoffCheck(graphableObject.yEqualsCutoff, start, end, graphableObject.graphedData.x[0], graphableObject.graphedData.x[-1])):
                    continue
                x, y = graphFunction(graphableObject.value, resolution = resolution, start = start, end = graphableObject.oldStart, rawData = True)
                graphableObject.graphedData.update(x = x + list(graphableObject.graphedData.x), y = y + list(graphableObject.graphedData.y))
                
                graphableObject.oldStart = start    
                endIndex = int((end - graphableObjects[0].graphedData.x[0]) * resolution)
                traces[index].update(x = graphableObject.graphedData.x[:endIndex], y = graphableObject.graphedData.y[:])
        else:
            startIndex = int((start - graphableObjects[0].graphedData.x[0]) * resolution)
            endIndex = int((end - graphableObjects[0].graphedData.x[0]) * resolution)
            for index, graphableObject in enumerate(graphableObjects):
                if(cutoffCheck(graphableObject.yEqualsCutoff, start, end, graphableObject.graphedData.x[0], graphableObject.graphedData.x[-1])):
                    continue
                traces[index].update(x = graphableObject.graphedData.x[startIndex:endIndex],y = graphableObject.graphedData.y[startIndex:endIndex])
            
    else:
        if(end > graphableObjects[0].oldEnd):
            for index, graphableObject in enumerate(graphableObjects):
                if(cutoffCheck(graphableObject.yEqualsCutoff, start, end, graphableObject.graphedData.x[0], graphableObject.graphedData.x[-1])):
                    continue
                x, y = graphFunction(graphableObject.value, resolution = resolution, start = graphableObject.oldEnd, end = end, rawData = True)
                graphableObject.graphedData.update(x = list(graphableObject.graphedData.x) + x, y = list(graphableObject.graphedData.y) + y)

                graphableObject.oldEnd = end    
                startIndex = int((start - graphableObjects[0].graphedData.x[0]) * resolution)
                traces[index].update(x = graphableObject.graphedData.x[startIndex::], y = graphableObject.graphedData.y[startIndex::])
        else:
            startIndex = int((start - graphableObjects[0].graphedData.x[0]) * resolution)
            endIndex = int((end - graphableObjects[0].graphedData.x[0]) * resolution)
            for index, graphableObject in enumerate(graphableObjects):
                if(cutoffCheck(graphableObject.yEqualsCutoff, start, end, graphableObject.graphedData.x[0], graphableObject.graphedData.x[-1])):
                    continue
                traces[index].update(x = graphableObject.graphedData.x[startIndex:endIndex],y = graphableObject.graphedData.y[startIndex:endIndex])          
        
###################################################################################

def widgetUpdates(traces, updateFunction):
    for trace in traces: 
        updateFunction(trace)

###################################################################################

def getWidgetDescription(description):
    return '<p style="font-family:' + pio.templates[pio.templates.default]["layout"]["font"]["family"] + ';font-size:15px">' + description + '</p>' 

###################################################################################

#Allows for parallel processing to help speed up the graphing process
def parallelGraphing(graphableObjects, precision, resolution, start, end):
    p = Pool(cpu_count())

    results = p.map(lambda graphableObject : parallelGraphingWorker(graphableObject, precision, resolution, start, end), graphableObjects)
    p.close()
    p.join()
    
    traces = []
    functions = []
    for index, objectData in enumerate(results): 
        traces.append(objectData[0])
        functions.append(objectData[1])
        graphableObjects[index].graphedData = objectData[0]
        
    return traces, functions

###################################################################################

def parallelGraphingWorker(graphableObject, precision, resolution, start, end):
    
    return (graphFunction(graphableObject.value, title = graphableObject.graphTitle, precision = precision, xTitle = graphableObject.xTitle, yTitle = graphableObject.yTitle, 
                        dash = graphableObject.dash, group = graphableObject.group, start = start, end = end, fill = graphableObject.fill, resolution = resolution), 
            graphableObject.value)

###################################################################################

def graphObjects(graphableObjects, precision, resolution, start, end):
    if(len(graphableObjects) > 9 and cpu_count() > 1):
        traces, functions = parallelGraphing(graphableObjects, precision, resolution, start, end)
    else: 
        traces = []
        functions = []

        for graphableObject in graphableObjects: 
            traces.append(graphFunction(graphableObject.value, title = graphableObject.graphTitle, precision = precision, xTitle = graphableObject.xTitle, 
                                        yTitle = graphableObject.yTitle, dash = graphableObject.dash, group = graphableObject.group, 
                                        start = start, end = end, fill = graphableObject.fill, resolution = resolution, yEqualsCutoff = graphableObject.yEqualsCutoff))
            graphableObject.graphedData = traces[-1]
            functions.append(graphableObject.value)

    return traces, functions