import random
import numpy
import math
import Behaviour

class Actor:
    def __init__(self, ID , market, resource, minAmount, maxAmount, underSell, overSell, currency = False):
        self.currency = currency
        self.ID = ID
        self.market = market
        self.resource = resource
        self.behaviour = Behaviour.Behaviour(self.market, self.resource)
        
        self.minAmount = minAmount
        self.maxAmount = maxAmount
        self.underSell = underSell
        self.overSell = overSell

        self.amountOfUniqueResources = resource.amountOfUniqueResources

        self.RandomizeBehavior()

    def RandomizeBehavior(self):
        if self.currency:
            self.myBehaviour = Behaviour.BasicCurrencyBehaviour(0, 1, -0.2, 0.2, self.resource, self.ID, self.market)
        else:
            self.myBehaviour = Behaviour.BasicUniform(self.minAmount, self.maxAmount, self.underSell, self.overSell, self.resource, self.ID, self.market)
        #
        
        #Behavior depends on: Market price of resource, amount of resources, productivity, consumption

    def Sell(self):
        thingsToSell = self.myBehaviour.PostResources()
        #print("Things to sell", thingsToSell)
        #Will in basic uniform behaviour go out of bounds

        for product in range(len(thingsToSell)):
            
            wanted_resources = thingsToSell[product][0]
            posted_amount = thingsToSell[product][1]
            posted_price = thingsToSell[product][2]
            
            for resource in range(len(wanted_resources)):
                postedResource = product
                wantedResource = int(wanted_resources[resource])
                postedAmount = posted_amount[resource]
                wantedAmount = posted_price[resource]      
                if wantedAmount < 0:
                    print("Hello")
                if postedAmount < 0:
                    print("Yahoi")
                #print("I'm actor ", self.ID, "I Will Sell ", postedResource, "For ", wantedResource, "I have ", postedAmount, "I want ", wantedAmount)
                self.market.PostResource(postedResource, wantedResource, postedAmount, wantedAmount, self.ID)
                    
                    