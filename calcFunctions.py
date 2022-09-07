import pandas as pd
from countryClasses import *



def createYearRangeDictWithEmptyArrays(yearsRange):
    '''
    Builds a dictionary with empty lists, for use with
    proceeding functions. The yearsRange input must be 
    created using createYearsList function (or equivalent)
    '''
    emptyDict = {}
    for years in yearsRange:
        if len(years) == 1:
            stepYearDictName = str(years[0])
            emptyDict[stepYearDictName] = []
        else:
            stepYearDictName = str(years[0]) +"-"+str(years[-1])
            emptyDict[stepYearDictName] = []

    return emptyDict


def createYearsList(startYear, endYear, step):
    '''
    Create's a list of years based on specified startYear
    and endYear. The step argument dictates the amount of
    years between an interval, e.g. 1961 - 1965, is produced
    from a step input of 5. For a single year list, specify
    step of 1.
    '''
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


def checkAverageInflationDictKeys(targetCountry, inputList):
    for x in range(len(inputList)):
        if targetCountry in inputList[x]:
                return True
    
    return False


def averageInflationByCountryByYearRange(inputDf, yearsRangeList, targetInflationRate):
    '''
    Outputs a calculation of the average inflation rate, by
    country and year based on the inputted dataframe, and the 
    year steps defined in the yearsRangeList input, created 
    from createYearsList function. 
    '''

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
            if stepYearAvg > int(targetInflationRate):
                countryDict = {}
                countryName = inputDf._get_value(x,"Country")
                countryDict[countryName] = str(round(float(stepYearAvg),2)) + " %"
                averageInflationDict[avgInflationDictKey].append(countryDict)
    return averageInflationDict



def averagePopulationByCountryByYearYange(inputDf, inflationDict, yearsRangeList):
    '''
    Using the output from averageInflationByCountryByYearRange function (to inflationDict),
    the average population is calculated for the specified time period as defined in the 
    yearsRangeList. The same yearsRangeList input should be used between both averageInflation
    function and averagePopulation function.
    '''
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
    '''
    Returns a dict with years as key, and world population for
    that specified year as the value
    '''

    worldPopulationDict = {}
    for x in yearsRangeList:
        if len(x) != 1:
            yearDictName = str(x[0]) +"-"+str(x[-1])
        else:
            yearDictName = str(x[0])

        worldPopulationDict[yearDictName] = inputDf[x].mean(axis=1).astype(int).values[0]

    return worldPopulationDict
   


def inflationByCountryByYear(inputDf, yearsRangeList, targetInflationRate):
    '''
    Returns a dictionary that contains year as key, and a list of dicts that
    contain country : inflation rate for that year, as the value. Countries are
    only included if their inflation rate for that year equals or exceeds
    the targetInflationRate input. inputDf should be a df built from inflation
    data. yearsRangeList can be created from createYearsList function or
    equivalent.
    '''
    # Initilise stepYearDict with empty arrays
    inflationByYearDict = createYearRangeDictWithEmptyArrays(yearsRangeList)

    ## Find inflation rates based on input 
    for x in range(len(inputDf.index)):
        for y in yearsRangeList:
            avgInflationDictKey = str(y[0])
            inflationRate = float(inputDf.loc[x, y])
            if inflationRate >= targetInflationRate:
                countryDict = {}
                countryName = inputDf._get_value(x,"Country")
                countryDict[countryName] = str(round(float(inflationRate),2)) + " %"
                inflationByYearDict[avgInflationDictKey].append(countryDict)

    return inflationByYearDict

def populationByCountryByYear(inputDf, inflationDict, yearsRangeList):
    '''
    Returns a dictionary that contains year as key, and a list of dicts that
    contain country : population for that year, as the value. Countries are
    only included if they are present in the inflactionDict input. inputDf 
    should be a df built from population data. yearsRangeList can be 
    created from createYearsList function or equivalent.
    '''

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

def inflationByCountryByYearTwoSources(inputDfone, inputDfTwo, yearsRangeList, targetInflationRate):
    '''
    Returns a dictionary that contains a year as a key, and a list of dicts
    
    '''
    # Initilise stepYearDict with empty arrays
    inflationByYearDict = createYearRangeDictWithEmptyArrays(yearsRangeList)
    #Set index of both DF's to be country
    inputDfone.set_index("Country", inplace=True)
    inputDfTwo.set_index("Country", inplace=True)

    # build a list of countries based on the longest list available
    # which is assumed to be inputDfone
    countriesList = list(inputDfone.index)

    ## Find inflation rates based on input 
    for country in countriesList:
        for y in yearsRangeList:
            avgInflationDictKey = str(y[0])
            inflationRate = 0
            try:
                inflationRate = float(inputDfone.loc[country, y])
            except:
                if country in inputDfTwo.index:
                    inflationRate = float(inputDfTwo.loc[country, y])
                else:
                    # 0 indicating value not present, and will therefore
                    # not be included in the final dataframe.
                    inflationRate = 0
            if inflationRate > targetInflationRate:
                countryDict = {}
                countryDict[country] = str(round(float(inflationRate),2)) + " %"
                inflationByYearDict[avgInflationDictKey].append(countryDict)

    return inflationByYearDict



def outputDataByAverage(yearRange, inflationData, populationData, worldPopulationData):
    countryObjects = createYearRangeDictWithEmptyArrays(yearRange)

    for year in countryObjects:
        for countryInflation in inflationData[year]:
            countryName = str(list(countryInflation.keys())[0])
            countryObj = Country()
            countryObj.setCountryName(countryName)
            countryObj.setInflationRate(countryInflation[countryName])
            countryObjects[year].append(countryObj)
                

        for countryPopulation in populationData[year]:
            countryName = str(list(countryPopulation.keys())[0])
            population = countryPopulation[countryName]
            for country in countryObjects[year]:
                if countryName == country.name:
                    country.setPopulation(population)


        worldPopObj = worldPopulation()
        worldPopObj.setWorldPopulation(worldPopulationData[year])
        countryObjects[year].append(worldPopObj)



    ## Write to file
    targetInflationRate = "30%"
    targetYearPeriod = "5"

    ## Output data

    with open('results.txt', 'w') as f:

        for yearRange in countryObjects:
            f.write("\n ==========================================")
            f.write(f"\n{yearRange} World Population: {countryObjects[yearRange][-1].amount:n}")
            yearRangePopTotal = 0
            for country in range(len(countryObjects[yearRange]) - 1):
                yearRangePopTotal += countryObjects[yearRange][country].population
                f.write(f"\n{countryObjects[yearRange][country].name} \n Inflation Rate: {countryObjects[yearRange][country].inflationRate} \n Population: {countryObjects[yearRange][country].population:n}\n ")

            worldPop = countryObjects[yearRange][-1].amount
            percentageOfWorldPop = str(round((yearRangePopTotal / worldPop) * 100,2)) + " %"
            f.write(f"\n Between {yearRange}, {percentageOfWorldPop} of the world's population ({yearRangePopTotal:n} people) \n subjected to inflation rates greater than {targetInflationRate}. ")

    return countryObjects




def outputDataByYear(yearRange, inflationData, populationData):

    countryObjects = createYearRangeDictWithEmptyArrays(yearRange)


    for year in countryObjects:
        for countryInflation in inflationData[year]:
            countryName = str(list(countryInflation.keys())[0])
            countryObj = Country()
            countryObj.setCountryName(countryName)
            countryObj.setInflationRate(countryInflation[countryName])
            countryObjects[year].append(countryObj)
                

        for countryPopulation in populationData[year]:
            countryName = str(list(countryPopulation.keys())[0])
            population = countryPopulation[countryName]
            for country in countryObjects[year]:
                if countryName == country.name:
                    country.setPopulation(population)

    return countryObjects