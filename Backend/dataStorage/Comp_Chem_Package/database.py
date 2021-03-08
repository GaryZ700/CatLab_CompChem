#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#This Python file provides a high-level interface towards interacting with the database for this package
#The point of this database is to store computed values in order to relerage them at a later time to avoid 
#long recalulations of frequently used data

import os
import sqlite3 as underlyingDB
import pickle

class dataBase():

    #Declare global variables here
    dbPath = ""
        
    def __init__(self):
        self.dbPath = "../compChemDB" if os.name == "posix" else "..\\compChemDB.db" 
        
        #create the starting database
        if(not os.path.exists(self.dbPath)):
            self.createDB()
###################################################################################

    def createDB(self):
        conn = self.detDBConn()
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS wavefunctions(calculation string PRIMARY KEY, eigenValues BLOB, eigenVectors BLOB, )")
        
###################################################################################

    def getDBConn(self):
        return underlyingDB.connect(self.dbPath)
    
###################################################################################

    def writeWavefunction(self, solution):
        conn = self.getDBConn()
        
###################################################################################
