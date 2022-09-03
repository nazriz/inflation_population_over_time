from calcFunctions import *
from countryClasses import *
import locale
locale.setlocale(locale.LC_ALL, '')

inflation_df = pd.read_csv ('inflation_data.csv')
population_df = pd.read_csv('population_data.csv')
total_world_pop_df = pd.read_csv('world_population_by_year.csv')


targetYears = createYearsList(1961, 2021, 1)

inflationDict = averageInflationByCountryByYearRange(inflation_df, targetYears)
populationDict = averagePopulationByCountryByYearYange(population_df, inflationDict, targetYears)
worldPopDict = generateWorldPopulationData(total_world_pop_df, targetYears)



def outputDataByAverage(yearRange, inflationData, populationData, worldPopulationData):
    countryObjects = createYearRangeDictWithEmptyArrays(yearRange)


    for year in countryObjects:
        for countryInflation in inflationData[year]:
            countryName = str(list(countryInflation.keys())[0])
            countryObj = Country()
            countryObj.setCountryName(countryName)
            countryObj.setAvgInflationRate(countryInflation[countryName])
            countryObjects[year].append(countryObj)
                

        for countryPopulation in populationData[year]:
            countryName = str(list(countryPopulation.keys())[0])
            avgPopulation = countryPopulation[countryName]
            for country in countryObjects[year]:
                if countryName == country.name:
                    country.setAvgPopulation(avgPopulation)


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
                yearRangePopTotal += countryObjects[yearRange][country].avgPopulation
                f.write(f"\n{countryObjects[yearRange][country].name} \n Inflation Rate: {countryObjects[yearRange][country].avgInflationRate} \n Population: {countryObjects[yearRange][country].avgPopulation:n}\n ")

            worldPop = countryObjects[yearRange][-1].amount
            percentageOfWorldPop = str(round((yearRangePopTotal / worldPop) * 100,2)) + " %"
            f.write(f"\n Between {yearRange}, {percentageOfWorldPop} of the world's population ({yearRangePopTotal:n} people) \n subjected to inflation rates greater than {targetInflationRate}. ")

    return countryObjects



def outputDataByYear(yearRange, inflationData, populationData, worldPopulationData):
    countryObjects = createYearRangeDictWithEmptyArrays(yearRange)


    for year in countryObjects:
        for countryInflation in inflationData[year]:
            countryName = str(list(countryInflation.keys())[0])
            countryObj = Country()
            countryObj.setCountryName(countryName)
            countryObj.setAvgInflationRate(countryInflation[countryName])
            countryObjects[year].append(countryObj)
                

        for countryPopulation in populationData[year]:
            countryName = str(list(countryPopulation.keys())[0])
            avgPopulation = countryPopulation[countryName]
            for country in countryObjects[year]:
                if countryName == country.name:
                    country.setAvgPopulation(avgPopulation)


        # worldPopObj = worldPopulation()
        # worldPopObj.setWorldPopulation(worldPopulationData[year])
        # countryObjects[year].append(worldPopObj)

    return countryObjects

testObj = outputDataByYear(targetYears, inflationDict, populationDict, worldPopDict)


countriesList = []

for year in testObj:
        for country in testObj[year]:
            countriesList.append(country.name)
           
countriesList = list(set(countriesList))


def buildCountryDict(countryList):
    countryDict = {}

    for x in countryList:
        countryDict[x] = 0
    return countryDict


countryPopDict = buildCountryDict(countriesList)

for country, pop in countryPopDict.items():
    for year in testObj:
        for x in testObj[year]:
            if x.name == country:
                if x.avgPopulation > pop:
                    countryPopDict[country] = x.avgPopulation

print(countryPopDict)

totalPop = 0
for country, pop in countryPopDict.items():
    totalPop += pop

print(testObj)
print(totalPop)
