import random
import numpy

class Resource:
    def __init__(self, lowestStock, highestStock, lowestProd, highestProd, resources, actoramount, currency=False):
        self.actoramount = actoramount
        self.amountOfUniqueResources = resources
        self.currency = currency
        if self.currency == True:
            self.resourceArray = numpy.zeros((actoramount, 4), dtype = list)
            self.currencyIndex = self.amountOfUniqueResources
        else:
            self.resourceArray = numpy.zeros((actoramount, 3), dtype = list)

        goodsArray = numpy.zeros(self.amountOfUniqueResources, dtype = int)
        productionArray = numpy.zeros(self.amountOfUniqueResources, dtype = float)
        gainArray = numpy.zeros(self.amountOfUniqueResources, dtype = float)

        # array[y-axsis][x-axsis] 
        self.resourceArray[0][0] = goodsArray
        self.resourceArray[0][1] = productionArray
        self.resourceArray[0][2] = gainArray

        for row in range(actoramount):
            for line in range(self.amountOfUniqueResources):
                #How much they have of it 
                goodsArray[line] = random.uniform(lowestStock, highestStock)
                #What the production is
                productionArray[line] = random.uniform(lowestProd, highestProd)
                #What is the gain from production, the -1 is to take account of the fact that arrays/list start at zero
                gainArray[line] = random.randint(0, self.amountOfUniqueResources-1)

            #Inserts the arrays into the main one
            self.resourceArray[row][0] = numpy.copy(goodsArray, order='K')
            self.resourceArray[row][1] = numpy.copy(productionArray, order='K') 
            self.resourceArray[row][2] = numpy.copy(gainArray, order='K')
            
            if self.currency == True:
                self.resourceArray[row][3] = random.uniform(lowestStock, highestStock)

    def GetCurrency(self):
        return self.currencyIndex

    def GetCurrencyAmount(self, actorid):
        return self.resourceArray[actorid][3]

    def Produce(self):
        for row in self.resourceArray:
            gainArray = row[2]
            productionArray = row[1]
            amountArray = row[0]
            producedArray = numpy.zeros(self.amountOfUniqueResources)
            for resource in range(self.amountOfUniqueResources):
                if productionArray[resource] < 0: #If there is negative production, reduce the reducing resource instead of the other resource.
                    producedArray[resource] += productionArray[resource] * amountArray[resource]
                else:
                    producedArray[int(gainArray[resource])] += productionArray[resource] * amountArray[resource]
                producedArray[resource] += amountArray[resource]

            for resource in range(self.amountOfUniqueResources):
                amountArray[resource] = producedArray[resource] 
            
    def ProduceConverging(self, MAX_VALUE):
        for row in self.resourceArray:
            gainArray = row[2]
            productionArray = row[1]
            amountArray = row[0]
            producedArray = numpy.zeros(self.amountOfUniqueResources)
            for resource in range(self.amountOfUniqueResources):
                if productionArray[resource] < 0: #If there is negative production, reduce the reducing resource instead of the other resource.
                    producedArray[resource] += productionArray[resource] * amountArray[resource]
                else:
                    #We put a cap on how much productivity is allowed, if someone has resources larger than MAX_VALUE then they only produce with
                    #MAX_VALUE and their productivity factor.
                    if amountArray[resource] > MAX_VALUE:
                        producedArray[int(gainArray[resource])] += productionArray[resource] * MAX_VALUE
                    else:
                        producedArray[int(gainArray[resource])] += productionArray[resource] * amountArray[resource]
                producedArray[resource] += amountArray[resource]

            for resource in range(self.amountOfUniqueResources):
                amountArray[resource] = producedArray[resource]

    def GetTotalResources(self):
        total = 0
        for row in self.resourceArray:
            cur_row = row[0]
            for i in range(self.amountOfUniqueResources):
                total += cur_row[i]
        return total

    #Trades resource1_amnt of resource1 from actor1 for resource2_amnt of resource2 from actor2
    def TradeResource(self, actor1, actor2, resource1_amnt, resource2_amnt, resource1, resource2):
        if self.currency == True and resource1 == self.currencyIndex:
            if self.resourceArray[actor1][3] >= resource1_amnt and self.resourceArray[actor2][0][resource2] >= resource2_amnt:
                self.resourceArray[actor1][3] -= resource1_amnt
                self.resourceArray[actor1][0][resource2] += resource2_amnt
                self.resourceArray[actor2][0][resource2] -= resource2_amnt
                self.resourceArray[actor2][3] += resource1_amnt
        
        elif self.currency == True and resource2 == self.currencyIndex:
            if self.resourceArray[actor1][0][resource1] >= resource1_amnt and self.resourceArray[actor2][3] >= resource2_amnt:
                self.resourceArray[actor1][0][resource1] -= resource1_amnt
                self.resourceArray[actor1][3] += resource2_amnt
                self.resourceArray[actor2][3] -= resource2_amnt
                self.resourceArray[actor2][0][resource1] += resource1_amnt

        else:
            if self.resourceArray[actor1][0][resource1] >= resource1_amnt and self.resourceArray[actor2][0][resource2] >= resource2_amnt:
                self.resourceArray[actor1][0][resource1] -= resource1_amnt
                self.resourceArray[actor1][0][resource2] += resource2_amnt
                self.resourceArray[actor2][0][resource2] -= resource2_amnt
                self.resourceArray[actor2][0][resource1] += resource1_amnt