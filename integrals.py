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
                    
                    #compute overlap coefficent
                    S[index1][index2] += cg3.constant * pow((math.pi/cg3.orbitalExponet), 3/2)	
                    print(str(cg1.constant) + " Constant1")
                    print(str(cg2.constant) + " Constant2")
                    print(cg3.orbitalExponet)
	
    return S
