#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#File that contains structures and functions related to diatomic constants

#allows access to the getDiatomicConstants function that 
#scrapes the NIST webook for diatomic constants
from nistScraper import * 

#function that builds a diatomic constants dict from 
#argument passed variables. Default is to initalize all values to 
#empty strings and 0s
def buildDiatomicConstants(name="", state="", T=0,
                           w=0, wx=0, wy=0, wz=0, B=0, a=0, 
                           y=0, D=0, re=0, u=0):
    
        return dict(name = name, state = state,           
                    T = T, w = w, wx = wx, wy = wy, 
                    wz = wz, B = B, a = a, y = y, 
                    D = D, re = re, u = u)