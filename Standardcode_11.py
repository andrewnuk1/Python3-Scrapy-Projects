import scrapy
import sys

##from scrapy.http import FormRequest, Request
from Howdens.items import HowdensItem

class howdensSpider(scrapy.Spider):
    name = "howdens"
    allowed_domains = ["www.howdens.com"]

    # read the file that has a list of google coordinates that are converted from postcodes
    with open("postcodeDistricts.txt") as f:
        postcodeDistricts = [x.strip('\n') for x in f.readlines()]

    # from the goole coordinates build the start URLs
    start_urls = []
    for a in range(len(postcodeDistricts)):
        start_urls.append("https://www.howdens.com/hw/depot/GetNearByDepotsFromPlace?itemsCount=10&search={}".format(postcodeDistricts[a]))

    # cycle through up to 10 depots on the page - test on 1 first
    def parse(self, response):
        for sel in response.xpath('/html/body'):
            for i in range(0,10):
                try:
                    item = HowdensItem()
                    item['name'] =sel.xpath('.//text()').re(r'(?<="name": ")(.*?)(?=",)')[i]
                    item['address'] =sel.xpath('.//text()').re(r'(?sm)(?<="address": \[)(.*?)(?=\],)')[i]
                    item['url'] = "/find-a-depot/" + sel.xpath('.//text()').re(r'(?<="url": "\/find-a-depot\/)(.*?)(?=")')[i]
                    item['depotid'] = sel.xpath('.//text()').re(r'(?<="depotid": ")(.*?)(?=")')[i]
                    yield item
                except IndexError:
                    pass
                    
                 
