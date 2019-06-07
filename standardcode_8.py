import scrapy
import time

from Ebags.items import EbagsItem
from selenium import webdriver
from scrapy.http import TextResponse

class ebagsSpider(scrapy.Spider):
    name = "ebags"
    allowed_domains = ["ebags.com"]
    start_urls = ["https://www.ebags.com/brands"]

    def parse(self, response):
        item = EbagsItem()
        for sel in response.xpath('//*[@class="container buffer-top buffer-bottom"]'):
            brands = sel.xpath('//*[@class="container buffer-top buffer-bottom"]/div[@class="brandListCon"]/ul[@class="brandListCol"]/li/a/text()').extract()
            brands = [brand.strip() for brand in brands]
            result = zip(brands)
            for brand in result:
                item['brand'] = brand
                yield item 
