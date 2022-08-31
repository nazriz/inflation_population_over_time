from calcFunctions import *
from countryClasses import *

inflation_df = pd.read_csv ('inflation_data.csv')
population_df = pd.read_csv('population_data.csv')
total_world_pop_df = pd.read_csv('world_population_by_year.csv')


targetYears = createYearsList(1961, 2021, 5)

inflationDict = averageInflationByCountryByYearRange(inflation_df, targetYears)
populationDict = averagePopulationByCountryByYearYange(population_df, inflationDict, targetYears)
totalPopDict = generateWorldPopulationData(total_world_pop_df, targetYears)
