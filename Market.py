#Class for handling the information posted on the market
import numpy

ARRAY_INCREASE_SIZE = 50000
MARKET_POST_SIZE = 6
class MarketPost:
    def __init__(self, resource1, resource1_amount, resource2, resource2_amount, posterid):
        self.res1 = resource1
        self.res1_amnt = resource1_amount
        self.res2 = resource2
        self.res2_amnt = resource2_amount
        self.id = posterid
        self.greedratio = resource1_amount / resource2_amount
    
    def __repr__(self):
        return str(self.res1) + " " + str(self.res1_amnt) + " " + str(self.res2) + " " + str(self.res2_amnt) + " " + str(self.id)
    #Get the ratio between the wanted product and the sold product the lower the less greedy
    def GetGreedRatio(self):
        return self.greedratio

#####Market array handling class
class PostArray:
    def __init__(self):
        self.total_size = ARRAY_INCREASE_SIZE
        self.current_size = 0
        self.start = 0
        self.array = numpy.zeros((ARRAY_INCREASE_SIZE, MARKET_POST_SIZE), dtype=float)

    def _PutPostInMarket(self, post):
        if self.current_size < self.total_size:
            row = self.array[self.current_size]
            row[0] = post.res1
            row[1] = post.res1_amnt
            row[2] = post.res2
            row[3] = post.res2_amnt
            row[4] = post.id
            row[5] = post.greedratio
            self.current_size += 1
        else:
            self._IncreaseMarketSize()
            self._PutPostInMarket(post)
    
    def _IncreaseMarketSize(self):
        old_size = self.total_size
        new_size = old_size + ARRAY_INCREASE_SIZE
        self.total_size = new_size
        new_array = numpy.zeros((new_size, MARKET_POST_SIZE))
        new_array[0:old_size, 0:MARKET_POST_SIZE] = self.array
        self.array = new_array

    def pop(self):
        self.start += 1

    def _GetPostInMarket(self, post_num):
        if post_num < self.current_size:
            row = self.array[self.start + post_num]
            return MarketPost(int(row[0]), row[1], int(row[2]), row[3], int(row[4]))
        else:
            raise(IndexError())

    def _OrderByGreed(self):
        self.array[self.array[:, 5].argsort()]

    def Clear(self):
        self.start = 0
        self.current_size = 0

class Market:
    def __init__(self, resourceAmount, resources):
        self.markets = {}
        self.market_current_size = {}
        self.market_total_size = {}
        self.resourceAmount = resourceAmount
        self.resources = resources
        self.recordedPrice = []
        self.sales_in_day = 0

    #Posts a proposed trade in the correct market
    def PostResource(self, PostedResource, WantedResource, postedAmount, wantedAmount, posterID):
        if postedAmount <= 0 or wantedAmount <= 0:
            return
        marketkey = self._GetMarketKey(PostedResource, WantedResource)
        self.markets[marketkey]._PutPostInMarket(MarketPost(PostedResource, postedAmount, WantedResource, wantedAmount, posterID))

    #Trades resource1_amount of resource1 from actor1 for resource2_amount of resource2 from actor2
    def _TradeResources(self, resource1, resource1_amount, actor1, resource2, resource2_amount, actor2):
        self.recordedPrice[resource1][resource2] = resource2_amount / resource1_amount
        self.recordedPrice[resource2][resource1] = resource1_amount / resource2_amount
        self.resources.TradeResource(actor1, actor2, resource1_amount, resource2_amount, resource1, resource2)
        self.sales_in_day += 1

    def MatchTrades(self):
        raise NotImplementedError("Abstract method")

    def RecordedPrice(self, product, resource):
        return self.recordedPrice[product][resource]

    #Kind of dumb key for this dictionary because a better one has yet to be found.
    def _GetMarketKey(self, posted, wanted):
        return str(posted) + "to" + str(wanted)


class CurrencyMarket(Market):
    def __init__(self, resourceAmount, resources, currency):
        super().__init__(resourceAmount, resources)
        self.currency = currency
        for i in range(resourceAmount):
            self.recordedPrice.append([1])
            self.markets[self._GetMarketKey(self.currency, i)] = PostArray()
            self.markets[self._GetMarketKey(i, self.currency)] = PostArray()
        self.recordedPrice.append([])
        for i in range(self.currency):
            self.recordedPrice[currency].append(1)

    def RecordedPrice(self, product, resource):
        if resource == self.currency: #If the looked for price is the currency then we look at space 0, not at space resource
            return self.recordedPrice[product][0]
        else:
            return self.recordedPrice[product][resource]

    def SetRecordedPrice(self, product, resource, price):
        if product == self.currency:
            self.recordedPrice[product][resource] = 1/price
            self.recordedPrice[resource][0] = price
        else:
            self.recordedPrice[resource][product] = 1/price
            self.recordedPrice[product][0] = price

class BarterMarket(Market):
    def __init__(self, resourceAmount, resources):
        super().__init__(resourceAmount, resources)
        for i in range(resourceAmount):
            self.recordedPrice.append([])
            for j in range(resourceAmount):
                self.recordedPrice[i].append(1)
                if i != j:
                    self.markets[self._GetMarketKey(i, j)] = PostArray()


class NiceCurrencyMarket(CurrencyMarket):
    def MatchTrades(self):
        for i in range(self.resourceAmount):
            key1 = self._GetMarketKey(i, self.currency)
            key2 = self._GetMarketKey(self.currency, i)
            self.markets[key1]._OrderByGreed()
            self.markets[key2]._OrderByGreed()
            trades_exist = self._FindNextPair(self.markets[key1], self.markets[key2])
            while trades_exist:
                trades_exist = self._FindNextPair(self.markets[key1], self.markets[key2])
        for market in self.markets.values():
            market.Clear()

    def _FindNextPair(self, marketlist1, marketlist2):
        if marketlist1.current_size - marketlist1.start < 1 or marketlist2.current_size - marketlist2.start < 1:
            return False
        #Attempts to match the two first posts in the list
        firstPost = marketlist1._GetPostInMarket(0)
        secondPost = marketlist2._GetPostInMarket(0)
        if firstPost.res1_amnt / firstPost.res2_amnt <= secondPost.res2_amnt / secondPost.res1_amnt:
            self._MakeTrade(firstPost, secondPost)
            if firstPost.res1_amnt == 0:
                marketlist1.pop()
            else:
                marketlist2.pop()
            return True
        return False

    #Calculates the total product sold and at which exact price
    def _MakeTrade(self, post1, post2):
        trade_ratio = post1.res1_amnt / post1.res2_amnt
        #If post2 has more resources to trade at this rate then post1 does.
        if post1.res2_amnt * trade_ratio <= post2.res2_amnt * trade_ratio:
            self._TradeResources(post1.res2, post1.res2_amnt, post1.id, post2.res2, post1.res1_amnt, post2.id)
            ratio = post2.res1_amnt / post2.res2_amnt
            post2.res2_amnt -= post1.res1_amnt
            post2.res1_amnt = post2.res2_amnt * ratio
            post1.res2_amnt = 0
            post1.res1_amnt = 0
        else:
            self._TradeResources(post1.res2, post2.res1_amnt, post1.id, post2.res2, post2.res2_amnt, post2.id)
            ratio = post2.res1_amnt / post2.res2_amnt
            post1.res2_amnt -= post2.res1_amnt
            post1.res1_amnt = post1.res2_amnt * ratio
            post2.res1_amnt = 0
            post2.res2_amnt = 0

    #Trades resource1_amount of resource1 from actor1 for resource2_amount of resource2 from actor2
    def _TradeResources(self, resource1, resource1_amount, actor1, resource2, resource2_amount, actor2):
        self.SetRecordedPrice(resource1, resource2, resource2_amount / resource1_amount)
        self.SetRecordedPrice(resource2, resource1, resource1_amount / resource2_amount)
        self.resources.TradeResource(actor1, actor2, resource1_amount, resource2_amount, resource1, resource2)
        self.sales_in_day += 1

class NiceMarket(BarterMarket): #The nice market lets people with the lowest asking price get the lowest asking price of the reverse
                                #Thus you'll have to be nice (not greedy) in order to get the best deals.
    def MatchTrades(self):
        self.sales_in_day = 0
        for i in range(self.resourceAmount):
            for j in range(i + 1, self.resourceAmount):
                key1 = self._GetMarketKey(i, j)
                key2 = self._GetMarketKey(j, i)
                self.markets[key1]._OrderByGreed()
                self.markets[key2]._OrderByGreed()
                trades_exist = self._FindNextPair(self.markets[key1], self.markets[key2])
                while trades_exist:
                    trades_exist = self._FindNextPair(self.markets[key1], self.markets[key2])
        for market in self.markets.values():
            market.Clear()

    #Finds the next pair in the non-greedy list. The pair is matched and if the ratio of buy/sell is larger for the person trading the resource
    #away then the trade goes through at the price of the more expensive partner
    def _FindNextPair(self, marketlist1, marketlist2):
        if marketlist1.current_size - marketlist1.start < 1 or marketlist2.current_size - marketlist2.start < 1:
            return False
        #Attempts to match the two first posts in the list
        firstPost = marketlist1._GetPostInMarket(0)
        secondPost = marketlist2._GetPostInMarket(0)
        if firstPost.res1_amnt / firstPost.res2_amnt <= secondPost.res2_amnt / secondPost.res1_amnt:
            self._MakeTrade(firstPost, secondPost)
            if firstPost.res1_amnt == 0:
                marketlist1.pop()
            else:
                marketlist2.pop()
            return True
        return False
                
    #Calculates the total product sold and at which exact price
    def _MakeTrade(self, post1, post2):
        trade_ratio = post1.res1_amnt / post1.res2_amnt
        #If post2 has more resources to trade at this rate then post1 does.
        if post1.res2_amnt * trade_ratio <= post2.res2_amnt:
            self._TradeResources(post1.res2, post1.res2_amnt, post1.id, post2.res2, post1.res1_amnt, post2.id)
            ratio = post2.res1_amnt / post2.res2_amnt
            post2.res2_amnt -= post1.res1_amnt
            post2.res1_amnt = post2.res2_amnt * ratio
            post1.res2_amnt = 0
            post1.res1_amnt = 0
        else:
            self._TradeResources(post1.res2, post2.res1_amnt, post1.id, post2.res2, post2.res2_amnt, post2.id)
            ratio = post2.res1_amnt / post2.res2_amnt
            post1.res2_amnt -= post2.res1_amnt
            post1.res1_amnt = post1.res2_amnt / ratio
            post2.res1_amnt = 0
            post2.res2_amnt = 0

