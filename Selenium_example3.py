import scrapy
import time

from Ebags.items import EbagsItem
from selenium import webdriver
from scrapy.http import TextResponse

class ebagsSpider(scrapy.Spider):
    name = "ebags"
    allowed_domains = ["ebags.com"]
    start_urls = [
        "https://www.ebags.com/brands",        
    ]

    def parse(self, response):
        for href in response.xpath('//*[@class="mainCon"]/div[@class="brandListCon"]/div[@class="brandList4Col"]/a/@href'):
           url = response.urljoin(href.extract())
           yield scrapy.Request(url, callback=self.parse_dir_contents)

    def __init__(self):
        self.driver = webdriver.Chrome("C:<path to file>/chromedriver_win32/chromedriver.exe")

    def parse_dir_contents(self, response):
        count = 0
        self.driver.get(response.url)
        
        while True:
            if count >0:
                try:
                    next = self.driver.find_element_by_xpath('//div[@class="pageThis"]/ul/li[@class="pageNext"]/a')
                    count = count +1
                    next.click()
                except:
                    break
            else:
                count = count + 1

            time.sleep(10)
            response1 = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
            item = EbagsItem()
            for sel in response1.xpath('//div[@class="ProductListWrap responsiveList"]'):
                item['brand'] = sel.xpath('//*[@class="selectionsTitle bfx-price"]/text()').extract()
                item['items'] = sel.xpath('//*[@class="selectionsCount"][@id="searchResultsCount"]/text()').extract()
                productnames = sel.xpath('//*[@class="itemProductName"]/a/text()').extract()
                productnames = [productname.strip() for productname in productnames]
                productnumbers = sel.xpath('//*[@class="itemProductName"]/a/@href').re(r'.*\/(.*)(?=\?productid)')
                productnumbers = [productnumber.strip() for productnumber in productnumbers]
                productids = sel.xpath('//*[@class="itemProductName"]/a/@href').re(r'(?<=productid=)(.*)')
                productids = [productid.strip() for productid in productids]
                result = zip(productnames, productnumbers, productids)
                for productname, productnumber, productid in result:
                    item['productname'] = productname
                    item['productnumber'] = productnumber
                    item['productid'] = productid
                    yield item
