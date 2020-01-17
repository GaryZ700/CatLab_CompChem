#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#This Python File contains class definition for various Diatomic Surface Potentials, such as the Extended Rydberg Equation

class extendedRydberg:
    
    import numpy as np
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
        return (-D * ( 1 + (a1*p) + (a2*pow(p, 2)) + (a3*pow(p, 3)) ) * self.np.exp(-a1 * p)) + c
    
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
            E.append(self.equation(r))
        
            r += dx
            
        return R, E
                
###################################################################################
    
    #fitPotential functions fits the potential to the proivided (x,y) coordinate data
    def fitPotential(self, R, E):
        
        minE = min(E)
        maxE = E[-1]
        Re = R[E.index(minE)]
    
        optimizedParameters = self.optimize.curve_fit(self.internalEquation, R, E, 
            
            #Parameter Guess Values
            #D guessed as the min - the max
            #Re is the Re at the minimum point of the well
            #a1 2, and 3 choosen as random numbers
            #c choosen as well min difference from zero
            [maxE-minE, Re, .5, .5, .5, maxE-minE], 
            maxfev=pow(10, 8))[0]
    
        self.D = optimizedParameters[0]
        self.Re = optimizedParameters[1]
        self.a1 = optimizedParameters[2]
        self.a2 = optimizedParameters[3]
        self.a3 = optimizedParameters[4]
        self.c = optimizedParameters[5]
        
        print(self.D)
        print(self.Re)
        print(self.a1)
        print(self.a2)
        print(self.a3)
        print(self.c)
        
        self.curveFitted = True
        
###################################################################################

    def checkFitting(self):
         if(not self.curveFitted):
            print("Warning! Please fit potential energy surface data to this Extended-Rydberg Potential using ExtendedRydbergInstanceName.fitPotential(xDataList, yDataList)")
            
#-----------------------------------------------------------------------------------

class morsePotential():
    
    import numpy as np
    
    #Define All Global Variables Here
    
    #D: Dissociation Energy 
    #Re: optimal bond distance
    #a: controls curvature of the potential
    #CurveFitted: bool that represents whether or not the curve has been fitted to some potential
    D = 0 
    Re = 0 
    a = 0
    c = 0
    curveFitted = False
    
###################################################################################    
    
    def internalEquation(self, r, D, Re, a, c):
        
        p = r-Re
        return (D * self.np.exp(-2 * a * p)) - (2 * D * self.np.exp(-a * p)) 
    
###################################################################################

    #Eqaution is the eqaution that is to be called by the outside user to call the function 
    #as this will auto-fill the constants for the Extended rydberg
    def equation(self, r):
        self.checkFitting()
        return self.internalEquation(r, self.D, self.Re, self.a, self.c)

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
    def fitPotential(self, R, E):
    
        optimizedParameters = self.optimize.curve_fit(self.internalEquation, R, E, maxfev=pow(10, 4))[0]
    
        self.D = optimizedParameters[0]
        self.Re = optimizedParameters[1]
        self.a = optimizedParameters[2]
        self.c = optimizedParameters[3]
        
        self.curveFitted = True
        
###################################################################################

    def checkFitting(self):
         if(not self.curveFitted):
            print("Warning! Please fit potential energy surface data to this Extended-Rydberg Potential using ExtendedRydbergInstanceName.fitPotential(xDataList, yDataList)")
    