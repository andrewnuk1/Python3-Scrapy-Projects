import scrapy

from urllib.parse import urljoin
from CrestNicholson.items import CrestnicholsonItem

class crestnicholsonSpider(scrapy.Spider):
    name = "crestnicholson"
    allowed_domains = ["crestnicholson.com"]
    start_urls = [
        "https://www.crestnicholson.com/sitemap-html",        
    ]

    def parse(self, response):
        for href in response.xpath('//*[@class="resp-tabs-container hor_1 tabs_sitemap"]/div[3]/ul/li/a/@href'):
            url1 = urljoin("https://www.crestnicholson.com",href.extract())
            url=urljoin(url1,"availability")
            print(url)
            yield scrapy.Request(url, callback=self.parse_dir_contents)
       
    def parse_dir_contents(self, response):
        for sel in response.xpath('//div[@class="container"]'):
           item = CrestnicholsonItem()
           item['name'] = sel.xpath('//h1[@class="availability-header__title"]/text()').re(r'Available homes at \s*(.*)')
           item['address'] = sel.xpath('//*[@class="availability-header__location"]/text()').extract()[1].strip()
           plotprices = sel.xpath('//a[@class="btn btn_blue btn_arrowed"]/../../td[last()-2]/text()').extract()
           plotprices = [plotprice.strip() for plotprice in plotprices]
           plotnames = sel.xpath('//a[@class="btn btn_blue btn_arrowed"]/../../td[1]/text()').extract()
           plotnames = [plotname.strip() for plotname in plotnames]
           plotids = sel.xpath('//a[@class="btn btn_blue btn_arrowed"]/@href').extract()
           plotids = [plotid.strip() for plotid in plotids]
           result = zip(plotnames, plotids, plotprices)
           for plotname, plotid, plotprice in result:
               item['plotname'] = plotname
               item['plotid'] = plotid
               item['plotprice'] = plotprice
               yield item
