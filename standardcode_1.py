import scrapy
from urllib.parse import urljoin

from checkatrade.items import CheckatradeItem

class checkatradeSpider(scrapy.Spider):
    name = "checkatrade"
    allowed_domains = ["checkatrade.com"]

    start_urls = ["https://www.checkatrade.com/SiteMap.aspx",]

    def parse(self, response):
        for href in response.xpath('//*[@class="directory-index push-half--top"]/a/@href'):
           url = urljoin('https://www.checkatrade.com/',href.extract())
           yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//*[@class="directory"]/tbody/tr'):
           member = sel.xpath('normalize-space(.//td/a/text())').extract()
           memberurl = sel.xpath('normalize-space(.//td/a/@href)').extract()
           basedin = sel.xpath('normalize-space(.//td[2]/text())').extract()
           memberfor = sel.xpath('normalize-space(.//td[3]/text())').extract()
           reports = sel.xpath('normalize-space(.//td[4]/text())').extract()
           rating = sel.xpath('normalize-space(.//td[5]/text())').extract()
           item = CheckatradeItem()
           item['member'] = member
           item['memberurl'] = memberurl
           item['basedin'] = basedin
           item['memberfor'] = memberfor
           item['reports'] = reports
           item['rating'] = rating
           yield item
