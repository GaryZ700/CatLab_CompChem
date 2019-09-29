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

#class to handle gaussian objects
class gaussian():

    #declare all variables here
    orbitalExponet = 0
    coord = vector()
    constant = 0
    contraction = 0
    normalization = 0

    #constructor function for the gaussianclass
    #orbitalExponet, should be gaussianexponet for this orbital
    #coord should be a new vector object for the gaussiancenter, which is the atomic center
    #contraction, contraction used in HF method for gaussianbasis set to weight power of single gaussian, default value is 1
    def __init__(self, orbitalExponet, coord, contraction=1):

        self.orbitalExponet = orbitalExponet
        self.coord = coord
        self.contraction = contraction
        
        #for normalization, from Szabo on pg. 168
        self.constant = pow((2.0 * orbitalExponet / math.pi), 3/4)
        self.normalization = self.constant
        
#--------------------------------------------------------------------------------
    #All class methods defined here

    #multipies two gaussians together and returns a new gaussian
    #takes another gaussianas a parameter
    #located on pg. 154
    def multiply(self, gaussian2):

        #compute new exponet for the gaussian
        p = self.orbitalExponet + gaussian2.orbitalExponet

        #ab is the multiplication of the two gaussianorbitals
        ab = self.orbitalExponet * gaussian2.orbitalExponet

        #e is the e used to calcuate K, the constant difference between the multiplication of two gaussians
        e = math.exp( (-ab/p) * pow( (self.coord - gaussian2.coord).magnitude(), 2 ) )
        K = pow((2.0*ab / (p*math.pi)), 3/4) * e

        #compute new position
        RA = self.coord * self.orbitalExponet        
        RB = gaussian2.coord * gaussian2.orbitalExponet 
        RC = (RA + RB) * (1/p)
    
        #create new gaussianand multiply K in to the constant
        multipliedGaussian= gaussian(p, RC)
        multipliedGaussian.constant *= K

        return multipliedGaussian
    
#--------------------------------------------------------------------------------
    
    #computes the value of this guassian function at the specified r value
    def compute(self, r):
        return  self.contraction * self.normalization * math.exp(-self.orbitalExponet * pow(r-self.coord.magnitude(), 2)) 
    
#--------------------------------------------------------------------------------

    #computes the value of the 2nd partial derivate of this function 
    def compute2ndPD(self, r):
        return 4 * self.normalization * self.contraction * pow(self.orbitalExponet*r, 2) * math.exp(-self.orbitalExponet * pow(r, 2))

##################################################################################

#class to handle basis sets of gaussiannatures
class gaussianBasis():

    #declare all variables here
    contractedGaussians = []
    basisName = ""
    
    #constructor function for the gaussianbasis class
    #electronShell, basis data electron shell json object
    #atom object to which this basisSet is being added to
    def __init__(self, electronShell, atom, basisName):
        self.functions = []
        self.contractedGaussians = []
        self.basisName = basisName

        self.addBasis(electronShell, atom)

#--------------------------------------------------------------------------------
    
    #All class functions defined here

    #function to addBasis to this gaussian
    #electronShell, electronshell data from json data file
    #atom, atom to which this basis set is being appened to 
    def addBasis(self, electronShell, atom):
        
        #loop over all set of coeffiencts used to define contracted gaussians for this basis set
        for coefficientData in electronShell["coefficients"]:
        
            #loop over all the exponets and coefficents in the electron shell
            for index in range(len(electronShell["exponents"])):

                #get exponet and coeff from the shell data
                exponent = float(electronShell["exponents"][index])
                coefficient = float(coefficientData[index])

                #add in a new primative gaussianwith from the coeffiecent and exponet
                self.contractedGaussians.append(gaussian(exponent, atom.coord, coefficient))
            
#--------------------------------------------------------------------------------
   
    def display(self):
        print("GB Len = " + str(len(self.contractedgaussians)))
        for cg in self.contractedgaussians:
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
    basisSet = []
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
        self.basisSet = []
        
#--------------------------------------------------------------------------------
    
    def display(self):
        
        print("Atomic Number: " + str(self.Z) + ", Electrons: " + str(self.N) + ", Coordinate: ", end="")
        self.coord.display()
        
#--------------------------------------------------------------------------------

    def addBasis(self, basisData, basisName):
        
        #loop over all electron shells used in this basis set
        for electronShell in basisData[str(self.Z)]["electron_shells"]:
            self.basisSet.append(gaussianBasis(electronShell, self, basisName))
      
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
        
        #load the basisSet data 
        #use a try-execept block to ensure that the basis set exists
        try:
            basisFile = open(BASIS_SET_FOLDER+basisName+".json", 'r')
            basisData = json.load(basisFile)["elements"]
            basisFile.close()        
        except:
            print("Basis '" + basisName + "' not found in '" + BASIS_SET_FOLDER + "'")
            print("Hartree Code will quit now.")
            sys.exit()
        
        #loop over all the atoms, and have each atom assign a basis set to itself
        for atom in range(len(self.atomData)):
            self.atomData[atom].addBasis(basisData, basisName)
            
#--------------------------------------------------------------------------------

    #getBasis functions returns a list of all basis functions used by atoms within this molecule
    def getBasis(self):
        
        basisList = []
        
        #loop over all atoms present
        for atom in self.atomData:
            #loop over all basis functions used within the atom
            for basis in atom.basisSet:
                basisList.append(basis)
                
        return basisList   
    
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