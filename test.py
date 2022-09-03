from calcFunctions import *
from countryClasses import *
import locale
locale.setlocale(locale.LC_ALL, '')

inflation_df = pd.read_csv ('inflation_data.csv')
population_df = pd.read_csv('population_data.csv')
total_world_pop_df = pd.read_csv('world_population_by_year.csv')


testYears = createYearsList(1961, 2021, 5)



# inflation_data = inflationByCountryByYear(inflation_df, testYears, 20 )

# inflation_data = inflationByCountryByYear(inflation_df, testYears, 20 )
# print(populationByCountryByYear(population_df, inflation_data, testYears))


print(averageInflationByCountryByYearRange(inflation_df, testYears))

# print(createYearRangeDictWithEmptyArrays(testYears))