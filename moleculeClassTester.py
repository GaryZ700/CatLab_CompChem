from molecule import atom 
from molecule import molecule 

#get default atom
a1 = atom()

a2 = atom([1,2,3], 5, 10)

molecule1 = molecule([a1, a2])

molecule1.addAtom(atom([3,2,1], 45, 500))

molecule1.addBasis("STO-3G")

for atom in molecule.atomData:

	print("Atom X = " + str(atom.x))
	print("Atom Y = " + str(atom.y))
	print("Atom Z = " + str(atom.z))
	print("Atomic Number = " + str(atom.Z))
	print("Atom N = " + str(atom.N))
	print("\n\n")
	print("Basis" + str(atom.basisSet.contractionCoeffs))
	print(atom.basisSet.orbitalExponets)


print("Total N =" + str(molecule1.N))
