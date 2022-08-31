from functools import total_ordering
from operator import truediv
from re import X
from tabnanny import check
import pandas as pd


inflation_df = pd.read_csv ('inflation_data.csv')
population_df = pd.read_csv('population_data.csv')
total_world_pop_df = pd.read_csv('world_population_by_year.csv')




# country_grp = df.groupby(["Country"])

    
# print(country_grp.get_group("Australia").filter(items=["1974", "1975", "1976"]))

# df.set_index('Country', inplace=True, drop=True)

# print(df.loc[df["Country"] == "Australia", "1964", "1965"])



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


targetColumns = createYearsList(1961, 2021, 5)

averageInflationDict = {}

# Initilise stepYearDict with empty arrays
for years in targetColumns:
        stepYearDictName = str(years[0]) +"-"+str(years[-1])
        averageInflationDict[stepYearDictName] = []

## Find inflation rates based on input 
for x in range(len(inflation_df.index)):
    for y in targetColumns:
        avgInflationDictKey = str(y[0]) +"-"+str(y[-1])
        stepYearAvg = inflation_df.loc[x, y].mean()
        if stepYearAvg > 30:
            countryDict = {}
            countryName = inflation_df._get_value(x,"Country")
            countryDict[countryName] = float(stepYearAvg)
            averageInflationDict[avgInflationDictKey].append(countryDict)



# Initilise averagePopulationDict with empty arrays
averagePopulationDict = {}
for years in targetColumns:
        stepYearDictName = str(years[0]) +"-"+str(years[-1])
        averagePopulationDict[stepYearDictName] = []

## Find average population based on input
for x in range(len(population_df.index)):
    for y in targetColumns:
        stepYearDictKey = str(y[0]) +"-"+str(y[-1])
        stepYearAvg = population_df.loc[x, y].mean()
        countryName = population_df._get_value(x,"Country")
        if checkAverageInflationDictKeys(countryName, averageInflationDict[stepYearDictKey]):
            countryDict = {}
            countryDict[countryName] = float(stepYearAvg)
            averagePopulationDict[stepYearDictKey].append(countryDict)



worldPopulationDict = {}
for x in targetColumns:
    yearDictName = str(x[0]) +"-"+str(x[-1])
    worldPopulationDict[yearDictName] = total_world_pop_df[x].mean(axis=1).astype(int).values[0]
   
