import scrapy
from urllib.parse import urljoin

from Persimmon.items import PersimmonItem

class persimmonSpider(scrapy.Spider):
    name = "persimmon"
    allowed_domains = ["persimmonhomes.com"]
    start_urls = ["https://www.persimmonhomes.com/find-your-new-home"]

    def parse(self, response):
        for href in response.xpath('//div[@class="accordion"]/div[@class="card"]/div/div[@class="card-body region-list"]/ul/li/a/@href'):
           url = urljoin('http://www.persimmonhomes.com/',href.extract())
           print(url)
           yield scrapy.Request(url, callback=self.parse_dir_contents1)

    def parse_dir_contents1(self, response):
        for href in response.xpath('//div[@class="row my-5 available-house-container"]/div/a/@href'):
           url = urljoin('http://www.persimmonhomes.com/',href.extract())
           #print url
           yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//div[@class="master-outer"]'):
           item = PersimmonItem()
           item['name'] = sel.xpath('//h2[@class="t20 fw300"]/a[@class="t-g"]/text()').extract()
           item['address'] = sel.xpath('//h2[@class="t20 fw300"]/text()[2]').extract()
           plotnames = sel.xpath('//div[@class="row my-5 justify-content-center"]/div/div/table/tbody/tr/td[1]/text()').extract()
           plotnames = [plotname.strip() for plotname in plotnames]
           plotids = sel.xpath('//div[@class="row my-5 justify-content-center"]/div/div/table/tbody/tr/td[1]/text()').extract()
           plotids = [plotid.strip() for plotid in plotids]
           plotprices = sel.xpath('//div[@class="row my-5 justify-content-center"]/div/div/table/tbody/tr/td[3]/text()[1]').extract()
           plotprices = [plotprice.strip() for plotprice in plotprices]
           result = zip(plotnames, plotids, plotprices)
           for plotname, plotid, plotprice in result:
               item['plotname'] = plotname
               item['plotid'] = plotid
               item['plotprice'] = plotprice
               yield item
