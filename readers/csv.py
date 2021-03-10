from os import path, name
import csv

def getAnimalList(dataFile):
    directory = path.dirname(path.dirname(__file__))
    pathToFile = path.join(directory, "data", dataFile)
    
    animalList = []

    with open(pathToFile, newline='') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=';', quotechar='|')
        for row in csvReader:
            animalList.append(row)

    return animalList
    
