#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#This Python file contains constants, functions and import statements that will be used throughout all 
#the notebooks pertaining to computational chemistry

#Section that can be modified by the user interactively

#@Functions Import Section
#@pow
#using default python pow

#@integrate
from scipy.integrate import quad as internalIntegrate
def integrate(f, lowerBound, upperBound):
    return internalIntegrate(f, lowerBound, upperBound, limit=pow(10, 5))[0]

#@ddx
from scipy.misc import derivative as internalDdx
def ddx(f, x, n=1, dx=pow(10, -5)):
    return internalDdx(f, x, n=n, dx=dx)

#@exp
from numpy import exp

#@sqrt
from numpy import sqrt

#@superSqrt sqrt meant to handle very very large numbers
def superSqrt(x):
    return pow(x, 0.5)

#@log general log function
from numpy import log 

#@factorial
from math import factorial

#hermitePolynomials
from scipy.special import eval_hermite as hermitePolynomials

#@Constant Variables Section
#@pi
from scipy.constants import pi

#@c units of m/s
from scipy.constants import c

#@hbar plancks reduced constant in units of kg m^2 / s
from scipy.constants import hbar

#@h plancks constant in units of kg m^2 / s
from scipy.constants import h

#@mToA converts meters to Angstroms
mToA = pow(10, 10)

#Default Imports and Constants that the user will not be modifying

#used for loading bars in python
from tqdm import tqdm

#import plotly graphing file
import plot

#import ipython widgets
from plot import widgets

#import graphable 
from graphable import *