#Python Molecule Class to be used for Quantom Mechanical Simulations Purposes
#Written by Gary Zeri for the Cat Lab Research Group at Chapman University.

import sys
import math
import json

#folder where the basisset json files are located
BASIS_SET_FOLDER = "./basisSets/"

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
    
    #multiplication of vector by a scalar constant or performs the dot product of two vectors
    def __mul__(self, other):
        
        #if multiplying another vector, perform the dot product
        if(type(other) == vector ):
            return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
        else:
            return vector(self.x * other,
                          self.y * other,
                          self.z * other)
        
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
       
        print("X: " + str(self.x) + " Y: " + str(self.y) + " Z: " + str(self.z))

##################################################################################

#class to handle guassian object
class guassian():

    #declare all variables here
    orbitalExponet = 0
    coord = vector()
    constant = 0
    contraction = 0
    normalization = 0

    #constructor function for the guassian class
    #orbitalExponet, should be guassian exponet for this orbital
    #coord should be a new vector object for the guassian center, which is the atomic center
    #contraction, contraction used in HF method for guassian basis set to weight power of single guassian, default value is 1
    def __init__(self, orbitalExponet, coord, contraction=1):

        self.orbitalExponet = orbitalExponet
        self.coord = coord
        self.contraction = contraction
        
        #for normalization, from Szabo on pg. 168
        self.constant = pow((2.0 * orbitalExponet / math.pi), 3/4)
        self.normalization = self.constant
        
#--------------------------------------------------------------------------------
    #All class methods defined here

    #multipies two guassians together and returns a new guassian
    #takes another guassian as a parameter
    #located on pg. 154
    def multiply(self, guassian2):

        #compute new exponet for the guassian
        p = self.orbitalExponet + guassian2.orbitalExponet

        #ab is the multiplication of the two guassian orbitals
        ab = self.orbitalExponet * guassian2.orbitalExponet

        #e is the e used to calcuate K, the constant difference between the multiplication of two guassians
        e = math.exp( (-ab/p) * pow( (self.coord - guassian2.coord).magnitude(), 2 ) )
        K = pow((2.0*ab / (p*math.pi)), 3/4) * e

        #compute new position
        RA = self.coord * self.orbitalExponet        
        RB = guassian2.coord * guassian2.orbitalExponet 
        RC = (RA + RB) * (1/p)
    
        #create new guassian and multiply K in to the constant
        multipliedGuassian = guassian(p, RC)
        multipliedGuassian.constant *= K

        return multipliedGuassian

##################################################################################

#class to handle basis sets of guassian natures
class guassianBasis():

    #declare all variables here
    contractedGuassians = []
    basisName = ""
    
    #constructor function for the guassian basis class
    #basisName, string of basis set to use
    #coord is center of atom that basis is attached to, must be a vector
    #Z, integer representing atomic number of atom whose basis set is being gathered
    def __init__(self, basisName, coord, Z):
        self.contractedGuassians = []
        self.addBasis(basisName, coord, Z)
        self.basisName = basisName
        
#--------------------------------------------------------------------------------
    
    #loadsBasisSet from json basis files that can be downloaded from the Basis Set Exchange
    #Basis Set Exchange Site: https://www.basissetexchange.org/
    #if basis name is not valid, or basis set file not in the current directory
    #Z, atomic number of atom
    def loadBasisSet(self, basisName, Z):
        
        basisFile = open(BASIS_SET_FOLDER+basisName+".json", 'r')
        basisData = json.load(basisFile)
        basisFile.close()
        
        shellData = basisData['elements'][str(Z)]['electron_shells'][0]
        
        #return list of coefficents and exponets as numbers
        return [float(x) for x in shellData['coefficients'][0]], [float(x) for x in shellData['exponents']]
        
#--------------------------------------------------------------------------------
    #All class functions defined here

    #function to addBasis to this guassian
    #basisName, string of name for basis set
    #at the moment, only sets the STO-3G basis set for hydrogen atoms
    #coord is vector for center of the contracted guassians to be added to this basis set
    #Z, integer representing atomic number of atom whose basis set is being gathered
    def addBasis(self, basisName, coord, Z):
       
        #try-except to load data from json file
        #meant to handle file not found exception
        try:
            contractionCoeffs, orbitalExponets = self.loadBasisSet(basisName.upper(), Z)
        except:
            print("Basis '" + basisName + "' not found in '" + BASIS_SET_FOLDER + "'")
            print("Hartree Code will quit now.")
            sys.exit()
        
        #iterate through all wavefunctions specified by the basis
        #and iterate through all contracted guassians that are a part of the wavefunction
        if(len(self.contractedGuassians) == 0):
            for cg in range(len(contractionCoeffs)):
                self.contractedGuassians.append( guassian(orbitalExponets[cg], coord, contractionCoeffs[cg]))
                
#--------------------------------------------------------------------------------
   
    def display(self):
        print("GB Len = " + str(len(self.contractedGuassians)))
        for cg in self.contractedGuassians:
            cg.coord.display()
        
        print("-------------------------------------")
      
##################################################################################

#contains an atom class that is used to build up the molecule class
#all atomic coordinates are in AU, Szabo Pg. 159
class atom():

    #all variables declared here
    coord = vector()
    Z = 1
    N = 1
    basisSet = 0
    mass = 0

    #constructor fucntion for the atom class
    #coord, vector of atom coordinates
    #atomicNumber, integer that represents atomic number of the element, from 1 to infinity
    #neutrons, number of neutrons this atom contains, used for mass computation
    #by default creates a hydrogen atom at the (0,0,0)
    def __init__(self, coord=vector(), Z=1, N=1, neutrons=0):

        #assign position to coordinates
        self.coord = coord

        #assign atomic number, electron number, and Mass in AU
        self.Z = Z
        self.N = N
        self.mass = Z + neutrons
        
#--------------------------------------------------------------------------------
    
    def display(self):
        
        print("Atomic Number: " + str(self.Z) + ", Electrons: " + str(self.N) + ", Coordinate: ", end="")
        self.coord.display()
    
#################################################################################

#class to handle combinations of atoms for atomic simulations
class molecule():

    #variables declared here
    #atomData is list to hold atom objects
    atomData = []
    N = 0
    basisName = "No Basis Set Specified"
    
    #constructor function for the molecule class
    #atoms, list of atom objects to add in 
    def __init__(self, atoms=[]):

        #reset class variables
        self.atomData = []
        self.N = 0
        self.basisName = "No Basis Set Specified"
        
        #iterate through all atoms passed into the constuctor function,
        #and add them into the molecule data structure
        for atom in atoms:
                self.addAtom(atom)
                
#--------------------------------------------------------------------------------

    def addAtom(self, atom):
        self.atomData.append(atom)
        self.N += atom.N
        
#--------------------------------------------------------------------------------

    def addBasis(self, basisName):

        self.basisName = basisName
        
        for atom in range(len(self.atomData)):
            self.atomData[atom].basisSet = guassianBasis(basisName, self.atomData[atom].coord, self.atomData[atom].Z)
            
#--------------------------------------------------------------------------------
    
    def display(self):
        
        print("Molecule")
        print("Basis Set: " + self.basisName)
        print("Total Number of Electrons: " + str(self.N))
        
        #display all atoms contained within this molecule, use a for loop to iterate over all the atoms
        print("Atoms: ")
        for atom in self.atomData:
            print("     ", end="")
            atom.display()