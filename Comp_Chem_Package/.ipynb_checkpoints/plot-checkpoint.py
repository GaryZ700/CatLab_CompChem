#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#This Python file sets up Plotly graphing specifically for Computational Chemical Calculations

import plotly.graph_objects as go
import plotly.io as pio
import ipywidgets as widgets

pio.renderers.default = "notebook+plotly_mimetype"

#set up comp chem visual template
pio.templates.default = "simple_white"

#modify the default template to better fit into the program
pio.templates[pio.templates.default].layout.update(dict(
    
    font_family = "Verdana",
    
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
                 xTitle="x", yTitle="y"):
    
    x = []
    y = []
    
    dx = 1 / resolution
    
    for step in range(int(abs( (end-start)/dx ))):
        x.append(start + (step * dx))
        y.append(function(x[-1]))
    
    precision = "0." + str(precision)
    return go.Scatter(
        x = x, y = y,
        name = title,
        
        hovertemplate = "<b>" + xTitle + " = %{x:" + precision + "f}</b><br>" + 
                        "<b>" + yTitle + "= %{y:" + precision + "f}</b>",
        hoverlabel_font_size = 16
    )
    
###################################################################################

#returns the ipython widgets needed f
def getGraphFunctionWidgets(figure, traces, functions):
    
    fontFamily = pio.templates[pio.templates.default]["layout"]["font"]["family"]
    startDescription = '<p style="font-family:' + fontFamily + ';font-size:15px">'
    endDescription = '</p>'
    
    resolution = widgets.BoundedFloatText(
        value = 100,
        min = 0.001, 
        max = pow(10, 300),
        step = 0.1,
        description = startDescription + "Resolution" + endDescription
    )
    
    precision = widgets.BoundedIntText(
        value = 2, 
        min = 0, 
        max = 20, 
        step = 1, 
        description = startDescription + "Precision" + endDescription
    )
    
    start = widgets.FloatText(
        value = 0, 
        step = 0.1,
        description = startDescription + "Start" + endDescription
    )
    
    end = widgets.FloatText(
        value = 5, 
        step = 0.1, 
        description = startDescription + "End" + endDescription
    )
    
    observationFunctionWrapper = lambda change: [trace.update(graphFunction(functions[index],
                                                                            title = trace.name,
                                                                            resolution = resolution.value,
                                                                            precision = precision.value,
                                                                            start = start.value, end = end.value
                                                                           )) 
                                                for index, trace in enumerate(traces)]
    
    resolution.observe(observationFunctionWrapper, "value")
    precision.observe(observationFunctionWrapper, "value")
    start.observe(observationFunctionWrapper, "value")
    end.observe(observationFunctionWrapper, "value")
    
    return widgets.VBox([
        figure,
        widgets.HBox([resolution, precision]),
        widgets.HBox([start, end])
    ])