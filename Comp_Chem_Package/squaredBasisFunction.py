#Written by Gary Zeri
#Member of the LaRue CatLab at Chapman University

from compChemGlobal import Graphable

#Supporting class for the basis function class that allows for creation of a lightweight squared wavefunction
#for graphing pourposes
class squaredBasisFunction(Graphable):
    
    #Declare Global Variables Here
    squaredValue = None
    
    def __init__(self, basisFunction):
        self.__dict__ = basisFunction.__dict__.copy()
        self.graphTitle += " Squared"
        self.squaredValue = basisFunction.squaredValue
        
###################################################################################

    def value(self, r):
        return self.squaredValue(r)