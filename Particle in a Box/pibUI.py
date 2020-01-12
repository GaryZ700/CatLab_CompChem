#Written by Gary Zeri, Computer Science Student at Chapman University and Member of the LaRue CatLab
#Class that Handles UI for Juypter Notebook Particle in a Box

class UI:
    
    #Declare All Global Variables Here
    dimensions = 1
    
    def __init__(self, dim):
        self.dimension = dim
        self.buildUI()
        
#------------------------------------------------------------------------

    #Builds the UI
    def buildUI():

        #Quantum Numer Input System
        qnUI = widgets.Text(
            value = "1, 2, 3",
            description = "",  
        )
        qnLabel = widgets.Label("Quantum Number(s)")
        qnLabel.layout.width = "35%"

        #Box Length Input System in Bohr Radius
        LUI = widgets.BoundedFloatText(
            value = 10,
            min = pow(10, -100),
            max = pow(10, 100)
        )
        LUILabel = widgets.Label("Box Length in Bohr Radius")
        LUILabel.layout.width = "35%"

        #Number of Points Input System, 
        #The larger this number the greater the resolution of the graph will be
        pointsUI = widgets.BoundedIntText(
            min = 0, 
            max = pow(10,100),
            value = 200
        )

        #Mass of the Particle in A.U.
        mUI = widgets.BoundedIntText(
            min = 1,
            max = pow(10, 100),
            value = 1,
        )
        mLabel = widgets.Label("Mass of Particle in A.U.")
        mLabel.layout.width = "35%"

        #Create inputs required for the 2D PIB
        if(self.dimension == 2):

            #Quantum Numer Input System
            qnUI2 = widgets.Text(
                value = "1, 2, 3",
                description = "",  
            )
            qnLabel2 = widgets.Label("Quantum Number(s)")
            qnLabel2.layout.width = "35%"

            #Box Length Input System in Bohr Radius
            LUI2 = widgets.BoundedFloatText(
                value = 10,
                min = pow(10, -100),
                max = pow(10, 100)
            )
            LUILabel2 = widgets.Label("Box Length in Bohr Radius")
            LUILabel2.layout.width = "35%"
            
        #prepare layout for the input widgets
        #then start the widgets to run
        qnLayout = [qnLabel, qnUI]
        LUILayout = [LUILabel, LUI]
        
        if(self.dimension == 2):
            qnLayout.extend( [qnLabel2, qnUI2] )
            LUILayout.extend( [LUILabel2, LUI2] )
        
        layout = widgets.VBox([widgets.HBox(qnLayout),
                               widgets.HBox(LUILayout),
                               widgets.HBox([mLabel, mUI]),
                               widgets.HBox([pointsLabel, pointsUI]),
                               widgets.HBox([executeButton])
                              ])    
