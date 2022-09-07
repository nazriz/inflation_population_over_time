class Country:
        
    def setCountryName(self, name):
        self.name = name

    def setInflationRate(self, rate):
        self.inflationRate = rate
    
    def setPopulation(self, num):
        self.population = num

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name



class worldPopulation:

    def setWorldPopulation(self, amount):
        self.amount = amount


    def __str__(self):
        return "WorldPopulation"

    def __repr__(self):
        return "WorldPopulation"


class highestPopulation:

    def buildCountryDict(self, countryList):
        self.countryDict = {}

        for x in countryList:
            self.countryDict[x] = 0