#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Concrete class to implement the Harmonic Osciallator potential energy surface

from diatomicPotential import DiatomicPotential

class howPES(DiatomicPotential):
    
    name = "HOW Potential Energy"
    isFit = True
    
    def implementation(self, r):
        return 0.5 * self.diatomicConstants["u"] * self.diatomicConstants["w"] * self.diatomicConstants["wx"] * (r - self.diatomicConstants["re"]) ** 2

###################################################################################

    def internalFit(self, data):
        pass
