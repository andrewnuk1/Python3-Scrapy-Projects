import scrapy

from rightmove.items import RightmoveItem

class RightmoveSpider(scrapy.Spider):
    name = "rightmove"
    allowed_domains = ["rightmove.co.uk"]

    # we need to run this in stages.  1 to 5 reading up to 700 lines from the rightmovepostcodes file
    # a seperate text file contains a list of the 2934 district codes in the UK
    with open("rightmovepostcodes.txt") as f:
        postcodes = [x.strip('\n') for x in f.readlines()]

    while True:
        to_do = input("Enter Stage 1 to 5  ")
        if to_do == "1" or to_do == "2" or to_do =="3" or to_do =="4" or to_do =="5":
            break

    # build a list of urls to scrap from the text file   
    start_urls = []
    startrange = 700*(int(to_do)-1)
    endrange = 700*(int(to_do))
    if endrange > len(postcodes):
        endrange = len(postcodes)
    for a in range(startrange,endrange):
        start_urls.append(postcodes[a])


    def parse(self, response):
        for sel in response.xpath('//*[@id="summaries"]'):
            names = sel.xpath('.//h2[@class="branchname"]/a/text()').extract()
            names = [name.strip() for name in names]
            telephones = sel.xpath('.//div[@class="details"]/div[contains(., "0")][1]/text()').re(r'0\s*(.*)')
            telephones = [telephone.strip() for telephone in telephones]
            branch_ids = sel.xpath('.//div[@class="photos"]/a/@href').re(r'(?<=agent/)(.*)')
            branch_ids = [branch_id.strip() for branch_id in branch_ids]
            result = zip(names, telephones, branch_ids)
            for name, telephone, branch_id in result:
                item = RightmoveItem()
                item['name'] = name
                item['telephone'] = telephone
                if "#" in str(branch_id):
                    item['branch_id'] = str(branch_id.split(".html")[0]) + str(branch_id[-3:])
                else:
                    item['branch_id'] = branch_id.split(".html")[0]
                yield item
               
        next_page = response.xpath('//*[@id="pagenavigation"]/a[@class="pagenavigation active"][contains(., "next")]/@href').extract()
        if next_page:
            next_href = next_page[0]
##            next_page_url = "http://www.rightmove.co.uk" + next_href  [website code changed]
            next_page_url = next_href
            request = scrapy.Request(url=next_page_url)
            yield request
