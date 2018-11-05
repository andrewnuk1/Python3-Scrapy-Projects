import scrapy

from autotrader.items import AutotraderItem

class AutotraderSpider(scrapy.Spider):
    name = "autotrader"
    allowed_domains = ["autotrader.co.uk"]

    while True:
        to_do = input("Enter 1 for cars or 2 for bikes or 3 for vans  ")
        if to_do == "1":
            start_urls = ["https://www.autotrader.co.uk/car-dealers/search?advertising-location=at_cars&postcode=m43aq&radius=1501&forSale=on&toOrder=on&page=1&sort=with-retailer-reviews"
                 ]
            break
        elif to_do == "2":
            start_urls = ["https://www.autotrader.co.uk/bikes/motorcycle-dealers/search?advertising-location=at_bikes&postcode=m43aq&radius=1500&forSale=on&toOrder=on&page=1&sort=with-retailer-reviews"
                 ]
            break        
        elif to_do == "3":
            start_urls = ["https://www.autotrader.co.uk/vans/van-dealers/search?advertising-location=at_vans&postcode=m43aq&radius=1500&page=1&sort=with-retailer-reviews"
                 ]
            break        

    def parse(self, response):
        for sel in response.xpath('//li[@class="dealerList__itemContainer"]'):
            name = sel.xpath('.//*[@itemprop="legalName"]/text() ').extract()
            address = sel.xpath('.//article/a/div/p[@itemprop="address"]/text()').extract()
            cars = sel.xpath('.//article/a/div/p[@class="dealerList__itemCount"]/span/text()').extract() 
            dealer_url = sel.xpath('.//article/a/@href').extract()
            item = AutotraderItem()
            item['name'] = name
            item['address'] = address
            item['cars'] = cars
            item['dealer_url'] = dealer_url
            yield item

        next_page = response.xpath('.//a[@class="pagination--right__active"]/@href').extract()
        if next_page:
            next_href = next_page[0]
            next_page_url = next_href
            request = scrapy.Request(url=next_page_url)
            yield request
