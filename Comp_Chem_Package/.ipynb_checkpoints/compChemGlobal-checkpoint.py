#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#This Python file contains constants, functions and import statements that will be used throughout all 
#the notebooks pertaining to computational chemistry

#Section that can be modified by the user interactively

#@Functions Import Section
#@pow
#uses default python pow

#@integrate
from scipy.integrate import quad as internalIntegrate
def integrate(f, lowerBound, upperBound):
    return internalIntegrate(f, lowerBound, upperBound, limit=1000)[0]

#@ddx
from scipy.misc import derivative as internalDdx
def ddx(f, x, n=1, dx=pow(10, -2)):
    return internalDdx(f, x, n=n, dx=dx)

#@exp
from numpy import exp

#@sqrt
from numpy import sqrt

#@superSqrt sqrt meant to handle very very large numbers
def superSqrt(x):
    return pow(x, 0.5)

#@log general log function as base e
from numpy import log 

#@factorial
from math import factorial

#hermitePolynomials
from scipy.special import eval_hermite as hermitePolynomials

#@floor
from math import floor

#@ceil
from math import ceil

#@eigh returns tuple/list with following data [ev, evc], with the ev and the evc being ordered
from scipy.linalg import eigh as internalEigh 
def eigh(matrix):
    ev, evc = internalEigh(matrix)
    evc = evc.transpose()
    
    return ev, evc

#@Constant Variables Section
#@pi
from scipy.constants import pi

#@e
from scipy.constants import e

#@c units of m/s
from scipy.constants import c

#@hbar plancks reduced constant in units of kg m^2 / s
from scipy.constants import hbar

#@h plancks constant in units of kg m^2 / s
from scipy.constants import h

#@mToA converts meters to Angstroms
mToA = pow(10, 10)

#@aToM2 converts Angstroms to meters squared
aToM2 = pow(10, -20)

#@jToWavenumbers
jToWavenumbers = 5.034116 * pow(10, 22)

#@amuToKg
amuToKg = 1.6605 * pow(10, -27)

#@inf
from numpy import inf

#Default Imports and Constants that the user will not be modifying

#import plotly graphing file
import plot

#import ipython widgets
from plot import widgets

#allow things to be graphable
from graphable import *