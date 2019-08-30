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