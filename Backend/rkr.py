#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

from pesMethod import * 

class rkr(PESMethod):
    
    #Overide global variables here
    start = -0.499
    name = "RKR"
    resolution = 4
    
    #Local Global Variables
    EPrimeCutoff = 0
    leftAsymptoteCutoff = 0
    
    #Declare all global variables here
    #delta should be a very small number
    #the smaller the value, the more accurate RKR will be but the slower it will also be
    delta = pow(10, -3)
    
    def getWidgets(self):
        return False

###################################################################################

    def implementation(self, v, E):
        
        #term ^ 1
        originalTerm = v + 0.5
        term = originalTerm
        b = self.diatomicConstants["B"] - self.diatomicConstants["a"] * term
        q = self.diatomicConstants["w"] - 2*self.diatomicConstants["wx"]*term
        
        #term ^ 2
        term *= originalTerm
        q += 3*self.diatomicConstants["wy"]*term
        b += self.diatomicConstants["y"]*term
        
        #term ^ 3
        term *= originalTerm
        q += 4*self.diatomicConstants["wz"]*term
        
        correctionFactor = 2*sqrt(self.delta / q)
        
        integrandF = lambda vPrime : 1 / sqrt(E - self.E(vPrime))
        integrandG = lambda vPrime : self.B(vPrime) / sqrt(E - self.E(vPrime))
        
        fValue = integrate(integrandF, -0.5, v-self.delta) + correctionFactor
        
        c0 = 4.1058045 * fValue / sqrt(self.diatomicConstants["u"])
        c1 = sqrt(1 + 
                      ( 1 / 
                           (fValue * 
                                     ( integrate(integrandG, -0.5, v-self.delta) + b*correctionFactor ))))
        
        #returns tuple of (r+, r-)
        return c0 * (c1 + 1), c0 * (c1 - 1)
    
###################################################################################

    def E(self, v, J=0):
        
        #term ^ 1
        originalTerm = v + 0.5
        term = originalTerm
        sumValue = self.diatomicConstants["w"]*term
        
        #term ^ 2
        term *= originalTerm
        sumValue -= self.diatomicConstants["wx"]*term
    
        #term ^ 3
        term *= originalTerm 
        sumValue += self.diatomicConstants["wy"]*term
        
        #term ^ 4
        term *= originalTerm 
        sumValue += self.diatomicConstants["wz"]*term
        
        if(J==0):
            return sumValue
        else: 
            return (2*J + 1) * (sumValue - 2*self.diatomicConstants["D"]*J*(J+1))
        
###################################################################################

    def EPrime(self, v):
        
        #term ^ 1
        term = v + 0.5 
        value = self.diatomicConstants["w"] - 2*self.diatomicConstants["wx"]*term 
        
        #term ^ 2
        term *= term 
        value += 3*self.diatomicConstants["wy"]*term 
        
        #term ^ 3
        term *= term 
        return value + 4*self.diatomicConstants["wz"]*term
        
###################################################################################

    def B(self, v):
        term = v + 0.5
        return self.diatomicConstants["B"] + term * (self.diatomicConstants["y"] * term - self.diatomicConstants["a"])
    
###################################################################################

    #Ovride the compute method due to the special needs of the RKR Method
    def compute(self, start=None, resolution=None, delta=None):

            #Set up variables needed for the computation
            if(start == None):
                start = self.start
            if(resolution == None):
                resolution = self.resolution
            if(delta == None):
                delta = self.delta
                
            #set up loading bar for computation
            EPrime = self.EPrime(start)
            loadingBar = widgets.FloatProgress(
                min = -EPrime,
                max = 0, 
                value = -EPrime
            )
            display(widgets.HBox([widgets.Label(value="Computing RKR Surface"), loadingBar]))
            
            dv = 1 / resolution
            v = start 
            leftAsympCutOff = False
            cutOffIndex = 0
            
            data = dict(r=[], E=[])
            derivatives = dict(ddr=[], ddE=[], ddE2=[])

            iterations = 0
            
            while(EPrime > self.EPrimeCutoff and iterations < 500):                
                energy = self.E(v)
                
                if(leftAsympCutOff):
                    data["E"].append(energy)
                    data["r"].append(self.implementation(v, energy)[0])
                else:
                    data["E"].extend([energy, energy])
                    data["r"].extend(self.implementation(v, energy))
                
                if(not leftAsympCutOff and len(data["r"]) > 2):
                    #Compute First Derivative
                    derivatives["ddr"].append( (data["r"][-3] + data["r"][-1]) / 2 )
                    derivatives["ddE"].append( energy-data["E"][-3] / ( data["r"][-3] - data["r"][-1] ))

                    if(len(derivatives["ddr"]) > 1):
                        #Compute 2nd Derivativ
                        derivatives["ddE2"].append( (derivatives["ddE"][-1] - derivatives["ddE"][-2]) / (derivatives["ddr"][-1] - derivatives["ddr"][-2]) )

                        #Determine if Cutoff should be used
                        if(derivatives["ddE2"][-1] <= self.leftAsymptoteCutoff):
                            leftAsympCutOff = True
                            cutOffIndex = len(data["E"])

                v += dv
                iterations += 1
                EPrime = self.EPrime(v)
                loadingBar.value = -EPrime
    
            #manually add in the minimum energy point
            data["r"].append(self.diatomicConstants["re"])
            data["E"].append(0)
            
            #compute the well depth
            data["D"] = max(data["E"][cutOffIndex:]) 
            
            data["method"] = self.name
            
            self.data = data
            return self.data