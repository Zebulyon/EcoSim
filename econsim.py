#!/usr/bin/python3
import time
import random
import numpy
import array
import Market

#Make several arrays so that we can easily read values as well as handle data quicker.
class Resource:
    def __init__(self, lowestStock, highestStock, lowestProd, highestProd, resources, actoramount):
        self.resourceAmount = resources
        self.resource = numpy.zeros((actoramount, resources * 3))
        for row in self.resource:
            for i in range(resources):
                row[i * 3] = random.uniform(lowestStock, highestStock)
                row[i * 3 + 1] = random.uniform(lowestProd, highestProd)
                row[i * 3 + 2] = random.randint(0, resources - 1)

    def Produce(self):
        for row in self.resource:
            temp = [0] * self.resourceAmount
            for i in range(self.resourceAmount):
                temp[i] += row[i * 3]
                temp[int(row[i * 3 + 2])] += row[i * 3] * row[i * 3 + 1]
            for i in range(self.resourceAmount):
                row[i * 3] = temp[i]

    def GetTotalResources(self):
        total = 0
        for row in self.resource:
            for i in range(self.resourceAmount):
                total += row[i * 3]
        return total

    #Trades resource1_amnt of resource1 from actor1 for resource2_amnt of resource2 from actor2
    def TradeResource(self, actor1, actor2, resource1_amnt, resource2_amnt, resource1, resource2):
        if self.resource[actor1][resource1 * 3] >= resource1_amnt and self.resource[actor2][resource2 * 3] >= resource2_amnt:
            self.resource[actor1][resource1 * 3] -= resource1_amnt
            self.resource[actor1][resource2 * 3] += resource2_amnt
            self.resource[actor2][resource2 * 3] -= resource2_amnt
            self.resource[actor2][resource1 * 3] += resource1_amnt

#Abstract behavior class
class Behavior:
    #Randomize the values used to determine behavior
    def __init__(self, resourceAmount):
        raise NotImplementedError("Abstract class")

    def PostResource(self, resource, currentStock, currentProductivity, marketPrice):
        raise NotImplementedError("Abstract class")

class BasicUniform(Behavior):
    def __init__(self, resourceAmount, lowest_div, highest_div, min_sold, max_sold):
        self.resource = []
        for _ in range(resourceAmount):
            percentage_to_sell = random.uniform(0, 1)
            divergence_from_price = random.uniform(lowest_div, highest_div)
            self.resource.append((percentage_to_sell, divergence_from_price))

    def PostResource(self, resource, currentStock, currentProductivity, marketPrice):
        print("lmao")

def main():
    number_of_resources = 4
    number_of_actors = 10000

    resource = Resource(0, 100, -0.2, 0.2, number_of_resources, number_of_actors)
    print(resource.GetTotalResources())
    bartermark = Market.NiceMarket(number_of_resources, resource)
    print(resource.GetTotalResources())
    for _ in range(2):
        resource.Produce()
    print(resource.GetTotalResources())

if __name__ == "__main__":
    main()