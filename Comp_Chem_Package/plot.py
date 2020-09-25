#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#This Python file sets up Plotly graphing specifically for Computational Chemical Calculations

import plotly.graph_objects as go
import plotly.io as pio
import ipywidgets as widgets

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

###################################################################################

#Global Plot Helper Functions Declared Here
#Returns a line trace from a given function
def graphFunction(function, title, resolution=100, start=0, end=5, precision=2, 
                 xTitle="x", yTitle="y", hoverTemplate=None, rawData=False, startBoundary=None, endBoundary=None, dash="solid", group="", graphCondition=None):
    
    #print("Graph Function Called!")
    
    x = []
    y = []
    
    dx = 1 / resolution 
    if(startBoundary != None and graphCondition == None and type(startBoundary) != list):
        for step in range(int(abs(end-start)/dx)):
            xValue = start + step * dx
            yValue = function(xValue)
            print(startBoundary)
            if(xValue >= startBoundary):
                if(yValue <= endBoundary(xValue)):
                    x.append(xValue)
                    y.append(yValue)
                else: 
                    break
                    
    elif (graphCondition != None):
        for step in range(int(abs(end-start)/dx)):
            xValue = start + step * dx
            yValue = function(xValue)
            if(graphCondition(xValue, yValue)):
                x.append(xValue)
                y.append(yValue)
        
    else: 
          for step in range(int(abs( (end-start)/dx ))):
            x.append(start + step * dx)
            y.append(function(x[-1]))

    if(rawData):
        return (x, y)
    else:
        return buildTrace(x, y, title, precision, xTitle, yTitle, hoverTemplate, dash=dash, group=group)

###################################################################################

def buildTrace(x, y, title, precision, xTitle, yTitle, mode="lines", legendgroup=None, dash="solid", group=""):
    
    precision = "0." + str(precision)
    return go.Scatter(
        x = x, y = y,
        name = title,
        
        hovertemplate = "<b>" + xTitle + " = %{x:" + precision + "f}</b><br>" + 
                        "<b>" + yTitle + " = %{y:" + precision + "f}</b>",
        hoverlabel_font_size = 16, 
        mode = mode, 
        line_dash = dash, 
        legendgroup = group
    )

###################################################################################

#returns the ipython widgets needed f
def getGraphFunctionWidgets(figure, traces, functions, returnWidgets=False,
                            resolution=100, start=0, end=5, precision=2, graphableData=0, endBoundary=None, startBoundary=None):
    
    fontFamily = pio.templates[pio.templates.default]["layout"]["font"]["family"]
    startDescription = '<p style="font-family:' + fontFamily + ';font-size:15px">'
    endDescription = '</p>'

    
    resolutionWidget = widgets.BoundedFloatText(
        value = resolution,
        min = 0.001, 
        max = pow(10, 300),
        step = 0.1,
        description = startDescription + "Resolution" + endDescription
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

        observationFunctionWrapper = lambda change : [trace.update(buildTrace( x = trace.x, y = trace.y, 
                                                                               title = trace.name,
                                                                               precision = precisionWidget.value,
                                                                               xTitle = trace.hovertemplate.split("<b>")[0].split("=")[0],
                                                                               yTitle = trace.hovertemplate.split("<b>")[1].split("=")[0 ],
                                                                               mode = "markers", group = trace.legendgroup)) 
                                                      for trace in traces[graphableData:]]
        precisionWidget.observe(observationFunctionWrapper, "value")

    else: 
        functionTraces = traces
    
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
    
    graphObject = widgets.VBox([
        figure,
        widgets.HBox([resolutionWidget, precisionWidget]),
        widgets.HBox([startWidget, endWidget])
    ])
    
    if(returnWidgets):
        return (graphObject, [resolutionWidget, startWidget, endWidget, precisionWidget])
    else:
        return graphObject

###################################################################################

def getWidgetDescription(description):
    return '<p style="font-family:' + pio.templates[pio.templates.default]["layout"]["font"]["family"] + ';font-size:15px">' + description + '</p>' 