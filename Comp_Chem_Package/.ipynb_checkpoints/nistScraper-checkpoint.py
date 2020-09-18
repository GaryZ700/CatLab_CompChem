#Written by Gary Zeri
#Computer Science Major at Chapman University, Member of Dr. LaRue's CatLab

#Code to scrape the NIST Webook for diatomic constants data

import requests
import re
from bs4 import BeautifulSoup as soup
from diatomicConstants import *

#Returns a diatomics constants object if the operation was sucessful
#Otherwise returns false
def getDiatomicConstants(diatomicIdentifier, state = "ground"):
    
    diatomicIdentifier = str(diatomicIdentifier)
    state = state.strip()
    
    #Translate text representation of greek letters in html code 
    #to actual unicode greek letters
    greekLetters = {
        "sigma":"\u03C3",
        "Sigma":"\u03A3",
        "csigma":"\u03A3",
        "pi":"\u03C0",
        "cpi":"\u03A0",
        "cdelta":"\u0394",
        "delta":"\u03b4",
        "phi":"\u03D5",
        "cphi":"\u03A6",
        "larrow":"",
        "lrarrow":"",
        "rarrow":"",
    }
    
    #Link for chemical formula, chemical name, and CAS Number
    searchUrls = ( ("https://webbook.nist.gov/cgi/cbook.cgi?Formula=", "&NoIon=on&Units=SI&cDI=on"), 
                   ("https://webbook.nist.gov/cgi/cbook.cgi?Name=","&Units=SI&cDI=on"), 
                   ("https://webbook.nist.gov/cgi/cbook.cgi?ID=","&Units=SI&cDI=on") 
                 )
    
    #search for teh diatomicIdentifier in all of the search urls
    for url in searchUrls: 

        nistData = soup(requests.get(url[0] + diatomicIdentifier.upper() + url[1]).text, "lxml")
    
        main = nistData.find("main", attrs = {"id":"main"})
        headerName = main.find("h1").text 
        fullRowsRaw = main.find_all("tr")[::-1]

        #check if the diatomicIdentifier was found in the url
        if(fullRowsRaw == []):
            if("ID" in url[0]):
                print('\nWarning!! Unable to locate the diatomic constants for "' + diatomicIdentifier + '".')
                return False
        else:
            break
    
   # old verification algorithem to check if data was found for the diatomic identifier 
   # if(headerName == "Search Results" or headerName == "Name Not Found"):
   #     print('\nWarning!! Unable to locate the diatomic constants for "' + diatomicSymbol + '".')
   #     return False

###################################################################################
    #Section to find the specifed diatomic state
    
    #iterate over all of the raw rows from NIST
    #to find the row with the specified state
    foundState = False
    for row in fullRowsRaw: 
        
        #Check if the row contains the appropriate subrow containing diatomic data
        dataRow = row.find("td", attrs={"class":"nowrap"})
        if(dataRow == None):
            continue
            
        #Parse the state from the row
        rowState = ""
        endingHrefNum = ""
        for stateComponents in dataRow.contents:
            stateComponents = str(stateComponents)
            
            #keep commas
            if(stateComponents != ","):
                
                #parse out a single state component
                for component in stateComponents.split(","):
                    
                    #check if component is alreadly parsed or is in an heml tag
                    if("<" in component):
                        #check if tag is an img, and convert img to text
                        if("img" in component):
                            rowState += greekLetters[ component.split(".")[0].split("/")[-1] ]
                        elif("href=" in component):
                            endingHrefNum = component.split("<")[1].split(">")[-1]
                        #assume <sub>/<sup> tag
                        else:
                            rowState += component.split("<")[1].split(">")[-1]                            
                    else:
                        rowState += component
            else:
                rowState += stateComponents
                
        #Remove extra starting and ending spaces from the rowState string
        rowStateWithHref = (rowState + endingHrefNum).strip()
        rowState = rowState.strip()
        
        #determine if the specified state was found
        if( (state.lower() == "ground" and "X" in rowState) or
             state == rowState or state == rowStateWithHref):                
    
            foundState = True
            break
    
###################################################################################    
    #State was found, proceed to parse out all the needed diatomic data for the state
    
    #if the correct state was found then begin the process of building the diatomics constants object
    #from the data on the nist site
    if(foundState):
        
        #remove the starting rows that do not contain useful data
        valueRows = row.find_all("td")[1:-2]
        
        if(len(valueRows) == 0):
            print("Warning! " + diatomicIdentifier + " " + state + " state missing diatomic constants on the NIST WebBook.")
            return
        
        values = []        
        #parse out any uneeded subscripts from the final value
        for value in valueRows:
            
            #remove first set of starting and ending brackets
            value = str(value).strip()[5:-5]

            #use regex to clean up the data
            value = re.sub("<.*?>.*?<.*?>|[^0-9.E\-]", "", value)
            1
            #determine if the data type has a valid value or if it should be none
            if(value == ""):
                values.append(None)
            else:
                values.append(float(value))

###################################################################################
        #Pull Mass data for the most common isotope from NIST to 
        #compute the reduced atomic mass for the diatomic molecule

        #Parse the atomic formula for the diatomic molecule
        moleculeName = main.find("ul").find("li").text.split(":")[1].strip()
        atoms = []
        for atomChar in moleculeName:
            
            #if is a character, decided if it is a new atom, or an older atom
            if(atomChar.isalpha()):
                if atomChar.islower():
                    atoms[-1] += atomChar
                else:
                    atoms.append(atomChar)
            #if is a number, then duplicate the first atom
            elif(atomChar.isnumeric()):
                atoms.append(atoms[-1])
            #else to ignore charge values
            else:
                break
        
        #get the individual masses of each of the atoms from NIST
        masses = []
        for atom in atoms: 
            data = soup(requests.get("https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=" + atom + "&ascii=ascii2&isotype=some").text, "lxml").find("pre")
            
            #create a list of lists containing the following data [string relative mass, string isotope percentage]
            parsedData = [ textBlock.split("\n")[3:5] for textBlock in data.text.strip().split("Atomic Number")[1:] ]
            
            #create the relative mass and isotopic percentage data lists
            #all even values are mass values, while odd values are isotope values
            isotopeMassData = []
            for data in parsedData:
                for innerData in data: 
                   
                    #try except to deal with cases where there is no value provided
                    try: 
                        isotopeMassData.append(float(innerData.split("=")[1].split("(")[0]))
                    except: 
                        isotopeMassData.append(0)
            
            #pull out the isotope and mass data from the combined isotope/mass data list
            isotopeData = isotopeMassData[1::2]
            massData = isotopeMassData[0::2]
        
            masses.append(massData[isotopeData.index(max(isotopeData))])
            
###################################################################################
        #webscraping has been completed 
        #returns a diatomicConstants object with all the parsed data

        return buildDiatomicConstants(name = moleculeName, state = state,           
                    T = values[0], w = values[1], wx = values[2], 
                    wy = 0 if values[3] == None else  values[3], 
                    wz = 0, B = values[4], a = values[5], 
                    y = 0 if values[6] == None else values[6], 
                    D = values[7], re = values[9], 
                    u = (masses[0] * masses[1]) / sum(masses) 
                   ) 
    else:
        print('Warning!! Could not find state "' + state + '"! ' +
              'Please check to ensure the state you specified exists for ' +
              diatomicIdentifier + ' on the NIST Webbook.'
             )