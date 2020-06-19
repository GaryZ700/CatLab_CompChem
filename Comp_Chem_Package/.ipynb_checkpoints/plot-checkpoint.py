#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#This Python file sets up Plotly graphing specifically for Computational Chemical Calculations

import plotly.graph_objects as go
import plotly.io as pio

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