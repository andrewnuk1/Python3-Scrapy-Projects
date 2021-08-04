import scrapy

from TaylorWimpey.items import TaylorwimpeyItem

from scrapy.http import TextResponse
from selenium import webdriver

class taylorwimpeySpider(scrapy.Spider):
    
    name = "taylorwimpey"
    allowed_domains = ["taylorwimpey.co.uk"]

    start_urls = ["https://www.taylorwimpey.co.uk/sitemap"]
    
    
    def __init__(self):
        try:
            self.driver = webdriver.Chrome("C:/Users/andrew/Downloads/chromedriver_win32/chromedriver.exe")
        except:
            self.driver = webdriver.Chrome("C:/Users/andre/Downloads/chromedriver_win32/chromedriver.exe")    


    def parse(self, response): # build a list of all locations
        self.driver.get(response.url)
        response1 = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        
        url_list1 = []
        
        for href in response1.xpath('//div[@class="content-container"]/ul/li/a/@href'):
            url = response1.urljoin(href.extract())
            url_list1.append(url)
            print(url)
        
        for url_development1 in url_list1:        
            yield scrapy.Request(url_development1, callback=self.parse_dir_contents1)


    def parse_dir_contents1(self, response): # go through each location to find all developments
        self.driver.get(response.url)
        response1 = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        
        url_list = []
        
        for href in response1.xpath('//div[@class="col col--results"]/div[@class="home-finder-results-wrapper"]/div/div/div/div/div/a/@href'):
            url = response1.urljoin(href.extract())
            url_list.append(url)
            print(url)
        
        url_list_unique = list(set(url_list)) # eliminate duplicate developments
        
        for url_development in url_list_unique:        
            yield scrapy.Request(url_development, callback=self.parse_dir_contents)
                
   
    def parse_dir_contents(self, response):
        self.driver.get(response.url)
        response1 = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')

        development_name = response1.xpath('//div/h1[@class="landing-page-hero__title"]/text()').extract()[0].strip()
        development_postcode = response1.xpath('//div[@class="contact-us"]/div/div[@class="contact-us-block"]/div[@class="contact-us-block__address"]/span/text()').extract()
                
        for sel in response1.xpath('//section[@id="plots-list"]/div/div/div[@class="plots-list__plots content-container"]/div[@class="plots-list-cards"]/div'):
           item = TaylorwimpeyItem()
           item['name'] = development_name
           item['address'] = development_postcode
           item['plotprice'] = sel.xpath('.//div/div[@class="plot-card-price"]/div[@class="plot-card-price__text"]/h3/text()').extract()
           item['plotname'] = sel.xpath('.//div[@class="plots-list-card-details"]/div/text()').extract()
           #item['plotid'] = sel.xpath('//*[@id="maincontent_0_developmentBrochures_brochures"]/li/a/@href').re(r'(?<={)(.*?)(?=})')
           yield item
        
