import scrapy

from justeat1.items import Justeat1Item
from scrapy.http import TextResponse

class Justeat1Spider(scrapy.Spider):
    name = "justeat1"
    allowed_domains = ["just-eat.co.uk"]

    start_urls = ["http://www.just-eat.co.uk/takeaway",]

    def parse(self, response):
        for href in response.xpath("//main[@id='main']/div[@class='grouped-link-list container ']/h2[contains(text(),'Restaurants Near You')]/../div[@class='grouped-link-list__groups']/div/div/ul[@class='grouped-link-list__group-links']/li/a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_url1)
            
        for href1 in response.xpath("//*[@class='grouped-link-list container ']/h2[contains(text(),'Find Takeaways in other locations')]/../div[@class='grouped-link-list__groups']/div/div/ul[@class='grouped-link-list__group-links']/li/a/@href"):
            url1 = response.urljoin(href1.extract())
            yield scrapy.Request(url1, callback=self.parse_dir_contents)

    def parse_dir_url1(self, response):
        for href1 in response.xpath('//*[@class="grouped-link-list__group-links"]/li/a/@href'):
            url1 = response.urljoin(href1.extract())
            yield scrapy.Request(url1, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//main/main/div/div/div[@data-test-id="searchresults"]/div/div/section'):
            item = Justeat1Item()
            item['name'] = sel.xpath('.//a/div/h3[@data-test-id="restaurant_name"]/text()').extract()
            item['cuisine'] = sel.xpath('.//a/div/p[@itemprop="servesCuisine"]/text()').extract()
            item['name_id'] = sel.xpath('.//@data-restaurant-id').extract()
            item['name_url'] = sel.xpath('.//a/@href').extract()
            yield item

