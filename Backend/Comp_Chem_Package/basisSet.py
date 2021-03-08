#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Class that specifies the methods and functionality of a basis set composed of basisfunctions

from compChemGlobal import plot, widgets, Graphable
from how import *

class basisSet(Graphable):
    
    #Declare all global variables here
    basisFunctionClass = None
    basisFunctions = None
    size = None
    diatomicConstants = None
    
    
    def __init__(self, diatomicConstants, basisFunctionClass=how, size=10):
        super().__init__()
        self.size = size
        self.basisFunctionClass = basisFunctionClass
        self.diatomicConstants = diatomicConstants
        self.xTitle = "r in Angstroms"
        self.yTitle = "Wavenumbers"
        self.buildBasisSet()
        
 ###################################################################################
    
    def buildBasisSet(self):
        
        self.basisFunctions = []
        graphableObjects = []
        for n in range(self.size):
            self.basisFunctions.append(self.basisFunctionClass(self.diatomicConstants, n))  
            graphableObjects.append(self.basisFunctions[-1])
            graphableObjects.append(squaredBasisFunction(self.basisFunctions[-1]))
        
        #get needed graphing data
        self.addGraphableObject(graphableObjects[::-1])
        function = self.basisFunctions[-1]
        self.graphTitle = function.name + " Basis Set"
        self.start = function.start 
        self.end = function.end
        self.isGraphable = False
   
    ###################################################################################
    
    #computes the value of the nth basisfunction at position r
    def value(self, n, r):
        
        if(n >= self.size):
            print("Warning! Basis function n=" + str(n) + " can not be found. Max n is " + str(n-1) + ".")
        elif(n < 0):
            print("Warning! Can retrive basis function n=" + str(n) + " lowest n is 0.")
        else:
            return self.basisFunctions[n].value(r)
   
    ###################################################################################
  
    #returns the list of basis functions within the basisSet
    def getBasisSet(self):
        return self.basisFunctions
    
    ###################################################################################

    #returns the nth specified basis function
    def getBasisFunction(self, n):
        return self.basisFunctions[n]
        
    ###################################################################################
    
    def getWidgets(self, traces, widgetD):
        
        revTraces = traces[::-1]
        
        #textbox used to show or hide wavefunctions
        visibleWavefunctions = widgets.Text(
            value = "0-" + str(len(traces) // 2),
            description = '<p style="font-family:verdana;font-size:15px">Visible Ψs</p>'
        )
        
        probability = widgets.Dropdown( options = ["Standard", 
                                                   "Probability Distribution", 
                                                   "Standard & Probability"],
        description = '<p style="font-family:verdana;font-size:15px">Mode</p>')
        
        def visibleWavefunctionsUpdate(value, modeValue):
         
            visibility = []
            
            try:
                for startEnd in value.split(";"):
                    if("-" in startEnd):
                        startEnd = [int(value) for value in startEnd.split("-")]
                        visibility.extend( range(startEnd[0], startEnd[1]+1))
                    else:
                        visibility.append(int(startEnd))
            except:
                return 
            
            if (modeValue == "Standard"):
                mode = 1
            elif (modeValue == "Probability Distribution"):
                mode = 0
            else:
                mode = 2

            for index, trace in enumerate(revTraces):    
                #evens are squared
                #odds are normal
                visibleType = index % 2
                
                #maps square and normal function to a single index
                index2 = index - visibleType - index // 2
        
                if index2 in visibility and visibleType ^ mode: 
                    trace.visible = True
                else:
                    trace.visible = False
                    
        vsfWrapper = lambda value : visibleWavefunctionsUpdate(visibleWavefunctions.value, 
                                                               probability.value)
        vsfWrapper(0)
        visibleWavefunctions.observe(vsfWrapper)
        probability.observe(vsfWrapper)
        
        return [[visibleWavefunctions, 0], [probability, 1]]
    
 ###################################################################################
    
    def __iter__(self):
        self._index=0
        return self

###################################################################################

    def __next__(self):
        if(self._index == self.size):
            raise StopIteration
        
        self._index += 1
        return self.basisFunctions[self._index-1]
    
###################################################################################

    class _iterator:
        
        basisSetSelf = None
        index = 0
        
        def __init__(self, basisSetSelf):
            self.basisSetSelf = basisSetSelf
            
        #---------------------------------------------------
        
        def __next__(self):
            if(self.index == self.basisSetSelf.size):
                raise StopIteration
            self.index += 1
            return self.basisSetSelf.basisFunctions[self.index-1]

    def __iter__(self):
        return self._iterator(self)

###################################################################################

    def __len__(self):
        return self.size
    
###################################################################################

    def __getitem__(self, key):
        return self.basisFunctions[key]