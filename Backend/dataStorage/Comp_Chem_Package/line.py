#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Concrete class to implement a line graphable object

from graphable import *

class line(Graphable):
    
    #is a line implemented as y=mx+b
    def __init__(self, m, b):
        self.graphTitle = "Line"
        
        self.m = m 
        self.b = b

###################################################################################

    def value(self, x):
        return self.m*x + self.b
        