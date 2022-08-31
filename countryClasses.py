
from cgi import test


class Country:
        
    def setCountryName(self, name):
        self.name = name

    def setAvgInflationRate(self, rate):
        self.avgInflationRate = rate
    
    def setAvgPopulation(self, num):
        self.avgPopulation = num

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
