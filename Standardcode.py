import scrapy
from urllib.parse import urljoin

from Persimmon.items import PersimmonItem

class persimmonSpider(scrapy.Spider):
    name = "persimmon"
    allowed_domains = ["persimmonhomes.com"]
    start_urls = ["http://www.persimmonhomes.com/sitemap",]
    
    def parse(self, response):
        for href in response.xpath('//*[@class="contacts-item"]/ul/li/a/@href'):
           url = urljoin('http://www.persimmonhomes.com/',href.extract())
           yield scrapy.Request(url, callback=self.parse_dir_contents)
            
    def parse_dir_contents(self, response):
        for sel in response.xpath('//*[@id="aspnetForm"]/div[4]'):
           item = PersimmonItem()
           item['name'] = sel.xpath('//*[@id="aspnetForm"]/div[4]/div[1]/div[1]/div/div[2]/span/text()').extract()
           item['address'] = sel.xpath('//*[@id="XplodePage_ctl12_dsDetailsSnippet_pDetailsContainer"]/div/*[@itemprop="postalCode"]/text()').extract()
           plotnames = sel.xpath('//div[@class="housetype js-filter-housetype"]/div[@class="housetype__col-2"]/div[@class="housetype__plots"]/div[not(contains(@data-status,"Sold"))]/div[@class="plot__name"]/a/text()').extract()
           plotnames = [plotname.strip() for plotname in plotnames]
           plotids = sel.xpath('//div[@class="housetype js-filter-housetype"]/div[@class="housetype__col-2"]/div[@class="housetype__plots"]/div[not(contains(@data-status,"Sold"))]/div[@class="plot__name"]/a/@href').extract()
           plotids = [plotid.strip() for plotid in plotids]
           plotprices = sel.xpath('//div[@class="housetype js-filter-housetype"]/div[@class="housetype__col-2"]/div[@class="housetype__plots"]/div[not(contains(@data-status,"Sold"))]/div[@class="plot__price"]/text()').extract()
           plotprices = [plotprice.strip() for plotprice in plotprices]
           result = zip(plotnames, plotids, plotprices)
           for plotname, plotid, plotprice in result:
               item['plotname'] = plotname
               item['plotid'] = plotid
               item['plotprice'] = plotprice
               yield item

