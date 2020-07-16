from PfsFile import PfsFile
import filecmp

""" 
This will load (parse) and then write back each of the given PFS files, and then compare the resulting files.
"""

import os
print(os.getcwd())

testFiles=[
    #"./tests/MSHE_main.she",           # MSHE main file
    "./tests/MSHE_main-repeat.she",     # MSHE main file with 2 repeated sections
    #"./tests/MSHE_UzSoilProp.uzs",     # MSHE UZ property file
    #"./tests/MSHE_Wells.wel",          # MSHE Well file
    #"./tests/MSHE_waterbalance.wbl",   # MSHE water balance file
    #"./tests/MSHE_ETVegProp.ETV",      # MSHE ETV file
]

for fileName in testFiles:
    setup = PfsFile(fileName)
    #print(setup[["[MIKESHE_FLOWMODEL]","[Climate]","[InfiltrationFraction]"]])
    #print(setup[["[MIKESHE_FLOWMODEL]","[ViewSettings]",1,'DefaultZoomDataArea_Y0']])
    #setup[["[MIKESHE_FLOWMODEL]","[Climate]","[InfiltrationFraction]","ShowShapeData"]]=5
    #print(setup[["[MIKESHE_FLOWMODEL]","[Climate]","[InfiltrationFraction]","ShowShapeData"]])
    #print(setup[["[MIKESHE_FLOWMODEL]","[Climate]","[InfiltrationFraction]"]])
    #setup.saveTo(fileName+".tmp")
    #print("{}: \t{}".format(filecmp.cmp(fileName, fileName+".tmp", shallow=False), fileName))
