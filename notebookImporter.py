#Python Script to allow a Juypter notebook to import code from other notebooks
#Based off the code described on the Juypter Notebook Documentation: https://nbviewer.jupyter.org/github/ipython/ipython/blob/master/examples/IPython%20Kernel/Importing%20Notebooks.ipynb

import os, sys, types, nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython import get_ipython

#name is string name of file to import not including .pynb
#will only import files that are located within the same directory as the file performing the import
def importNotebook(name):
    
    fileName = "./" + name + ".ipynb"
    
    #check whether or the file name exists
    if(not os.path.isfile(fileName)):
        print("File " + fileName + " does not exist, please try again.")
        return -1
  
    #createa a new module to hold the Juypyter notbook functions
    module = types.ModuleType(name)
    module.__file__ = fileName
    module.__dict__["get_ipython"] = get_ipython
    shell = InteractiveShell.instance()
    
    #load data from the notebook 
    with open(fileName, 'r') as f:
        notebookData = nbformat.read(f, 4)["cells"]
        
    #make all text code executable
    for cell in notebookData:
        
        #check if cell contains code 
        if(cell.cell_type == "code"):
            code = shell.input_transformer_manager.transform_cell(cell.source)
            exec(code, module.__dict__)    
            
    return module    