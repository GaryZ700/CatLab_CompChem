#Python Implementation of the Hartree Fock Method
#Procedures listed in the code follow as described in Modern Quantum Chemistry: Introduction to Advanced Electronic Structure Theory, By Attila Szabo and Neil S. Ostlund

from molecule import molecule
from molecule import atom
import numpy as np
import integrals

#Step 1
#Specify Molecules, Nuclear Coordinates, and Charge of the nucli Number of Electrons,

#generate a sole hydrogen ion with 2 electrons
hydrogenIon = molecule()
hydrogenIon.addAtom(atom([0,0,0], 1, 2))

moleculerSystem = hydrogenIon

#and a basis set, for now will add default basis of STO-3G for hydrogen to all atoms
moleculerSystem.addBasis("STO-3G")


#Step 2
#Calculate Integrals
#Overlap, KE, Nuclear Attraaction, Electron Repulsion
S = integrals.overlap(molecule)
print(S)

#Step 3
#Dignolize Overlap Matrix and Obtain transformation matrix X

#Step 4
#Obtain guess Density matrix, P

#Step 5 
#Calculate Contraction of Density Matrix with Electron Repulsion, G Matrix

#Step 6
#Calculate Fock matrix, core matrix + G matrix

#Step 7
#Using X diagnolize Fock Matrix

#Step 8
#Diagnolize F' to get C' and E'

#Step 9
#Calculate C from C'

#Step 10
#From P for next iteration of HF Procedure

#Step 11
#Determine if current P is close "enough" to previos P, 
#	if no iterate again start from step 5
#	if yes, then stop iterating, HF procedure completed, and use final C matrix to compute physical properties


