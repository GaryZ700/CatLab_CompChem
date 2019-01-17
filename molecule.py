#Python Molecule Class to be used for Quantom Mechanical Simulations Purposes
#Written by Gary Zeri for the Cat Lab Research Group at Chapman University. 


#contains an atom class that is used to build up the molecule class 
class atom():

	#all variables declared here
	x = 0
	y = 0
	z = 0
	Z = 1
	N = 1	

	#constructor fucntion for the atom class
	#coord, list of coordinates in [x,y,z] format
	#atomicNumber, integer that represents atomic number of the element, from 1 to infinity
	#by default creates a hydrogen atom at the (0,0,0)
	def __init__(self, coord=[0,0,0], Z=1, N=1):
		
		#assign position to coordinates		
		self.x = coord[0]
		self.y = coord[1]
		self.z = coord[2]

		#assign atomic number, and electron number
		self.Z = Z
		self.N = N

#################################################################################

#class to handle combinations of atoms for atomic simulations
class molecule():
	
	#variables declared here
	#atomData is list to hold atom objects
	atomData = []
	N = 0

	#constructor function for the molecule class
	#atoms, can be either list of Chemical Symbols as strings to represent atoms, or list of actual atom objects to add to the molecule
	#coordinates are only used if Chemical symbols supplied to the atoms list, and represent coordinates of the atoms 
	def __init__(self, atoms=[], coordinates=[]):

		stringAtomCounter = 0

		#iterate through all atoms passed into the constuctor function 
		for atom in atoms:
			
			#if string atom name was passed in, then add atom in as string
			if(type(atom) == str):
				self.addStringAtom(atom, coordinates[stringAtomCounter])
				stringAtomCounter += 1
			#else, add in atom as an atom object
			else:
				self.addAtom(atom)

#--------------------------------------------------------------------------------
	#All class functions defined here

	def addStringAtom(self):
		#atomData.append(atom(coord, atomStringToNumber()))
		print("pass")	

#--------------------------------------------------------------------------------

	def addAtom(self, atom):
		self.atomData.append(atom)		
		self.N += atom.N

