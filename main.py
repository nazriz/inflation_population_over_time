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



filteredDataByInflationRate = outputDataByYear(targetYears, inflationDict, populationDict)

## Prepares data into concatenated dataframe, for export to CSV.
# all data present in this output is what has met the specified threshold
# i.e. If searching for countries with inflation rate over 20%,
# this output will return EVERY instance of a country with an inflation
# rate over 20% between the targeted years.

def outputAllTargetData():
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

    for year, columnsData in dfDictData.items():
        df = pd.DataFrame(columnsData).T
        df.columns = ["country", "inflationRate", "population"]
        df["year"] = year

        listOfDf.append(df)


    final = pd.concat(listOfDf)

    final.set_index(["year", "country"], inplace=True)


    final.to_csv("output_whole_data.csv")



def outputCalculationTargetData():

    countriesList = []

    for year in filteredDataByInflationRate:
            for country in filteredDataByInflationRate[year]:
                countriesList.append(country.name)
            
    countriesList = list(set(countriesList))

    def buildCountryDict(countryList):
        countryDict = {}

        for x in countryList:
            countryDict[x] = []
        return countryDict

    peakPopByCountry = buildCountryDict(countriesList)
    for country, pop in peakPopByCountry.items():
        for year in filteredDataByInflationRate:
            for x in filteredDataByInflationRate[year]:
                if x.name == country:
                    try:
                        if x.population > pop[2]:
                            peakPopByCountry[country][0] = year
                            peakPopByCountry[country][1] = x.inflationRate
                            peakPopByCountry[country][2] = x.population
                    except:
                            peakPopByCountry[country].append(year)
                            peakPopByCountry[country].append(x.inflationRate)
                            peakPopByCountry[country].append( x.population)


    listOfDf = []
    for country, columnsData in peakPopByCountry.items():
            df = pd.DataFrame(columnsData).T
            df.columns = ["year", "inflationRate", "population"]
            df["country"] = country

            listOfDf.append(df)


    final = pd.concat(listOfDf)
    final.set_index(["country"], inplace=True)

    final.to_csv("output_calculation_data.csv")




outputCalculationTargetData()

