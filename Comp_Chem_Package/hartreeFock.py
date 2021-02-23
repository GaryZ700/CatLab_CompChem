#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

from math import erf
import numpy as np
from molecule import *
from pesMethod import *
from compChemGlobal import eigh

class hartreeFock(PESMethod):
    
    #Override global variables
    name = "Hartree-Fock"
    start = 0.7
    end = 10
    resolution = 10
    
    #local variables
    system = None
    convergence = pow(10, -15)
    maxCycles = 200
    
    def __init__(self, molecule, basis = "STO-3G"):
        self.system = molecule
        self.system.addBasis(basis)
    
###################################################################################

    def getWidgets(self):
        return False
    
###################################################################################

    #r in units of angstroms
    def implementation(self, r):   
        self.system.atomData[0].coord.z = self.system.atomData[1].coord.z + r
        return self.scf()

###################################################################################

    def scf(self):
        
        F = H = self.buildH()
        X, size = self.X()
        
        electronRepulsion = self.electronElectronRepulsion()
        startingF = F
        E = []
        converged = False
        
        cycles = 0
        while(not converged):

           #diagnolze the Fock matrix and convert it to MO basi
            F = np.matmul(np.matmul(X.transpose(), H), X)

            #diagnolize the Fock Matrix to obtain the MOs and the their respective energies
            MOEnergy, MO = eigh(F)

            #Transform the MO basis MOs to an AO basis
            C = np.matmul(X, MO)

            #compute the electron density, the two electron term, and then use G to compute the new Fock matrix
            P = self.densityMatrix(C, self.system.N, size)
            G = self.G(electronRepulsion, P, size)
            F = H + G
            
            E.append(self.expectationEnergy(H, F, P))
            
            if(len(E) > 2):
                if(abs(E[-2] - E[-1]) < self.convergence):
                    converged = True
                elif(cycles > self.maxCycles):
                    print("SCF Failed to Converge")
                    return False
            cycles += 1

        return E[-1] + self.nuclearRepulsion()
    
###################################################################################
    
    #Computes the initial integrals required for the computation
    #Returns the starting Fock matrix
    def buildH(self):
        H = np.array(self.kineticEnergy())
        for atom in self.nuclearAttraction():
            H += np.array(atom)

        return H
    
###################################################################################

    def kineticEnergy(self):

        #init empty list for the kinetic energy matrix
        T = []

        basis = self.system.getBasis()

        #iterate through all basis functions used within the molecule
        for index1, psi1 in enumerate(basis):
            T.append([])

            for index2, psi2 in enumerate(basis):
                T[index1].append(0)		

                #KE integral computed by taking gaussian 1 times -1/2 del squared acting upon gaussian 2
                #equation located on page 427 of Szabo

                #iterate through all the contracted gaussians of psi1 and psi2 
                for cg1 in psi1.contractedGaussians:
                    for cg2 in psi2.contractedGaussians:

                        ab = cg1.orbitalExponet * cg2.orbitalExponet
                        p = cg1.orbitalExponet + cg2.orbitalExponet
                        distanceSquared = pow((cg1.coord - cg2.coord).magnitude(), 2)

                        c1 = ab / p 
                        c2 = pow(math.pi / p, 3/2)
                        constant = cg1.contraction * cg2.contraction * cg1.constant * cg2.constant * c1 * c2

                        e = math.exp(-c1*distanceSquared)

                        T[index1][index2] += constant * (3 - (2*c1*distanceSquared) ) * e
        return T

###################################################################################

    def nuclearAttraction(self):

        #init nuclear attraction matrix 
        #each nuclear attraction list is composed of 1 matrix for each atom in the molecule, which includes a psi x psi matrix of values from the primative gaussian compuatation 
        V = []

        basis = self.system.getBasis()

        #used for graphing purposes
        distances = []
        errorInputs = []
        errorValues = []

        #iterate through all atoms for Z
        for atomIndex, atom in enumerate(self.system.atomData):        
            V.append([])

            #iterate through all basis functions used
            for index1, psi1 in enumerate(basis):
                V[atomIndex].append([])

                for index2, psi2 in enumerate(basis):
                    V[atomIndex][index1].append(0)

                    #iterate through all the primative gaussians
                    for cg1 in psi1.contractedGaussians:
                        for cg2 in psi2.contractedGaussians:

                            #compute data needed for the integral
                            ab = cg1.orbitalExponet * cg2.orbitalExponet
                            p = cg1.orbitalExponet + cg2.orbitalExponet

                            e = (-ab/p) *  pow((cg1.coord - cg2.coord).magnitude(), 2)

                            c1 = (-2 * math.pi) / p
                            cg3 = cg1.multiply(cg2)

                            constant = cg1.contraction * cg2.contraction * c1 * atom.Z * math.exp(e)
                            errorInput = p * math.pow((cg3.coord - atom.coord).magnitude(), 2)

                            #error input cutoff and else statement equation from Szabo pg. 437
                            #use first error equation to simulate asymptote for very small values
                            #but, due to numerical errors with python, small numbers only occurs 
                            #if index1==index2, but sometimes, such values may be larger,
                            #resulting in a negative error that is remedied by the cutoff equation
                            electronNuclearDistance = (cg3.coord - atom.coord).magnitude()
                            error = self.errorFunction(errorInput, electronNuclearDistance)

                            V[atomIndex][index1][index2] += constant * error * cg1.constant * cg2.constant 

        return V
    
###################################################################################
    
    def errorFunction(self, errorInput, distance):

        if(distance < 10**-70):
             return 1 - (errorInput/3)
        else:
             return 0.5 * pow(math.pi/errorInput, 0.5) * erf(pow(errorInput, 0.5))
            
###################################################################################

    def X(self):

        S = [] 

        #get basis function for the molecule
        #is an array with all basis functions from the atoms in the molecule contained within it
        basis = self.system.getBasis()

        #iterate through all basisSets used in the molecule
        for index1, psi1 in enumerate(basis):
                S.append([])
                for index2, psi2 in enumerate(basis):
                    S[index1].append(0)			

                    #overlap integral is simply the integral of basis function 1 times basis function 2
                    #is done with gaussians thorough gaussian multiplication, which results in a new 
                    #gaussian which is then integrated analytically, 
                    #and whose analytical equation is solved here for the overlap 

                    #iterate through all contracted gaussians that compose psi 1 and psi 2
                    for cg1 in psi1.contractedGaussians:
                        for cg2 in psi2.contractedGaussians:

                            #get overlap contracted gaussian 
                            cg3 = cg1.multiply(cg2)

                            #get constant to multiply overlap integral by 
                            constant = cg3.constant * cg1.contraction * cg2.contraction

                            #compute overlap coefficent
                            S[index1][index2] += constant * pow((math.pi/cg3.orbitalExponet), 3/2) 	

        size = len(S)
                            
        #init transformation matrix 
        X = np.zeros([size, size])

        #diagnolize S to obtain eigenvalues and vector
        eigenValues, eigenVectors = np.linalg.eigh(S)

        X = eigenVectors * (eigenValues ** -0.5)

        return X, size
    
###################################################################################

    def densityMatrix(self, C, N, size):

        P = np.zeros([size, size])

        #iterate through all indexes of the density matrix
        for u in range(size):
            for v in range(size):

                for a in range(int(N/2)):
                    P[u, v] += 2 * C[u,a] * C[v, a]
        return P

###################################################################################    
    
    def G(self, electronRepulsion, P, size):

        #init G matrix 
        G = np.zeros([size, size])

        #loop over all the required indexes to generate the G matrix
        for u in range(size):
            for v in range(size):
                for y in range(size):
                    for s in range(size):

                        G[u, v] += P[y, s] * (electronRepulsion[u][v][s][y] - ( 0.5 * electronRepulsion[u][y][s][v] ) )                
        return G
    
###################################################################################

    def expectationEnergy(self, H, F, P):

        #get size and init E to 0
        size = len(H)
        E = 0

        #iterate through all indexes needed
        for u in range(size):
            for v in range(size):
                   E += P[v, u] * (H[u, v] + F[u, v] )
        return E * 0.5

###################################################################################
    
    def electronElectronRepulsion(self):

        #init electron-electron repulsion list 
        #constructs a tensor equal to the size of the basis set squared
        electronRepulsion = []

        basis = self.system.getBasis()

        #iterate through PsiA1PsiA2 and PsiB1PsiB2
        for index1, psi1 in enumerate(basis):
            electronRepulsion.append([])
            for index2, psi2 in enumerate(basis):
                electronRepulsion[index1].append([])

                for index3, psi3 in enumerate(basis):
                    electronRepulsion[index1][index2].append([])
                    for index4, psi4 in enumerate(basis):
                        electronRepulsion[index1][index2][index3].append(0)

                        #iterate through all of the primative gaussians for each of the wavefunctions
                        for cg1 in psi1.contractedGaussians:
                            for cg2 in psi2.contractedGaussians:
                                for cg3 in psi3.contractedGaussians:
                                    for cg4 in psi4.contractedGaussians:

                                        pA = cg1.orbitalExponet + cg2.orbitalExponet
                                        pB = cg3.orbitalExponet + cg4.orbitalExponet
                                        abA = cg1.orbitalExponet * cg2.orbitalExponet
                                        abB = cg3.orbitalExponet * cg4.orbitalExponet

                                        pAB = pA + pB

                                        term1 = (2 * pow(math.pi, 5/2)) / (pA*pB*pow(pAB, 1/2))
                                        distanceAB = pow( (cg1.coord - cg2.coord).magnitude(), 2)
                                        distanceCD = pow( (cg3.coord - cg4.coord).magnitude(), 2)

                                        e = ((-abA/pA) * distanceAB) - ( (abB/pB) * distanceCD )

                                        cgAB = cg1.multiply(cg2)
                                        cgCD = cg3.multiply(cg4)

                                        distanceABCD = (cgAB.coord - cgCD.coord).magnitude()

                                        errorInput = ( (pA * pB) / pAB) * pow(distanceABCD, 2)
                                        error = self.errorFunction(errorInput, distanceABCD)

                                        constant = cg1.constant * cg2.constant * cg3.constant * cg4.constant * cg1.contraction * cg2.contraction * cg3.contraction * cg4.contraction

                                        electronRepulsion[index1][index2][index3][index4] += term1 * math.exp(e) * error * constant
        return electronRepulsion    
    
###################################################################################

    def nuclearRepulsion(self):

        repulsion = 0

        #iterate through all atoms present
        for atom1 in self.system.atomData:
            for atom2 in self.system.atomData:

                if(atom1 == atom2):
                    continue

                repulsion += (atom1.Z * atom2.Z) / (atom1.coord - atom2.coord).magnitude()

        return repulsion * 0.5