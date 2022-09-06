from calcFunctions import *
from countryClasses import *
import locale
locale.setlocale(locale.LC_ALL, '')

# inflation_df = pd.read_csv ('inflation_data.csv')
population_df = pd.read_csv('population_data.csv')
total_world_pop_df = pd.read_csv('world_population_by_year.csv')
headline_inflation_df = pd.read_csv('headline_inflation.csv')
bis_inflation_df = pd.read_csv('bis_inflation_data.csv')

targetYears = createYearsList(1961, 2021, 1)

# inflationDict = averageInflationByCountryByYearRange(inflation_df, targetYears)
inflationDict = inflationByCountryByYearTwoSources(headline_inflation_df, bis_inflation_df, targetYears, "20")
populationDict = averagePopulationByCountryByYearYange(population_df, inflationDict, targetYears)
worldPopDict = generateWorldPopulationData(total_world_pop_df, targetYears)




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


filteredDataByInflationRate = outputDataByYear(targetYears, inflationDict, populationDict)


countriesList = []

for year in filteredDataByInflationRate:
        for country in filteredDataByInflationRate[year]:
            countriesList.append(country.name)
           
countriesList = list(set(countriesList))


def buildCountryDict(countryList):
    countryDict = {}

    for x in countryList:
        countryDict[x] = 0
    return countryDict


peakPopByCountry = buildCountryDict(countriesList)
peakYearDict = {}
for country, pop in peakPopByCountry.items():
    for year in filteredDataByInflationRate:
        for x in filteredDataByInflationRate[year]:
            if x.name == country:
                    if x.population > pop:
                        peakPopByCountry[country] = x.population
                        peakYearDict[country] = year


totalPop = 0
for country, pop in peakPopByCountry.items():
    totalPop += pop


# print(filteredDataByInflationRate)
# print(peakPopByCountry)

# print(totalPop)
popualtionInPercent = (totalPop/ 7900000000) * 100


# with open('results_new.txt', 'w') as f:

#         for year in filteredDataByInflationRate:
#             f.write("\n")
#             for country in filteredDataByInflationRate[year]:
#                 f.write(f"\n{year}")
#                 f.write(f"\n{country.name} \n Inflation Rate: {country.avgInflationRate} \n Population: {country.population:n}\n ")
#         f.write(f"{popualtionInPercent}% of the world's population have experienced inflation over 20% since 1961")


# index_list = []
# for k, v in filteredDataByInflationRate.items():
#     index_list.append(k)


dfDictData = {}
for year, countries in filteredDataByInflationRate.items():
    countryNameList, countryInflationRateList, countryPopulationList = [], [], []
    for country in countries:
        countryNameList.append(country.name)
        countryInflationRateList.append(country.inflationRate)
        countryPopulationList.append(country.population)
    
    combinedCountryAttributesList = []
    combinedCountryAttributesList.append(countryNameList)
    combinedCountryAttributesList.append(countryInflationRateList)
    combinedCountryAttributesList.append(countryPopulationList)

    dfDictData[year] = combinedCountryAttributesList


listOfDf = []
finalDf = None

for year, columnsData in dfDictData.items():
    df = pd.DataFrame(columnsData).T
    df.columns = ["country", "inflationRate", "population"]
    df["year"] = year

    listOfDf.append(df)


final = pd.concat(listOfDf)

final.set_index(["year", "country"], inplace=True)
print(final)


