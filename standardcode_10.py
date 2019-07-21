import scrapy

from deliveroo.items import DeliverooItem

class DeliverooSpider(scrapy.Spider):
    name = "deliveroo"
    allowed_domains = ["deliveroo.co.uk"]

    start_urls = ["https://deliveroo.co.uk/sitemap",]

    def parse(self, response):
        for href in response.xpath('//ul/div/li/ul/li/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)
            print(url)

    def parse_dir_contents(self, response):
        for sel in response.xpath('/html/body/div[1]/div[1]'):
            item = DeliverooItem()
            item['name'] = sel.xpath('//div[@class="restaurant__details"]/h1/text()').extract()
            item['address'] = sel.xpath('//div[@class="restaurant__details"]/div/div/small[contains(@class,"address")]/text()').extract()
            yield item
