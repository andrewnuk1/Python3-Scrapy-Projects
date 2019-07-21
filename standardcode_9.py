import scrapy

from justeat.items import JusteatItem
from scrapy.http import TextResponse
from  more_itertools import unique_everseen

class JusteatSpider(scrapy.Spider):
    name = "justeat"
    allowed_domains = ["just-eat.co.uk"]

    # download the restuarant_urls.txt from justeat1 spider output
    with open("restuarant_urls.txt") as f:
        restuarant_urls = [x.strip('\n') for x in f.readlines()]
    restuarant_urls=list(unique_everseen(restuarant_urls))

    # we need to run this in stages, about 7000 restuarants at a time max.
    print("total number of restaurants:  " + str(len(restuarant_urls)))
    print("first record:  " + str(restuarant_urls[0]))
    print("8000th record:  " + str(restuarant_urls[7999]))
    print("last record:  " + str(restuarant_urls[len(restuarant_urls)-1]))

    while True:
        to_do = input("Enter Stage 1 to X (max 6 for now)  ")
        if to_do == "1" or to_do == "2" or to_do =="3" or to_do =="4" or to_do =="5"  or to_do =="6":
            break

    # build a list of urls to scrap  
    start_urls = []
    startrange = 7000*(int(to_do)-1)
    endrange = 7000*(int(to_do))
    if endrange > len(restuarant_urls):
        endrange = len(restuarant_urls)
    for a in range(startrange,endrange):    
        start_urls.append("https://www.just-eat.co.uk" + str(restuarant_urls[a]))


    def parse(self, response):
        for sel in response.xpath('//div[@class="restaurantParts"]'):
            item = JusteatItem()
            item['name'] = sel.xpath('//*[@itemprop="name"]/text()').extract()
            item['address'] = sel.xpath('//*[@itemprop="address"]/span/text()').extract()
            item['cuisine'] = sel.xpath('.//div/p/span[@itemprop="servesCuisine"]/text()').extract()
            item['ratingvalue'] = sel.xpath('.//div/p[@itemprop="aggregateRating"]/meta[@itemprop="ratingValue"]/@content').extract()
            item['ratingcount'] = sel.xpath('.//div/p[@itemprop="aggregateRating"]/meta[@itemprop="ratingCount"]/@content').extract()
            item['ratingbest'] = sel.xpath('.//div/p[@itemprop="aggregateRating"]/meta[@itemprop="bestRating"]/@content').extract()
            item['ratingworst'] = sel.xpath('.//div/p[@itemprop="aggregateRating"]/meta[@itemprop="worstRating"]/@content').extract()
            item['name_id'] = sel.xpath('.//@data-restaurant-id').extract()
            yield item
