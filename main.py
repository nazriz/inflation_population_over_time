import pandas as pd


df = pd.read_csv ('inflation_data.csv')



# country_grp = df.groupby(["Country"])

    
# print(country_grp.get_group("Australia").filter(items=["1974", "1975", "1976"]))

# df.set_index('Country', inplace=True, drop=True)

# print(df.loc[df["Country"] == "Australia", "1964", "1965"])


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


            
# print(df.loc[13, ["1971", "1972", "1973", "1974", "1975"]].mean())


targetColumns = createYearsList(1961, 2021, 5)

stepYearDict = {}

# Initilise stepYearDict with empty arrays
for years in targetColumns:
        stepYearDictName = str(years[0]) +"-"+str(years[-1])
        stepYearDict[stepYearDictName] = []

for x in range(len(df.index)):
    for y in targetColumns:
        stepYearDictKey = str(y[0]) +"-"+str(y[-1])
        stepYearAvg = df.loc[x, y].mean()
        if stepYearAvg > 30:
            countryDict = {}
            countryName = df._get_value(x,"Country")
            countryDict[countryName] = float(stepYearAvg)
            stepYearDict[stepYearDictKey].append(countryDict)
            # stepYearsWithCountry = y.copy()
            # stepYearsWithCountry.insert(0, "Country")
            # print(df.loc[x, stepYearsWithCountry])
            # print(f"Average inflation: {stepYearAvg}")
            # print(stepYearAvg)
            # print(countryName)


print(stepYearDict)

    



    


