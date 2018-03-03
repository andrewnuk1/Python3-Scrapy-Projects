import scrapy
import time

from BerkeleyHomes.items import BerkeleyHomesItem
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
           yield scrapy.Request(url, callback=self.parse_dir_url1)

    def parse_dir_url1(self, response):
        for href1 in response.xpath('//*/a[@class="action view red"]/@href'):
           url1 = response.urljoin(href1.extract())
           yield scrapy.Request(url1, callback=self.parse_dir_contents)

    def __init__(self):
        # you will need to determine the path to your chrome driver
        # for Windows10 it is "C:/Users/username/Downloads/chromedriver_win32/chromedriver.exe"
        self.driver = webdriver.Chrome("C:path-to-driver/chromedriver_win32/chromedriver.exe")

    def parse_dir_contents(self, response):
        count = 0
        self.driver.get(response.url)

        # press the next page button if present and if scraped the first page already        
        while True:
            body = self.driver.find_element_by_css_selector('body')
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(10)
            if count >0:
                try:
                    next = self.driver.find_element_by_xpath('//ul[@class="pagination"]/li[@class="next"]/a')
                    count = count +1
                    next.click()
                except:
                    break
            else:
                count = count + 1

            time.sleep(10)  # need to ensure entire page is loaded before scraping
            response1 = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
            item = BerkeleyHomesItem()
            for sel in response1.xpath('//*[@class="flexStretch"]'):
                item['name'] = sel.xpath('//*[@class="span10"]/div/h1/text()').extract()
                item['address'] = sel.xpath('//*[@class="span10"]/div/h2/text()').extract()
                plotnames = sel.xpath('//*/td/a[contains(text(),"View")]/../../td[2]/text()').extract()
                plotnames = [plotname.strip() for plotname in plotnames]
                plotprices = sel.xpath('//*/td/a[contains(text(),"View")]/../../td[@data-sort]/text()').extract()
                plotprices = [plotprice.strip() for plotprice in plotprices]
                result = zip(plotnames, plotprices)
                for plotname, plotprice in result:
                    item['plotname'] = plotname
                    item['plotprice'] = plotprice
                    yield item
