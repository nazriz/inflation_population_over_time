from functools import total_ordering
from operator import truediv
from pickle import EMPTY_DICT
from queue import Empty
from re import X
from tabnanny import check
import pandas as pd


def createYearRangeDictWithEmptyArrays(yearsRange):
    emptyDict = {}
    for years in yearsRange:
        if len(years) == 1:
            stepYearDictName = str(years[0])
            emptyDict[stepYearDictName] = []
        else:
            stepYearDictName = str(years[0]) +"-"+str(years[-1])
            emptyDict[stepYearDictName] = []

    return emptyDict


def checkAverageInflationDictKeys(targetCountry, inputList):
    for x in range(len(inputList)):
        if targetCountry in inputList[x]:
                return True
    
    return False


def createYearsList(startYear, endYear, step):

    listOfYearsByStep = []

    yearsToGenerate = endYear - startYear

    tempList = []
    tempList.append(str(startYear))
    year = startYear
    stepCounter = 0

    for x in range(yearsToGenerate):
        year += 1
        if stepCounter < step - 1:
            tempList.append(str(year))
            stepCounter += 1
        else:
            stepCounter = 0
            listOfYearsByStep.append(tempList)
            tempList = []
            tempList.append(str(year))

    listOfYearsByStep.append(tempList)
    return listOfYearsByStep


def averageInflationByCountryByYearRange(inputDf, yearsRangeList):
    # Initilise stepYearDict with empty arrays
    averageInflationDict = createYearRangeDictWithEmptyArrays(yearsRangeList)

    ## Find inflation rates based on input 
    for x in range(len(inputDf.index)):
        for y in yearsRangeList:
            if len(y) != 1:
                avgInflationDictKey = str(y[0]) +"-"+str(y[-1])
            else:
                avgInflationDictKey = str(y[0])
            stepYearAvg = inputDf.loc[x, y].mean()
            if stepYearAvg > 30:
                countryDict = {}
                countryName = inputDf._get_value(x,"Country")
                countryDict[countryName] = str(round(float(stepYearAvg),2)) + " %"
                averageInflationDict[avgInflationDictKey].append(countryDict)
    return averageInflationDict



def averagePopulationByCountryByYearYange(inputDf, inflationDict, yearsRangeList):

    # Initilise averagePopulationDict with empty arrays
    averagePopulationDict = createYearRangeDictWithEmptyArrays(yearsRangeList)

    ## Find average population based on input
    for x in range(len(inputDf.index)):
        for y in yearsRangeList:
            if len(y) != 1:
                stepYearDictKey = str(y[0]) +"-"+str(y[-1])
            else:
                stepYearDictKey = str(y[0])
            stepYearAvg = inputDf.loc[x, y].mean()
            countryName = inputDf._get_value(x,"Country")
            if checkAverageInflationDictKeys(countryName, inflationDict[stepYearDictKey]):
                countryDict = {}
                countryDict[countryName] = int(stepYearAvg)
                averagePopulationDict[stepYearDictKey].append(countryDict)

    return averagePopulationDict


def generateWorldPopulationData(inputDf, yearsRangeList):

    worldPopulationDict = {}
    for x in yearsRangeList:
        if len(x) != 1:
            yearDictName = str(x[0]) +"-"+str(x[-1])
        else:
            yearDictName = str(x[0])

        worldPopulationDict[yearDictName] = inputDf[x].mean(axis=1).astype(int).values[0]

    return worldPopulationDict
   


def inflationByCountryByYear(inputDf, yearsRangeList, targetInflationRate):
    # Initilise stepYearDict with empty arrays
    inflationByYearDict = createYearRangeDictWithEmptyArrays(yearsRangeList)

    ## Find inflation rates based on input 
    for x in range(len(inputDf.index)):
        for y in yearsRangeList:
            avgInflationDictKey = str(y[0])
            inflationRate = float(inputDf.loc[x, y])
            if inflationRate > targetInflationRate:
                countryDict = {}
                countryName = inputDf._get_value(x,"Country")
                countryDict[countryName] = str(round(float(inflationRate),2)) + " %"
                inflationByYearDict[avgInflationDictKey].append(countryDict)

    return inflationByYearDict

def populationByCountryByYear(inputDf, inflationDict, yearsRangeList):

    # Initilise averagePopulationDict with empty arrays
    countryPopulationDict = createYearRangeDictWithEmptyArrays(yearsRangeList)

    ## Find average population based on input
    for x in range(len(inputDf.index)):
        for y in yearsRangeList:
            countryPopDictKey = str(y[0])
            populationForYear = float(inputDf.loc[x, y])
            countryName = inputDf._get_value(x,"Country")
            if checkAverageInflationDictKeys(countryName, inflationDict[countryPopDictKey]):
                countryDict = {}
                countryDict[countryName] = int(populationForYear)
                countryPopulationDict[countryPopDictKey].append(countryDict)

    return countryPopulationDict
