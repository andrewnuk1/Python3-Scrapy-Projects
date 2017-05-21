import scrapy
import time

from Ebags.items import EbagsItem
from selenium import webdriver
from scrapy.http import TextResponse

class ebagsSpider(scrapy.Spider):
    name = "ebags"
    allowed_domains = ["ebags.com"]
    start_urls = ["https://www.ebags.com/brands"]

    global choice

    # running A-M or N-Z, memory can't take A-Z
    choice = 0
    while True:
        to_do = input("Enter 1 for A-M or 2 or N-Z or 3 for just brands: ")
        if to_do == "1":
            choice = 1
            break
        elif to_do == "2":
            choice = 2
        elif to_do == "3":
            choice = 3
            break

    # either yield the brands only or follow the links to further details
    def parse(self, response):
        if choice == 3:
            item = EbagsItem()
            for sel in response.xpath('//*[@class="mainCon"]'):
                brands = sel.xpath('//*[@class="mainCon"]/div[@class="brandListCon"]/div[@class="brandList4Col"]/a/text()').extract()
                brands = [brand.strip() for brand in brands]
                result = zip(brands)
                for brand in result:
                    item['brand'] = brand
                    yield item                
        else:
            list_to_run = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
            for href in response.xpath('//*[@class="mainCon"]/div[@class="brandListCon"]/div[@class="brandList4Col"]/a/@href'):
                if href.extract()[7] in list_to_run[0 + ((choice - 1)*14):13 + ((choice - 1)*13)]:
                    url = response.urljoin(href.extract())
                    print(url)
                    yield scrapy.Request(url, callback=self.parse_dir_contents)

    def __init__(self):
        self.driver = webdriver.Chrome("C:/Users/andrew/Downloads/chromedriver_win32/chromedriver.exe")

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
