#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#This Python file provides a high-level interface towards interacting with the database for this package
#The point of this database is to store computed values in order to relerage them at a later time to avoid 
#long recalulations of frequently used data

import os
import sqlite3 
import numpy as np
from nistScraper import buildDiatomicConstants

class dataBase():

    #Declare global variables here
    dbPath = ""
    flatArrayToDBSep = ",  "
    arrayToDBSep = "\n"
        
    def __init__(self):
        self.dbPath = "/".join(__file__.split("/")[:-1] + ["compChemDB.db"]) if os.name == "posix" else "\\".join(__file__.split("\\")[:-1] + ["compChemDB.db"])  
        #create format an empty database if one does not alreadly exist
        if(not os.path.exists(self.dbPath)):
            self.formatDB()

###################################################################################

    def formatDB(self):
        self.connect()
        
        self.cursor.execute("CREATE TABLE diatomic_constants(molecule string PRIMARY KEY, state string, T DOUBLE, w DOUBLE, wx DOUBLE, wy DOUBLE, wz DOUBLE, B DOUBLE, a DOUBLE, y DOUBLE, D DOUBLE, re DOUBLE, u DOUBLE)")
        self.cursor.execute("CREATE TABLE schrodinger_solutions(molecule string, basis string, size int, eigen_values string, eigen_vectors string, max_wavefunctions int, pes string, method string, CONSTRAINT solution PRIMARY KEY (molecule, basis, size, pes, method))")
        self.cursor.execute("CREATE TABLE morse_potentials(molecule string, method string, a string, CONSTRAINT potential PRIMARY KEY (molecule, method))")
        self.cursor.execute("CREATE TABLE pes_methods(molecule string, method string, r string, E string, D DOUBLE, start DOUBLE, end DOUBLE, CONSTRAINT pes_method PRIMARY KEY (molecule, method))")
        self.close()
        
###################################################################################

    def connect(self):
        self.connection = sqlite3.connect(self.dbPath)
        self.cursor = self.connection.cursor()
    
###################################################################################

    def write(self, table, rows, questionMarks, values):
        self.cursor.execute("INSERT OR IGNORE INTO " + table + rows + " VALUES" + questionMarks, values)
        return True
                            
###################################################################################
                            
    def getData(self, table, columnNames, columnValue):
        self.cursor.execute("SELECT * from " + table + " WHERE " + " and ".join([ name + "= '" + str(columnValue[index]) + "'" for index, name in enumerate(columnNames)]))
        return self.cursor.fetchall()   
    
###################################################################################

    def writeDiatomicConstants(self, dc):
        self.connect()
        self.write("diatomic_constants", "(molecule,state,T,w,wx,wy,wz,B,a,y,D,re,u)", "(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (dc["name"], dc["state"], dc["T"], dc["w"], dc["wx"], dc["wy"], dc["wz"], dc["B"], dc["a"], dc["y"], dc["D"], dc["re"], dc["u"]))                  
        self.close()
    
###################################################################################

    def getDiatomicConstants(self, moleculeName):
        self.connect()
        data = self.getData("diatomic_constants", ["molecule"], [moleculeName])
        if(data == []):
            print("Diatomic constants for " + moleculeName + " not found in the database.")
            return False
        else: 
            data = data[0]
            return buildDiatomicConstants(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12])
        self.close()
    
###################################################################################

    def close(self):
        self.cursor = None
        self.connection.commit()
        self.connection.close()
        self.connection = None
        
###################################################################################

    #Data Helper Methods are defined here
    #Only 1D array
    def flatArrayToDB(self, array):
        return self.flatArrayToDBSep.join([str(val) for val in array])
    
###################################################################################

    #Any size multidimensonal array
    def arrayToDB(self, array):
        return self.arrayToDBSep.join( [self.flatArrayToDB(flatArray) for flatArray in array] )
    
###################################################################################

    def dbToFlatArray(self, dbStr):
        return np.array(list(map(float, dbStr.split(self.flatArrayToDBSep))))
    
###################################################################################

    def dbToArray(self, dbStr):
        return np.array( [ self.dbToFlatArray(dbStr2) for dbStr2 in dbStr.split(self.arrayToDBSep) ] )