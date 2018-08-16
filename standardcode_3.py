import scrapy

from zoopla.items import ZooplaItem

class ZooplaSpider(scrapy.Spider):
    name = "zoopla"
    allowed_domains = ["zoopla.co.uk"]
    start_urls = ["https://www.zoopla.co.uk/find-agents/estate-agents/directory/a#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/b#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/c#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/d#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/e#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/f#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/g#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/h#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/i#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/j#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/k#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/l#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/m#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/n#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/o#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/p#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/q#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/r#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/s#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/t#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/u#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/v#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/w#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/x#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/y#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/z#directory",
                  "https://www.zoopla.co.uk/find-agents/estate-agents/directory/123",
                                    ]

#   need to change start_url estate-agents and letting-agents
#   need to change 'name' and 'rent' / 'sale'

    def parse(self, response):
        for href in response.xpath('//*[@id="landing-page"]/div/div/ul/li/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//*[@id="content"]/div[@class="agents-results"]/div/div'):
            item = ZooplaItem()
            item['name'] = sel.xpath('.//h2/text() |.//h2/a/text() ').extract()
#            item['name'] = sel.xpath('.//h2/text() |.//h2/a/text() ').extract()
            item['address'] = sel.xpath('normalize-space(.//div[@class="clearfix"]/div/p/span/text())').extract()
            item['sale'] = sel.xpath('.//*[contains(text(), "Residential for sale:")]/strong/a/text()').extract()
#            item['rent'] = sel.xpath('.//*[contains(text(), "Residential to rent:")]/strong/a/text()').extract()
            yield item

        next_page = response.xpath('//*[@class="paginate bg-muted"]/a[contains(text(),"Next")]/@href').extract()
        if next_page:
            next_href = next_page[0]
            next_page_url = 'https://www.zoopla.co.uk' + next_href
            request = scrapy.Request(url=next_page_url, callback=self.parse_dir_contents)
            yield request
