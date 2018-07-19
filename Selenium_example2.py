import scrapy
import time

from urllib.parse import urljoin
from hungryhouse.items import HungryhouseItem
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.http import TextResponse

class HungryhouseSpider(scrapy.Spider):
    name = "hungryhouse"
    allowed_domains = ["hungryhouse.co.uk"]
    start_urls =["https://hungryhouse.co.uk/takeaway"]

    # parse / parse_dir_contents / parse_dir_contents1 follow the links the page with the restaurant lists
    # parse starts at the city list page
    def parse(self,response):
        for href in response.xpath('//*[@class="CmsRestcatCityLandingLocations"]/ul[@class="cities"]/li/a/@href'):
           url = urljoin('https://hungryhouse.co.uk/',href.extract())
           yield scrapy.Request(url, callback=self.parse_dir_contents)

    # parse_dir_contents will get to the web page with the lists except for London
    def parse_dir_contents(self, response):
        for href1 in response.xpath('//*[contains(text(),"Choose your location")]/../ul/li/a/@href'):
           url1 = urljoin('https://hungryhouse.co.uk/',href1.extract())
           if "london-takeaway" in url1:
               yield scrapy.Request(url1, callback=self.parse_dir_contents1)
           yield scrapy.Request(url1, callback=self.parse_dir_contents2)
           
    # parse_dir_contents1 is needed for London which is one link deeper
    def parse_dir_contents1(self, response):
        for href2 in response.xpath('//*[contains(text(),"Choose your location")]/../ul/li/a/@href'):
           url2 = urljoin('https://hungryhouse.co.uk/',href2.extract())
           yield scrapy.Request(url2, callback=self.parse_dir_contents2)       

    def __init__(self):
        try:
            self.driver = webdriver.Chrome("C:/Users/xxxxxx/Downloads/chromedriver_win32/chromedriver.exe")
        except:
            self.driver = webdriver.Chrome("C:/Users/xxxxx/Downloads/chromedriver_win32/chromedriver.exe")
            

    # and now we are on the web page where the restaurants are listed
    # now we need to use Selenium to activate a javescript button to reveal all the page
    def parse_dir_contents2(self,response):    
        self.driver.get(response.url)
        
        # Pressing the "Show More" button until there are no more on the page to reveal all the page
        # But first we need to scroll down to the bottom of the page to allow the "Show More" to work
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1) # waiting 1 seconds for the page to load fully
            next =self.driver.find_element_by_xpath('//*[@id="restsPages"]/a')
            try:
                next.click()
                time.sleep(3) # waiting 3 seconds for the page to load fully
            except:
                break
            
        # Now that the webpage is all revealed Scrapy can bring down all the restaurant URLs
        # I.e. we need to follow the link for every restuarant to get onto its page to get our data
        response1 = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        for href in response1.xpath('//*[@class="restsRestInfo"]/a/@href'):
            url = response1.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents3)

#        self.driver.close()

    # and now Scrapy can take the names, addresses and postcodes of all the restaurants from their URL page
    def parse_dir_contents3(self, response):
        item = HungryhouseItem()
        for sel in response.xpath('//*[@class="restBoxInfo"]'):
            item['name']=sel.xpath('//div/div/div/h1/span/text()').extract()[0].strip()
            item['address']=sel.xpath('//*[@id="restMainInfoWrapper"]/div[@class="restDetailsBox"]/div/h2/span/span/text()').extract()[0].strip()
            item['postcode']=sel.xpath('//*[@id="restMainInfoWrapper"]/div[@class="restDetailsBox"]/div/h2/span/span[last()]/text()').extract()[0].strip()
            yield item

