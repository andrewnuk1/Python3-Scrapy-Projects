import scrapy

from onthemarket.items import OnthemarketItem

class OnthemarketSpider(scrapy.Spider):
    name = "onthemarket"
    allowed_domains = ["onthemarket.com"]

# a text file with the list of UK district postcodes
    with open("agentspostcode.txt") as f:
        agentspostcodes = [x.strip('\n') for x in f.readlines()]  

    start_urls = []
    for a in range(len(agentspostcodes)):
        start_urls.append(agentspostcodes[a])

    def parse(self, response):
        for sel in response.xpath('//*[@id="properties"]'):
            names = sel.xpath('.//li/div[2]/div/h3/a/text()').extract()
            names = [name.strip() for name in names]
            addresses = sel.xpath('.//li/div[2]/div/p/a/text()').extract()
            addresses = [address.strip() for address in addresses]
            result = zip(names, addresses)
            for name, address in result:
                item = OnthemarketItem()
                item['name'] = name
                item['address'] = address
                yield item

        next_page = response.xpath('//*[@title="Next page"]/@href').extract()
        if next_page:
            next_href = next_page[0]
            next_page_url = 'https://www.onthemarket.com' + next_href
            request = scrapy.Request(url=next_page_url)
            yield request

