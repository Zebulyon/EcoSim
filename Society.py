#!/usr/bin/python3
import random
import numpy
import Market
from Resource import Resource
from Actor import Actor
from Behaviour import Behaviour
import sys

class Society:
    def __init__(self, currency, actorNumber, resource, min_init_amountToSell, max_init_amountToSell, min_init_priceDivergence, max_init_priceDivergence, trade, converging_value):
        #Setting base values
        self.currency = currency
        self.actorNumber = actorNumber
        self.resource = resource
        self.trade = trade
        #If there is no productivity convergence then this should be -1
        self.converging_value = converging_value

        self.min_init_amountToSell = min_init_amountToSell
        self.max_init_amountToSell = max_init_amountToSell

        self.min_init_priceDivergence = min_init_priceDivergence
        self.max_init_priceDivergence = max_init_priceDivergence

        #Start initaion of enviroment
        self.dayNum = 0
        if currency == True:
            self.market = Market.NiceCurrencyMarket(self.resource.amountOfUniqueResources, self.resource, self.resource.GetCurrency())
        else:
            self.market = Market.NiceMarket(self.resource.amountOfUniqueResources, self.resource)
        self.CreateActors(self.actorNumber)

    def CreateActors(self, actorNumber):
        self.actorList = numpy.zeros(0, dtype=Actor)
        for name in range(0, actorNumber):
            #Actor obj takes name, 
            self.actorList = numpy.append(self.actorList, [Actor(name, self.market, self.resource, self.min_init_amountToSell, self.max_init_amountToSell, self.min_init_priceDivergence, self.max_init_priceDivergence, self.currency)])

    def Update(self, days_to_run):
        for _ in range(days_to_run):
            self.RunDay()
        print("Final amount of resources", self.resource.GetTotalResources())

    def RunDay(self):
        #print("Day " + str(self.dayNum))
        #print("Current amount of resources", self.resource.GetTotalResources())
        self.dayNum += 1
        if self.converging_value < 0:
            self.resource.Produce()
        else:
            self.resource.ProduceConverging(self.converging_value)
        if self.trade:
            for actor in self.actorList:
                actor.Sell()
            self.market.MatchTrades()
            print("Sales day", self.dayNum, ":", self.market.sales_in_day)

def main():
    currency = False
    trade = False
    #Should be -1 if no converging value should be used
    converging_value = 10**5

    amountOfActors = 10000
    amountOfResources = 20
    min_init_resources = 0
    max_init_resources = 50
    min_init_production = -0.2
    max_init_production = 0.2
    resource = Resource(min_init_resources, max_init_resources, min_init_production, max_init_production, amountOfResources, amountOfActors, currency)

    min_init_amountToSell = 0
    max_init_amountToSell = 1
    min_inti_priceDivergence = -0.2
    max_inti_priceDivergence = 0.2
    society = Society(currency, amountOfActors, resource, min_init_amountToSell, max_init_amountToSell, min_inti_priceDivergence, max_inti_priceDivergence, trade, converging_value)
    society.Update(30)

#def script_main(currency, trade, converging_value, amountOfActors, amountOfResources, min_init_resources, max_init_resources, min_init_production, max_init_production, min_init_amountToSell, max_init_amountToSell, min_inti_priceDivergence, max_inti_priceDivergence, days):
def script_main(argv):
    if(len(argv) != 15):
        exit(-1)
    currency = bool(int(argv[1]))
    trade = bool(int(argv[2]))
    #Should be -1 if no converging value should be used
    converging_value = float(argv[3])

    amountOfActors = int(argv[4])
    amountOfResources = int(argv[5])
    min_init_resources = float(argv[6])
    max_init_resources = float(argv[7])
    min_init_production = float(argv[8])
    max_init_production = float(argv[9])

    min_init_amountToSell = float(argv[10])
    max_init_amountToSell = float(argv[11])
    min_inti_priceDivergence = float(argv[12])
    max_inti_priceDivergence = float(argv[13])
    days = int(argv[14])
    
    resource = Resource(min_init_resources, max_init_resources, min_init_production, max_init_production, amountOfResources, amountOfActors, currency)
    society = Society(currency, amountOfActors, resource, min_init_amountToSell, max_init_amountToSell, min_inti_priceDivergence, max_inti_priceDivergence, trade, converging_value)
    society.Update(days)

script_main(sys.argv)