#Function Implementations for integrals used within the Hartree Fock Method
#uses equations on Pg. 175 and 427 of Szabo QM Textbook. 
#molecule, molecule object to compute overlap of

import math

def overlap(molecule):

    #init empty list for the overlap matrix
    S = []
	
	#iterate thorugh all atoms	
    for index1, atom1 in enumerate(molecule.atomData):
        S.append([])
        for index2, atom2 in enumerate(molecule.atomData):
            S[index1].append(0)			
            
            #prepare basis sets 
            psi1 = atom1.basisSet
            psi2 = atom2.basisSet

            #overlap integral is simply the integral of basis function 1 times basis function 2
            #is done with guassians thorough guassian multiplication, which results in a new guassian which is then integrated analytically, and whose analytical equation is solved here for the overlap 
            
            #iterate through all contracted guassians that compose psi1 and psi 2
            for cg1 in psi1.contractedGuassians:
                for cg2 in psi2.contractedGuassians:
                    
                    #get overlap contracted guassian 
                    cg3 = cg1.multiply(cg2)
                    
                    #get constant to multiply overlap integral by 
                    constant = cg3.constant * cg1.contraction * cg2.contraction
                 
                    #compute overlap coefficent
                    S[index1][index2] += constant * pow((math.pi/cg3.orbitalExponet), 3/2) 	

               
    return S

##################################################################################

def kineticEnergy(molecule):
    
    #init empty list for the kinetic energy matrix
    T = []
	
	#iterate thorugh all atoms	
    for index1, atom1 in enumerate(molecule.atomData):
        T.append([])
        for index2, atom2 in enumerate(molecule.atomData):
            T[index1].append(0)			
            
            #prepare basis sets 
            psi1 = atom1.basisSet
            psi2 = atom2.basisSet  
            
            #KE integral computed by taking guassian 1 times -1/2 del squared acting upon guassian 2
            #equation located on page 427 of Szabo
            
            #iterate through all the contracted guassians of psi1 and psi2 
            for cg1 in psi1.contractedGuassians:
                for cg2 in psi2.contractedGuassians:
                
                    ab = cg1.orbitalExponet * cg2.orbitalExponet
                    p = cg1.orbitalExponet + cg2.orbitalExponet
                    c1 = ab / p 
                    c2 = pow(math.pi / p, 3/2)
                    distanceSquared = pow((cg1.coord - cg2.coord).magnitude(), 2)
                    e = math.exp(-c1*distanceSquared)
                    constant = cg1.contraction * cg2.contraction * cg1.constant * cg2.constant
                   
                    T[index1][index2] += constant * c1 * (3 - (2*c1*distanceSquared) ) * c2 * e
    
    return T