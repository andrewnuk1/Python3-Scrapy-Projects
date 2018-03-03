import scrapy

from urllib.parse import urljoin
from ASOS.items import AsosItem

class ASOSSpider(scrapy.Spider):
    name = "ASOS"
    allowed_domains = ["asos.com"]
    start_urls = [
        "http://www.asos.com/women/jeans/cat/?cid=3630",        
        "http://www.asos.com/women/dresses/cat/?cid=8799",        
        "http://www.asos.com/men/t-shirts-vests/cat/?cid=7616",        
        "http://www.asos.com/women/shoes/cat/?cid=4172",        
        "http://www.asos.com/men/shoes-boots-trainers/cat/?cid=4209",    
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@data-auto-id="productList"]'):
           item = AsosItem()
           item['category'] = sel.xpath('//div[@id="plp"]/div/section/h1/text()').extract()
           names = sel.xpath('//div[@data-auto-id="productTileDescription"]/div/div/p/text()').extract()
           names = [name.strip() for name in names]
           prices = sel.xpath('//span[@data-auto-id="productTilePrice"]/text()').extract()
           prices = [price.strip() for price in prices]
           product_ids = sel.xpath('//article[@data-auto-id="productTile"]/../article/@id').extract()
           product_ids = [product_id.strip() for product_id in product_ids]
           product_urls = sel.xpath('//article[@data-auto-id="productTile"]/a/@href').extract()
           product_urls = [product_url.strip() for product_url in product_urls]
           result = zip(names, prices, product_ids, product_urls)
           for name, price, product_id, product_url in result:
               item['name'] = name
               item['price'] = price
               item['product_id'] = product_id
               item['product_url'] = product_url
               yield item

        next_page = response.xpath('//*[@data-auto-id="loadMoreProducts"]/@href').extract()
        if next_page:
            next_href = next_page[0]
            print(next_page[0])
            next_href = urljoin("http://www.asos.com",next_page[0])
            print(next_href)
            request = scrapy.Request(url=next_href, callback=self.parse)
            yield request
