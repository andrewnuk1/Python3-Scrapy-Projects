import scrapy

from urllib.parse import urljoin
from foodstandardsagency.items import FoodstandardsagencyItem
from selenium import webdriver
from scrapy.http import TextResponse

class foodstandardsagencySpider(scrapy.Spider):
    name = "foodstandardsagency"
    allowed_domains = ["ratings.food.gov.uk"]
    start_urls = ["http://ratings.food.gov.uk/open-data/en-GB"]

    def parse(self, response):
        for href in response.xpath('//tr/td/a[text()[contains(.,"English")]]/@href'):
            url = urljoin('http://ratings.food.gov.uk/',href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def __init__(self):
        try:
            self.driver = webdriver.Chrome("C:/Users/xxxxxx/Downloads/chromedriver_win32/chromedriver.exe")
        except:
            self.driver = webdriver.Chrome("C:/Users/xxxxx/Downloads/chromedriver_win32/chromedriver.exe")
            
    def parse_dir_contents(self, response):  
        self.driver.get(response.url)

        response1 = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        for sel in response1.xpath('//*[@id="collapsible2"]/div[@class="expanded"]/div[@class="collapsible-content"]/div[@class="collapsible"]/div[@class="expanded"]'):
            businessname = sel.xpath('.//span[text()[contains(.,"<BusinessName")]]/../span[2]/text()').extract()
            postcode = sel.xpath('.//span[text()[contains(.,"<PostCode")]]/../span[2]/text()').extract()
            businesstype = sel.xpath('.//span[text()[contains(.,"<BusinessType") and not(contains(., "<BusinessTypeID"))]]/../span[2]/text()').extract()
            businesstypeID = sel.xpath('.//span[text()[contains(.,"<BusinessTypeID")]]/../span[2]/text()').extract()
            ratingvalue = sel.xpath('.//span[text()[contains(.,"<RatingValue")]]/../span[2]/text()').extract()
            ratingdate = sel.xpath('.//span[text()[contains(.,"<RatingDate")]]/../span[2]/text()').extract()
            item = FoodstandardsagencyItem()
            item['businessname'] = businessname
            item['postcode'] = postcode
            item['businesstype'] = businesstype
            item['businesstypeID'] = businesstypeID
            item['ratingvalue'] = ratingvalue
            item['ratingdate'] = ratingdate
            yield item

##        self.driver.close()
