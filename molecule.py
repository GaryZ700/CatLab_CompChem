#Python Molecule Class to be used for Quantom Mechanical Simulations Purposes
#Written by Gary Zeri for the Cat Lab Research Group at Chapman University. 
#class handle vectors for atomic coordinates

import math

class vector():
    
    #declare all variables here 
    x = 0
    y = 0
    z = 0
    
    #constructor function for the vector class
    #by default returns the zero vector
    def __init__(self, x=0, y=0, z=0):
        
        self.x = x
        self.y = y
        self.z = z
        
#--------------------------------------------------------------------------------
    
    #addition of two vectors function
    def __add__(self, other):
        
        return vector(self.x + other.x,
                      self.y + other.y, 
                      self.z + other.z)

#--------------------------------------------------------------------------------

    #overload subtraction operator
    def __sub__(self, other):
        
        return vector(self.x - other.x, 
                      self.y - other.y, 
                      self.z - other.z)
    
#--------------------------------------------------------------------------------

    #function to get magnitude of the vector
    def magnitude(self):
        
        randicand = (self.x ** 2) + (self.y ** 2) + ( self.z ** 2)
        return math.sqrt(randicand)

#--------------------------------------------------------------------------------

    #function to print the vector to the screen
    def display(self):
        
        print("\nX: " + str(self.x) + " Y: " + str(self.y) + " Z: " + str(self.z))

##################################################################################
        
#class to handle guassian object
class guassian():

    #declare all variables here
    orbitalExponet = 0
    coord = vector()
    constant = 0

    #constructor function for the guassian class
    #orbitalExponet, should be guassian exponet for this orbital
    #coord should be a new vector object for the guassian center, which is the atomic center
    def __init__(self, orbitalExponet, coord):
    
        self.orbitalExponet = orbitalExponet
        self.coord = coord

        #for normalization, from Szabo on pg. 168
        self.constant = pow((2.0 * orbitalExponet / math.pi), 3/4) 
#--------------------------------------------------------------------------------
    #All class methods defined here

    #multipies two guassians together and returns a new guassian
    #takes another guassian as a parameter
    #located on pg. 169
    def multiply(self, guassian2):

        #compute new exponet for the guassian
        p = self.orbitalExponet + guassian2.orbitalExponet

        #ab is the multiplication of the two guassian orbitals
        ab = self.orbitalExponet * guassian2.orbitalExponet
        
        #e is the e used to calcuate K, the constant difference between the multiplication of two guassians
        e = math.exp( (-ab/p) * pow( (self.coord - guassian2.coord).magnitude(), 2 ) )
        K = pow((2.0*ab / (p*math.pi)), 3/4) * e

        #compute new position
        R = self.coord - guassian2.coord

        #create new guassian and multiply K in to the constant
        multipliedGuassian = guassian(p, R)
        multipliedGuassian.constant *= K

        return multipliedGuassian

##################################################################################
    
#class to handle basis sets of guassian natures
class guassianBasis():

    #declare all variables here
    contractedGuassians = []

    #constructor function for the guassian basis class
    #basisName, string of basis set to use
    #coord is center of atom that basis is attached to, must be a vector
    def __init__(self, basisName, coord):
        self.addBasis(basisName, coord)

#--------------------------------------------------------------------------------
    #All class functions defined here
    
    #function to addBasis to this guassian
    #basisName, string of name for basis set
    #at the moment, only sets the STO-3G basis set for hydrogen atoms
    #coord is vector for center of the contracted guassians to be added to this basis set
    def addBasis(self, basisName, coord):
        
        contractionCoeffs = [0.15432897, 0.53532814, 0.44463454]
        orbitalExponets = [3.42525091, 0.62391373, 0.16885540] 

        #iterate through all wavefunctions specified by the basis 
        #and iterate through all contracted guassians that are a part of the wavefunction 
        for cg in range(len(contractionCoeffs)):
            self.contractedGuassians.append( guassian(orbitalExponets[cg], coord))
            self.contractedGuassians[cg].constant *= contractionCoeffs[cg]
        
##################################################################################
                    
#contains an atom class that is used to build up the molecule class 
class atom():

    #all variables declared here
    coord = vector()
    Z = 1
    N = 1
    basisSet = 0

    #constructor fucntion for the atom class
    #coord, vector of atom coordinates
    #atomicNumber, integer that represents atomic number of the element, from 1 to infinity
    #by default creates a hydrogen atom at the (0,0,0)
    def __init__(self, coord=vector(), Z=1, N=1):

    #assign position to coordinates
        self.coord = coord

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
            atom.basisSet = guassianBasis(basisName, atom.coord)
