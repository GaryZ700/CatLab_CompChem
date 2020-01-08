#Written by Gary Zeri, Computer Science Major at Chapman University and Member of the LaRue CatLab

#RKR Class to Allow for Simple RKR Calcuations as needed
class RKR:
    
    #All Imports Done Here
    import numpy as np
    from tqdm import tqdm 
    
    #Declare All Global Variables Here
    
    #Is the distance from v that the integration stops at
    delta = pow(10, -5)

    #Reduced Molecular Mass
    #In Non Hartree Atomic Units, each proton has an amu of 1
    u = 0

    #Diatomic Constants, must be in Wavenumbers (1 / cm)
    we = 0
    wxe = 0
    wye = 0
    wze = 0
    Be = 0
    alphae = 0
    ye = 0
    
    turningPoints = []
    energy = []
    
    dataGraphed = False

###################################################################################

    def setDiatomicConstants(self, alphae, Be, we, wxe, wye, wze, ye):
        
        self.alphae = alphae
        self.Be = Be
        self.we = we
        self.wxe = wxe
        self.wye = wye
        self.wze = wze
        self.ye = ye
        
        self.dataGraphed = False
        self.turningPoints = []
        self.energy = []
        
###################################################################################

    def setReducedMass(self, u):
        self.u = u
        
        self.dataGraphed = False
        self.turningPoints = []
        self.energy = []
        
###################################################################################

    def setDelta(self, delta):
        self.delta = delta
        
###################################################################################       

    def E(self, v):
        term = v + 0.5 
        return (self.we * term) - (self.wxe*pow(term, 2)) + (self.wye*pow(term, 3)) + (self.wze*pow(term,4))

###################################################################################
    
    def integralRadical(self, v, vPrime):
        return self.np.sqrt( self.E(v) - self.E(vPrime) )

###################################################################################       
    
    def B(self, v):
        term = v + 0.5
        return self.Be - (self.alphae * term)  + self.ye*pow(term, 2)

###################################################################################       

    def Q(self, v):
        term = v + 0.5
        return self.we - (2*self.wxe*term) + (3*self.wye*pow(term, 2)) + (4*self.wze*pow(term,3))
    
###################################################################################           

    def correctionFactor(self, v):
        return 2 * self.np.sqrt(self.delta / self.Q(v))

###################################################################################           

    def f(self, v):
        
        from scipy.integrate import quad as integrate
        
        integrand = lambda vPrime: 1 / self.integralRadical(v, vPrime)
        return integrate(integrand, -0.5, v-self.delta)[0] + self.correctionFactor(v)
    
###################################################################################

    def g(self, v):
        
        from scipy.integrate import quad as integrate
        
        integrand = lambda vPrime : self.B(vPrime) / self.integralRadical(v, vPrime)
        return integrate(integrand, -0.5, v-self.delta)[0] + (self.B(v)*self.correctionFactor(v))
    
################################################################################### 

    #v refers to the specided energy level for which the turning points should be computed for
    def compute(self, v):
        
        #Check that reduced mass is not zero and that an exception will not be thrown when 
        #division by zero occurs
        if(self.u == 0):
            print("Warning!! The reduced mass $\mu$ must be greater than 0!")
            print("Please use the setReducedMass(muValue) method on the RKR class instance to fix this issue.")
            print("RKR method is now aborting.")
            return
        
        c0 = 4.1058045 * self.f(v) / self.np.sqrt(self.u)
        radicand = 1 / ( self.f(v) * self.g(v) )
        c1 = self.np.sqrt(1 + radicand)

        self.energy.extend( [self.E(v)] * 2 )
        self.turningPoints.append( c0 * (c1 + 1) )  
        self.turningPoints.append( c0 * (c1 - 1) )
        
        return ( (self.turningPoints[-1], self.turningPoints[-2], self.energy[-1]) )
    
###################################################################################

    def graphData(self, resolution=0.01, startPoint=-0.499, endPoint=12):

        if(not self.dataGraphed):
            
            self.dataGraphed = True
            self.turningPoints = []
            self.energy = []
            
            print("\nGenerating RKR Graph")
            for v in self.tqdm(self.np.arange(startPoint, endPoint, resolution)):
                self.compute(v)
                
        return self.turningPoints, self.energy