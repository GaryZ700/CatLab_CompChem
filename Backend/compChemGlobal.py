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
    return internalIntegrate(f, lowerBound, upperBound, limit=2000)[0]

#@ddx
from scipy.misc import derivative as internalDdx
def ddx(f, x, n=1, dx=pow(10, -4)):
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

#@aToM2 converts Angstroms squared to meters squared
a2ToM2 = pow(10, -20)

#@jToWavenumbers
jToWavenumbers = 5.034116 * pow(10, 22)
#hcw * 100

#wavenumbersToHz
wavenumbersToHz = 2.99793 * pow(10,10)

#@amuToKg
amuToKg = 1.6605 * pow(10, -27)

#@inf
from numpy import inf

#Default Imports and Constants that the user will not be modifying

#import ipython widgets
from plot import widgets

#allow things to be graphable
from graphable import *

#import plotly graphing file
import plot

#Create global unit conversion objects
from collections import namedtuple
unitBase = namedtuple("unitConversion", ["hartree"])
units = unitBase(hartree="hartree")

#general useful packages 
import numpy as np
from database import dataBase as internalDB
globalDB = internalDB()

#Global Settings Variable Definitions
minNumCPUs = 2

#Uses Jit and is faster in online Jupyter Lab
"""#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#This Python file contains constants, functions and import statements that will be used throughout all 
#the notebooks pertaining to computational chemistry

#Section that can be modified by the user interactively


#general useful packages/functions
import numpy as np
from numba import jit

#@Functions Import Section
#@pow

#@integrate
from scipy.integrate import quad as internalIntegrate
def integrate(f, lowerBound, upperBound):
    return internalIntegrate(f, lowerBound, upperBound, limit=2000)[0]

#@ddx
from scipy.misc import derivative as internalDdx
def ddx(f, x, n=1, dx=pow(10, -4)):
    return internalDdx(f, x, n=n, dx=dx)

#@exp
from numpy import exp as internalExp 
@jit(nopython = True)
def exp(x):
    return internalExp(x)

#@sqrt
from numpy import sqrt as internalSqrt
@jit(nopython = True)
def sqrt(x):
    return pow(x, 0.5)

#@superSqrt sqrt meant to handle very very large numbers
def superSqrt(x):
    if(x < 1000000000000):
        return sqrt(x)
    else:
        return pow(x, 0.5)
    
#@log general log function as base e
from numpy import log as internalLog
@jit(nopython = True)
def log(x):
    return internalLog(x)

#@factorial
from math import gamma as internalGamma
@jit(nopython = True)
def factorial(x):
    return internalGamma(x+1)

#hermitePolynomials
from scipy.special import eval_hermite as hermitePolynomials

#@floor
from math import floor as internalFloor
@jit(nopython = True)
def floor(x):
    return internalFloor(x)

#@ceil
from math import ceil as internalCeil
@jit(nopython = True)
def ceil(x):
    return internalCeil(x)

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

#@aToM2 converts Angstroms squared to meters squared
a2ToM2 = pow(10, -20)

#@jToWavenumbers
jToWavenumbers = 5.034116 * pow(10, 22)
#hcw * 100

#wavenumbersToHz
wavenumbersToHz = 2.99793 * pow(10,10)

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

#Create global unit conversion objects
from collections import namedtuple
unitBase = namedtuple("unitConversion", ["hartree"])
units = unitBase(hartree="hartree")

#Global Settings Variable Definitions
minNumCPUs = inf"""