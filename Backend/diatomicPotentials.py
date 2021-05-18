#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#This Python File contains class definition for various Diatomic Surface Potentials, such as the Extended Rydberg Equation

import numpy as np

class extendedRydberg:
    
    from numpy import exp
    import mpmath
    from scipy import optimize as optimize
    
    #Delcare All Global Variables Here
    
    #D: represents the well depth
    #Re: Equblibrium well depth
    #a1, a2, a3: constants that determine the curvature and shape of the potential
    #c: represent constant to be added to shift the potential up or down
    #curveFitted, bool that represents whether or not the curve has been fitted and used to 
    #avoid user caused errors
    D = 0
    Re = 0 
    a1 = 0 
    a2 = 0 
    a3 = 0
    c = 0
    curveFitted = False
    zeroRe = True
       
    #Extended Rydberg Equation Constructor Function
    #Fitting Data: Is a list containing two other lists that respectivly contain the diatomic bond distances and energy at each bond distance level
    def __init__(self, fittingData=[], flex=.00001):
        
        if(len(fittingData) == 2):
            self.fitPotential(fittingData[0], fittingData[1], flex)
            
###################################################################################

    #Extended Ryd-Berg Equation Originates From 
    #"Application of extended-Rydberg parameters in general Morse potential functions'
    #By Teik-Cheng Lim
    #r: Independent Variable, represents the bond distance in the diatomic molecule
    #D: represents the well depth
    #Re: Equblibrium well depth
    #a1, a2, a3: constants that determine the curvature and shape of the potential
    def internalEquation(self, r, D, Re, a1, a2, a3, c):
        
        p = r-Re

        eTerm = self.exp(-a1 * p)
        
        if(not self.zeroRe):
            c = 0 
            
        return (-D * ( 1 + (a1*p) + (a2*pow(p, 2)) + (a3*pow(p, 3)) ) * eTerm) + c
    
###################################################################################

    #Eqaution is the eqaution that is to be called by the outside user to call the function 
    #as this will auto-fill the constants for the Extended rydberg
    def equation(self, r):
        self.checkFitting()
        return self.internalEquation(r, self.D, self.Re, self.a1, self.a2, self.a3, self.c)
        
###################################################################################    
    
    #function that returns two lists of x and y data for graphing purposes
    def graphData(self, rMin, rMax, dx=0.001):
        
        self.checkFitting()
        
        #Praprare Variables Used for Graphing
        r = rMin
        R = []
        E = []
        
        while(r < rMax):
            
            R.append(r)
            E.append(
                self.equation(r)
            )
        
            r += dx
            
        return R, E
                
###################################################################################
    
    #fitPotential functions fits the potential to the proivided (x,y) coordinate data
    def fitPotential(self, R, E, flex=.0000001):
                
        minE = min(E)
        maxE = max(E)
        Re = (R[0] + R[1]) / 2
        DE = maxE
        
        optimizationFunction = lambda r, a1, a2, a3 : self.internalEquation(r, DE, Re, a1, a2, a3, DE)

        #def internalEquation(self, r, D, Re, a1, a2, a3, c):
        #optimizeEquation = lambda r, a1, a2, a3 : self.internalEquation(r, DE, Re, a1, a2, a3, DE)
        optimizedParameters = self.optimize.curve_fit(self.internalEquation, R, E, maxfev = pow(10, 9)*2)[0]   
            #Parameter Guess Values
            #D guessed as the min - the max
            #Re is the Re at the minimum point of the well
            #a1 2, and 3 choosen as random numbers
            #c choosen as well min difference from zero
           # p0 = [DE, Re,  1, 1, 1, DE],
           # bounds = [(DE-flex, Re-flex, -np.inf, -np.inf, -np.inf, DE-flex), 
           #              (DE+flex, Re+flex, np.inf, np.inf, np.inf, DE+flex)],
           # maxfev = pow(10, 9)*2)[0] 
        
        self.D = optimizedParameters[0]
        self.Re = optimizedParameters[1]
        self.a1 = optimizedParameters[2]
        self.a2 = optimizedParameters[3]
        self.a3 = optimizedParameters[4]
        self.c = optimizedParameters[5]
        
        #print(self.D)
        #print(self.Re)
        print(self.a1)
        print(self.a2)
        print(self.a3)
        #print(self.c)
        
        self.curveFitted = True
        
###################################################################################
        
    def buildPotential(self, DC):
        self.D = DC.D
        self.Re = DC.re
        self.a1 = optimizedParameters[2]
        self.a2 = optimizedParameters[3]
        self.a3 = optimizedParameters[4]
    
###################################################################################

    def checkFitting(self):
         if(not self.curveFitted):
            print("Warning! Please fit potential energy surface data to this Extended-Rydberg Potential using ExtendedRydbergInstanceName.fitPotential(xDataList, yDataList)")
            
#-----------------------------------------------------------------------------------

class morsePotential():
       
    import numpy as np
    from scipy import optimize as optimize

    #Define All Global Variables Here
    
    #D: Dissociation Energy 
    #Re: optimal bond distance
    #a: controls curvature of the potential
    #CurveFitted: bool that represents whether or not the curve has been fitted to some potential
    D = 0 
    Re = 0 
    a = 0
    c = 0
    R = [0]
    curveFitted = False
    
    #Morse Potential Equation Constructor Function
    #Fitting Data: Is a list containing two other lists that respectivly contain the diatomic bond distances and energy at each bond distance level
    def __init__(self, fittingData=[], useInterpolation=False):
        
        if(len(fittingData) == 2):
            self.fitPotential(fittingData[0], fittingData[1], useInterpolation)
            
###################################################################################    
    
    def internalEquation(self, r, D, Re, a, c):
        p = r-Re
        return (D * self.np.exp(-2 * a * p)) - (2 * D * self.np.exp(-a * p)) + c
    
###################################################################################

    #Eqaution is the eqaution that is to be called by the outside user to call the function 
    #as this will auto-fill the constants for the Extended rydberg
    def equation(self, r):
        
        self.checkFitting()
        
        if(self.useInterpolation):
            deltaFunction = lambda discreteR : abs(discreteR - r)
            a = self.a[self.R.index(min(self.R, key=deltaFunction))]
            
            if(a == self.a[len(self.a)-1]):
                r = max(self.R)
        else:
            a = self.a[0]
        
        return self.internalEquation(r, self.D, self.Re, a, self.c)

###################################################################################    
    
    #function that returns two lists of x and y data for graphing purposes
    def graphData(self, rMin, rMax, dx=0.001):
        
        self.checkFitting()
        
        #Praprare Variables Used for Graphing
        r = rMin
        R = []
        E = []
        
        while(r < rMax):
            
            R.append(r)
            E.append(self.equation(r))
        
            r += dx
            
        return R, E
                
###################################################################################
    
    #fitPotential functions fits the potential to the proivided (x,y) coordinate data
    def fitPotential(self, R, E, useInterpolation=False):
    
        self.Re = (R[0] + R[1]) / 2
        self.D = max(E)
        a = []
    
        if(useInterpolation):
            for index, r in enumerate(R):
                a.append(self.buildA(r, E[index]))
        else:
            optimizationFunction = lambda r, a : self.internalEquation(r, self.D, self.Re, a, self.D)
            a.extend(self.optimize.curve_fit(optimizationFunction, R, E, maxfev=pow(10, 5))[0])
    
        self.a = a
        self.c = self.D
        self.R = R
        
        self.useInterpolation = useInterpolation
        self.curveFitted = True

###################################################################################

    def checkFitting(self):
         if(not self.curveFitted):
            print("Warning! Please fit potential energy surface data to this Extended-Rydberg Potential using ExtendedRydbergInstanceName.fitPotential(xDataList, yDataList)")    
            
###################################################################################

    def buildA(self, r, E):
        
        squareRoot = self.np.sqrt(E / self.D)
        
        if(r > self.Re and squareRoot != 1):
            squareRoot *= -1
        
        return -self.np.log(1 + squareRoot) / (r - self.Re)