import scrapy
import time

from BerkeleyHomes.items import BerkeleyHomesItem
from selenium import webdriver
from scrapy.http import TextResponse

class berkeleyhomesSpider(scrapy.Spider):
    name = "berkeleyhomes"
    allowed_domains = ["berkeleygroup.co.uk"]
    start_urls = [
        "http://www.berkeleygroup.co.uk/new-homes/developments-by-county/",        
    ]

    def parse(self, response):
        for href in response.xpath('//*/a[@class="button-dark-grey"]/@href'):
           url = response.urljoin(href.extract())
#           print url
           yield scrapy.Request(url, callback=self.parse_dir_url1)

    def parse_dir_url1(self, response):
        for href1 in response.xpath('//*/a[@class="action view red"]/@href'):
           url1 = response.urljoin(href1.extract())
#           print url1
           yield scrapy.Request(url1, callback=self.parse_dir_contents)

    def __init__(self):
        self.driver = webdriver.Chrome("C:/Users/andrew/Downloads/chromedriver_win32/chromedriver.exe")

    def parse_dir_contents(self, response):
        count = 0
        self.driver.get(response.url)
        
        while True:
            if count >0:
                try:
                    next = self.driver.find_element_by_xpath('//ul[@class="pagination"]/li[@class="next"]/a')
                    count = count +1
                    next.click()
                except:
                    break
            else:
                count = count + 1

            time.sleep(10)
            response1 = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
            item = BerkeleyHomesItem()
            for sel in response1.xpath('//*[@class="flexStretch"]'):
                item['name'] = sel.xpath('//*[@class="span10"]/div/h1/text()').extract()
                item['address'] = sel.xpath('//*[@class="span10"]/div/h2/text()').extract()
                plotnames = sel.xpath('//*/td/a[contains(text(),"View")]/../../td[2]/text()').extract()
                plotnames = [plotname.strip() for plotname in plotnames]
    #            plotphases = sel.xpath('//*/td[contains(text(),"Available")]/../td[8]/text()').extract()
    #            plotphases = [plotphase.strip() for plotphase in plotphases]

                plotprices = sel.xpath('//*/td/a[contains(text(),"View")]/../../td[@data-sort]/text()').extract()
                plotprices = [plotprice.strip() for plotprice in plotprices]
                result = zip(plotnames, plotprices)
                for plotname, plotprice in result:
                    item['plotname'] = plotname
    #                item['plotphase'] = plotphase
                    item['plotprice'] = plotprice
                    yield item

