from cgi import test
from turtle import xcor
from calcFunctions import *
from countryClasses import *
import locale
locale.setlocale(locale.LC_ALL, '')

old_inflation_df = pd.read_csv ('old_inflation_data.csv')
population_df = pd.read_csv('population_data.csv')
total_world_pop_df = pd.read_csv('world_population_by_year.csv')
headline_inflation_df = pd.read_csv('headline_inflation.csv')
bis_inflation_df = pd.read_csv('bis_inflation_data.csv')

bis_inflation_df.set_index("Country", inplace=True)
headline_inflation_df.set_index("Country", inplace=True)

testYears = createYearsList(1955, 1970, 1)
countriesList = list(headline_inflation_df.index)



def inflationByCountryByYearTwoSources(inputDfone, inputDfTwo, yearsRangeList, targetInflationRate):
    # Initilise stepYearDict with empty arrays
    inflationByYearDict = createYearRangeDictWithEmptyArrays(yearsRangeList)
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



testTwoSources = inflationByCountryByYearTwoSources(headline_inflation_df, bis_inflation_df, testYears, 20)

print(testTwoSources)


# def getInflationRate(inputDf, country, year):

#     return float(inputDf.loc[country, year])

# testOutput = inflationByCountryByYearTest(headline_inflation_df,bis_inflation_df, testYears, 20)

# for x in testOutput:
#     print(x)
#     print(testOutput[x])
