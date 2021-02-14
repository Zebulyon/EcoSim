
import numpy
import random

class Behaviour:
    def __init__(self, market, resource):
        self.market = market
        self.resource = resource

#Should seek behavior that buys things used for production and sells things not used for production
class ProductionSeekingBehavior(Behaviour):
    def __init__(self):
        print("Nothing")

class BasicUniform(Behaviour):

    def __init__(self, minAmount, maxAmount, underSell, overSell, resource, actor_ID, market):
        
        self.market = market
        self.actor_ID = actor_ID
        self.resource = resource
        self.inStorageList = resource.resourceArray[actor_ID][0]
        self.amountOfUniqueResources = self.resource.amountOfUniqueResources

        self.minAmount = minAmount
        self.maxAmount = maxAmount
        self.underSell = underSell
        self.overSell = overSell
        
        self.behaviourArray = numpy.zeros((self.amountOfUniqueResources, 3), dtype = list)
        self.InitilizeBehaviourArray()

    def PercentageToSell(self):
        # how large of a % it will sell of its resource
        percentage_to_sell = random.uniform(self.minAmount,self.maxAmount)
        return percentage_to_sell
    
    def DivergenceToSell(self):
        # % of how much it will deviate from the recorded market price of yesterday
        divergence_to_sell = random.uniform(self.underSell,self.overSell)  
        return divergence_to_sell

    def ResourceIwant(self, product):

        resource = product
        while resource == product:
            resource = random.randint(0, self.amountOfUniqueResources-1)
        return resource

    def InitilizeBehaviourArray(self):
        for product in range (self.amountOfUniqueResources):
            
            # First field is for the resource i sell my product for
            # Second field is the amount of my product I will sell
            # Third field is the price I will sell my product for in relation to the resource 
            self.behaviourArray[product][0] = [self.ResourceIwant(product)]
            self.behaviourArray[product][1] = [self.PercentageToSell()]
            self.behaviourArray[product][2] = [self.DivergenceToSell()]

    def PostResources(self):

        temp = numpy.zeros((self.amountOfUniqueResources,3), dtype = list)

        for product in range(self.amountOfUniqueResources):

            resource = self.behaviourArray[product][0]
            temp[product][0] = resource

            amountPercentage = self.behaviourArray[product][1]
            amount = amountPercentage[0]*self.inStorageList[product]
            temp[product][1] = [amount]

            divergence = self.behaviourArray[product][2]
            
            temp[product][2] = [ ( amount * divergence[0] * self.market.RecordedPrice(product, resource[0]) ) + ( amount * self.market.RecordedPrice(product, resource[0]) ) ]
            #print("amount", amount, "amountPercentage", amountPercentage[0], "in storage", self.inStorageList[product], "divergence", divergence, "recorded price" , self.market.RecordedPrice(product, resource[0]))

        return temp

    

class BasicCurrencyBehaviour(Behaviour):

    def __init__(self, minAmount, maxAmount, underSell, overSell, resource, actor_ID, market):

        #Refernces
        self.market = market 
        self.resource = resource
        self.actor_ID = actor_ID

        #Values
        self.minAmount = minAmount
        self.maxAmount = maxAmount
        self.underSell = underSell
        self.overSell = overSell

        #Called and set values
        self.inStorageList = resource.resourceArray[actor_ID][0]
        self.amountOfUniqueResources = self.resource.amountOfUniqueResources
        self.InitilizeBehaviourArray()

    def PercentageToSell(self):
            # how large of a % it will sell of its resource
            percentage_to_sell = random.uniform(self.minAmount,self.maxAmount)
            return percentage_to_sell
    
    def DivergenceToSell(self):
            # % of how much it will deviate from the recorded market price of yesterday
            divergence_to_sell = random.uniform(self.underSell,self.overSell)  
            return divergence_to_sell
           
    def InitilizeBehaviourArray(self):

        self.behaviourArray = numpy.zeros((self.amountOfUniqueResources+1, 3), dtype = list)

        for product in range (self.amountOfUniqueResources+1):

            #Only necessary for Currency
            if product == self.resource.GetCurrency():
                currencyForWhatArray = numpy.zeros(self.amountOfUniqueResources, dtype = float)
                currencyAmountToSellArray = numpy.zeros(self.amountOfUniqueResources, dtype = float)
                currencyPriceArray = numpy.zeros(self.amountOfUniqueResources, dtype = float)

                amountToSell = (self.PercentageToSell()) / (self.amountOfUniqueResources-1)
                for resource in range(0,self.amountOfUniqueResources):
                    if resource != self.resource.GetCurrency():
                        currencyForWhatArray[resource] = resource
                        currencyAmountToSellArray[resource] = amountToSell
                        currencyPriceArray[resource] = self.DivergenceToSell()

                self.behaviourArray[product][0] = numpy.copy(currencyForWhatArray, order = 'K')
                self.behaviourArray[product][1] = numpy.copy(currencyAmountToSellArray, order='K')
                self.behaviourArray[product][2] = numpy.copy(currencyPriceArray, order='K')

            elif product != self.resource.GetCurrency():
                self.behaviourArray[product][0] = [self.resource.GetCurrency()]
                self.behaviourArray[product][1] = [self.PercentageToSell()]
                self.behaviourArray[product][2] = [self.DivergenceToSell()]
            

    def PostResources(self):
        
        placeHolderArray = numpy.zeros((self.amountOfUniqueResources+1, 3), dtype = list)

        for product in range(self.amountOfUniqueResources+1):

            # self.resource.GetCurrency() returns the name of the resource used as currency
            if product == self.resource.GetCurrency():
                placeHolderArray[product][0] = self.behaviourArray[product][0]

                placeHolderAmountArray = numpy.zeros(self.amountOfUniqueResources)
                placeHolderPriceArray = numpy.zeros(self.amountOfUniqueResources)

                currencyAmountToSellArray = self.behaviourArray[product][1]
                currencyPriceArray = self.behaviourArray[product][2]

                for resource in range(self.amountOfUniqueResources):
                    if resource != product:
                        placeHolderAmountArray[resource] = (currencyAmountToSellArray[resource]+1)*(self.resource.GetCurrencyAmount(self.actor_ID))
                        placeHolderPriceArray[resource] = (currencyPriceArray[resource]* self.market.RecordedPrice(product,resource ) * placeHolderAmountArray[resource]) + (self.market.RecordedPrice(product, resource) * placeHolderAmountArray[resource])

                placeHolderArray[product][1] = placeHolderAmountArray
                placeHolderArray[product][2] = placeHolderPriceArray

            elif product != self.resource.GetCurrency():
                    
                # Col1 = product name 
                # Col2 = Total amount to sell
                # Col3 = Price for our product
                placeHolderArray[product][0] = self.behaviourArray[product][0]
                placeHolderArray[product][1] = numpy.multiply(numpy.add(self.behaviourArray[product][1], [1]),(self.inStorageList[product]))
                placeHolderArray[product][2] = numpy.add(numpy.multiply(numpy.multiply(self.behaviourArray[product][2], placeHolderArray[product][1]), [self.market.RecordedPrice(product, 0)]),numpy.multiply([self.market.RecordedPrice(product, 0)], placeHolderArray[product][1]))

        return placeHolderArray

