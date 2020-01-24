#Basis Functions Module
#Contains Classes for Different Basis Functions that can be used for Quantum Mechanical Simulations

#Written by Gary Zeri, Computer Science Student at Chapman University and Member of the LaRue CatLab.

class HOW: 
    
    #mpmath due to handle the overly larage and small numbers computed in this calculation
    #Values range from 10^-40 to 10^40
    import mpmath as mpm
    from mpmath import mpf
    from tqdm import tqdm
    from scipy import inf
    from scipy.integrate import quad as integrate
    
    #Declare All Global Variables Here
    
    #Optimal Bond Distance in Angstrom
    re = 0
    #Base Vibrational Frequency of Diatomic Molecule in hertz
    w = 0
    #Mass of Diatomic Molecule in kg
    u = 0
    #Planck's reduced constant in units of kg m^2 / s
    hbar = 0
    #unitConverter that has units of 1/m^2 and used to change units later in the calculation
    unitConverter = 0
    #How many functions are used for the basis
    size = 0
    #list to hold all the basis function
    basis = []
    
    #Constructor Function that sets the required parameters for the basis set
    #re expected in units of Angstrom
    #w expected in units of wavenumbers
    #u expected in units of AMU
    #checkOrtho: bool that represents whether or not the orthonormality of the basis set should be checked
    def __init__(self, re, w, u, size, checkOrtho=False):
        
        #set numerical accuracy
        self.mpm.mp.prec = 200
        self.mpm.mp.dps = 200
        
        self.size = size
        
        from scipy import constants as consts
        
        #convert provided parameters internally required units
        self.re = self.mpf(re)   
        self.w = self.mpf(w) * self.mpf(100) * self.mpf(consts.c)
        self.u = self.mpf(u) * self.mpf(1.6605) * (10 ** self.mpf(-27))
        
        self.hbar = self.mpf(consts.hbar)        
        self.unitConverter = (self.u * self.w) / self.hbar

        self.buildBasis(checkOrtho)
        
###################################################################################

    #Convert the provided r to a centerd position in units of m
    def rToX(self, r):
        return (r-self.re) / (self.mpf(10) ** self.mpf(10))

###################################################################################

    #Function to represent the e^x term for the wavefunction 
    def eTerm(self, r):
        x = self.rToX(r)
        return self.mpm.exp(-self.unitConverter * (x ** self.mpf(2)) / 2 )
    
###################################################################################    

    #Function that provides input to the hermite polynomial function 
    def hermiteInput(self, r):
        x = self.rToX(r)
        return self.mpm.sqrt(self.unitConverter) * x
    
 ###################################################################################   
    
    #creates a new basis function and returns it as a lambda function
    def newHOW(self, n):
        
        normalization = 1 / self.mpm.sqrt( (2**n) * self.mpm.factorial(n) )
        toAU = ( self.unitConverter * (self.mpf(10) ** self.mpf(-20)) / self.mpm.pi ) ** self.mpf(0.25)
        
        return lambda r : normalization * toAU * self.eTerm(r) * self.mpm.hermite(n, self.hermiteInput(r))

###################################################################################

    #Function to determine if the basis set is orthonormal
    def isOrtho(self):
        
        for index1, b1 in enumerate(self.basis):
            for index2, b2 in enumerate(self.basis):
                
                overlap = abs(round(integrate(0, inf), 7))
                
                if(index1 == index2 and (overlap < .98 or overlap > 1.001)):
                   return (false, index1, index2) 
                elif(overlap != 0):
                   return (false, index1, index2)
                
        return (True)

###################################################################################

    #generates the basis of the specified size
    #checkOrtho: bool that states whether the program should check if the basisSet is orthonormal
    def buildBasis(self, checkOrtho=False):
        
        self.basis = []
        
        for n in range(self.size):
            self.basis.append( self.newHOW(n) )
                               
        if(checkOrtho and not self.isOrtho()[0]):
            print("Warning!!! Harmonic Oscilator Basis Set is not Orthonormal!!")
                   
###################################################################################
    
    #Returns an x and y list of data that can be graphed
    def graphData(self, start=0, end=5, resolution=.01):
        
        x = []
        y = [ [] for i in  range(self.size) ]
        
        points = int( (end - start) / resolution ) 
        
        print("Graphing Data")
        for point in self.tqdm(range(points)):
            x.append( (point * .01) + start )
            
            #For graphing purposes convert Hartrees to Wavenumbers
            for index, basis in enumerate(self.basis): 
                   y[index].append( float(basis(x[-1])) * 2.2 * pow(10,4) )
                
        return x, y