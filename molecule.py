#Python Molecule Class to be used for Quantom Mechanical Simulations Purposes
#Written by Gary Zeri for the Cat Lab Research Group at Chapman University. 

#class to handle guassian objects 
class guassian():

	#declare all variables here
	orbitalExponet = 0
	coord = []
	constant = 0
	
	#constructor function for the guassian class
	def __init__(self, orbitalExponet, coord):

		self.orbitalExponet = orbitalExponet
		self.coord = coord
		
		#for normalization, from Szabo on pg. 168
		constant = pow((2.0 * orbitalExponet / math.pi), 3/4) 

#--------------------------------------------------------------------------------
	#All class methods defined here

	#multipies two guassians together and returns a new guassian
	#takes another guassian as a parameter
	def multiply(guassian):
		
		#compute new exponet for the guassian
		p = self.orbitalExponet + guassian.orbitalExponet
		
		#compute terms to help in calculating new position of guassian
		ab = self.orbitalExponet * guassian.orbitalExponet
		e = math.exp( (-ab/p) * pow((self.cord.difference(guassian.coord).magnitude),2))
		K = pow((2.0*ab / (p*math.pi)), 3/4) * e

		#compute new position
		R = self.coord - guassian.coord

		#create new guassian and multiply K in to the constant
		multipliedGuassian = guassian(p, R)
		multipliedGuassian.constant *= K
		
		return multipliedGuassian
 	
#class to handle basis sets of guassian natures
class guassianBasis():

	#declare all variables here
	psi = []

	#constructor function for the guassian basis class
	#basisName, string of basis set to use
	def __init__(self, basisName):
		self.addBasis(basisName)

#--------------------------------------------------------------------------------
	#All class functions defined here
	
	#function to addBasis to this guassian
	#basisName, string of name for basis set
	#at the moment, only sets the STO-3G basis set for hydrogen atoms
	def addBasis(self, basisName):
		contractionCoeffs = [0.15432897, 0.53532814, 0.44463454]
		orbitalExponets = [3.42525091, 0.62391373, 0.16885540] 

		for i in range(3):


#--------------------------------------------------------------------------------
	
	#function to multiply this guassian with another guassian basis
	#returns a new guassianBasis object
	#takes another guassianBasis object to multiply with this one
	def multiply(guassian):

		#iterate through all contracted guassians that make up the final orbital
		for cg1 in self.range(len(self.orbitalExponets)):
			for cg2 in self.range(len(guassian.orbitalExponets)):
				
				p = self.orbitalExponets[cg1] + guassian.orbitalExponets[cg2]
				center = np.matrix([0,0,0])

						

#contains an atom class that is used to build up the molecule class 
class atom():

	#all variables declared here
	x = 0
	y = 0
	z = 0
	Z = 1
	N = 1
	basisSet = 0	
	
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

#--------------------------------------------------------------------------------

	def addBasis(self, basisName):

		for atom in self.atomData:
			atom.basisSet = guassianBasis(basisName)
