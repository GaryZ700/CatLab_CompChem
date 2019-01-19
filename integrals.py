#Function Implementations for integrals used within the Hartree Fock Method
#uses equations on Pg. 175 and 427 of Szabo QM Textbook. 
#molecule, molecule object to compute overlap of
def overlap(molecule):

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
			S[index1][index2] += psi1.multiply(psi2).integrate()	
	
	return S
