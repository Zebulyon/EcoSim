#!/usr/bin/python3
import Market
from Resource import Resource

def TEST_resource_trading():
    TEST_resource_trading_even_ratio()
    TEST_resource_trading_not_even_ratio()
    TEST_resource_trading_not_functioning()
    TEST_resource_trading_multiple_trades_with_one()
    TEST_resource_trading_inverse_size()

def TEST_resource_trading_inverse_size():
    number_of_resources = 2
    number_of_actors = 2
    resource = Resource(0, 0, 0, 0, number_of_resources, number_of_actors)
    actor1 = 0
    actor2 = 1
    resource1 = 0
    resource2 = 1
    resource1_amount = 100
    resource2_amount = 60
    resource.resourceArray[actor1][0][resource2] = resource1_amount
    resource.resourceArray[actor2][0][resource1] = resource2_amount

    resource_before = resource.GetTotalResources()

    bartermark = Market.NiceMarket(number_of_resources, resource)
    bartermark.PostResource(resource1, resource2, 50, 100, actor1)
    bartermark.PostResource(resource2, resource1, 20, 60, actor2)
    bartermark.MatchTrades()
    if resource_before == resource.GetTotalResources() and resource.resourceArray[actor2][0][resource2] == 100 and resource.resourceArray[actor2][0][resource1] == 10 and resource.resourceArray[actor1][0][resource2] == 0 and resource.resourceArray[actor1][0][resource1] == 50:
        print("TEST_resource_trading_inverse_size successful")
    else:
        print("TEST_resource_trading_inverse_size failed")

def TEST_resource_trading_multiple_trades_with_one():
    number_of_resources = 2
    number_of_actors = 3
    resource = Resource(0, 0, 0, 0, number_of_resources, number_of_actors)
    actor1 = 0
    actor2 = 1
    actor3 = 2
    resource1 = 0
    resource2 = 1
    resource1_amount = 20
    resource2_amount = 20
    resource23_amount = 10
    resource.resourceArray[actor1][0][resource2] = resource1_amount
    resource.resourceArray[actor2][0][resource1] = resource2_amount
    resource.resourceArray[actor3][0][resource2] = resource23_amount

    resource_before = resource.GetTotalResources()

    bartermark = Market.NiceMarket(number_of_resources, resource)
    bartermark.PostResource(resource1, resource2, 10, 20, actor1)
    bartermark.PostResource(resource2, resource1, 40, 20, actor2)
    bartermark.PostResource(resource1, resource2, 5, 10, actor3)
    bartermark.MatchTrades()
    if resource_before == resource.GetTotalResources() and resource.resourceArray[actor2][0][resource2] == 30 and resource.resourceArray[actor2][0][resource1] == 5 and resource.resourceArray[actor1][0][resource2] == 0 and resource.resourceArray[actor1][0][resource1] == 10 and resource.resourceArray[actor3][0][resource2] == 0 and resource.resourceArray[actor3][0][resource1] == 5:
        print("TEST_resource_trading_multiple_trades_with_one successful")
    else:
        print("TEST_resource_trading_multiple_trades_with_one failed")

def TEST_resource_trading_even_ratio():
    number_of_resources = 2
    number_of_actors = 2
    resource = Resource(0, 0, 0, 0, number_of_resources, number_of_actors)
    actor1 = 0
    actor2 = 1
    resource1 = 0
    resource2 = 1
    resource1_amount = 20
    resource2_amount = 20
    resource.resourceArray[actor1][0][resource2] = resource1_amount
    resource.resourceArray[actor2][0][resource1] = resource2_amount

    resource_before = resource.GetTotalResources()

    bartermark = Market.NiceMarket(number_of_resources, resource)
    bartermark.PostResource(resource1, resource2, 10, 20, actor1)
    bartermark.PostResource(resource2, resource1, 40, 20, actor2)
    bartermark.MatchTrades()
    if resource_before == resource.GetTotalResources() and resource.resourceArray[actor2][0][resource2] == 20 and resource.resourceArray[actor2][0][resource1] == 10 and resource.resourceArray[actor1][0][resource2] == 0 and resource.resourceArray[actor1][0][resource1] == 10:
        print("TEST_resource_trading_even_ratio successful")
    else:
        print("TEST_resource_trading_even_ratio failed")

def TEST_resource_trading_not_even_ratio():
    number_of_resources = 2
    number_of_actors = 2
    resource = Resource(0, 0, 0, 0, number_of_resources, number_of_actors)
    actor1 = 0
    actor2 = 1
    resource1 = 0
    resource2 = 1
    resource1_amount = 20
    resource2_amount = 20
    resource.resourceArray[actor1][0][resource2] = resource1_amount
    resource.resourceArray[actor2][0][resource1] = resource2_amount

    resource_before = resource.GetTotalResources()

    bartermark = Market.NiceMarket(number_of_resources, resource)
    bartermark.PostResource(resource1, resource2, 10, 20, actor1)
    bartermark.PostResource(resource2, resource1, 30, 20, actor2)
    bartermark.MatchTrades()
    if resource_before == resource.GetTotalResources() and resource.resourceArray[actor2][0][resource2] == 20 and resource.resourceArray[actor2][0][resource1] == 10 and resource.resourceArray[actor1][0][resource2] == 0 and resource.resourceArray[actor1][0][resource1] == 10:
        print("TEST_resource_trading_not_even_ratio successful")
    else:
        print("TEST_resource_trading_not_even_ratio failed")


def TEST_resource_trading_not_functioning():
    number_of_resources = 2
    number_of_actors = 2
    resource = Resource(0, 0, 0, 0, number_of_resources, number_of_actors)
    actor1 = 0
    actor2 = 1
    resource1 = 0
    resource2 = 1
    resource1_amount = 20
    resource2_amount = 20
    resource.resourceArray[actor1][0][resource2] = resource1_amount
    resource.resourceArray[actor2][0][resource1] = resource2_amount

    resource_before = resource.GetTotalResources()

    bartermark = Market.NiceMarket(number_of_resources, resource)
    bartermark.PostResource(resource1, resource2, 10, 20, actor1)
    bartermark.PostResource(resource2, resource1, 50, 20, actor2)
    bartermark.MatchTrades()
    if resource_before == resource.GetTotalResources() and resource.resourceArray[actor2][0][resource2] == 0 and resource.resourceArray[actor2][0][resource1] == 20 and resource.resourceArray[actor1][0][resource2] == 20 and resource.resourceArray[actor1][0][resource1] == 0:
        print("TEST_resource_trading_not_functioning successful")
    else:
        print("TEST_resource_trading_not_functioning failed")

if __name__ == "__main__":
    TEST_resource_trading()