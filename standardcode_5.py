import scrapy
import re

from Rightmove1.items import Rightmove1Item

class Rightmove1Spider(scrapy.Spider):
    name = "rightmove1"
    allowed_domains = ["rightmove.co.uk"]

    with open("estate_agent_ids.txt") as f:
        estate_agent_ids = [str(x.strip('\n')) for x in f.readlines()]

    start_urls = []
    for i in range(len(estate_agent_ids)):
        if estate_agent_ids[i][-3:] == "ram":
            branch_number = estate_agent_ids[i][estate_agent_ids[i].rindex("-")+1:-3]
            start_urls.append("https://www.rightmove.co.uk/property-for-sale/find.html?includeSSTC=true&locationIdentifier=BRANCH%5E" + str(branch_number))
            start_urls.append("https://www.rightmove.co.uk/commercial-property-for-sale/find.html?includeSSTC=true&locationIdentifier=BRANCH%5E" + str(branch_number))
        elif estate_agent_ids[i][-3:] == "lam":
            branch_number = estate_agent_ids[i][estate_agent_ids[i].rindex("-")+1:-3]
            start_urls.append("https://www.rightmove.co.uk/property-to-rent/find.html?includeLetAgreed=true&locationIdentifier=BRANCH%5E" + str(branch_number))
            start_urls.append("https://www.rightmove.co.uk/commercial-property-to-let/find.html?includeLetAgreed=true&locationIdentifier=BRANCH%5E" + str(branch_number))            
        else:
            branch_number = estate_agent_ids[i][estate_agent_ids[i].rindex("-")+1:]
            start_urls.append("https://www.rightmove.co.uk/property-for-sale/find.html?includeSSTC=true&locationIdentifier=BRANCH%5E" + str(branch_number))
            start_urls.append("https://www.rightmove.co.uk/property-to-rent/find.html?includeLetAgreed=true&locationIdentifier=BRANCH%5E" + str(branch_number))
            start_urls.append("https://www.rightmove.co.uk/commercial-property-for-sale/find.html?includeSSTC=true&locationIdentifier=BRANCH%5E" + str(branch_number))
            start_urls.append("https://www.rightmove.co.uk/commercial-property-to-let/find.html?includeLetAgreed=true&locationIdentifier=BRANCH%5E" + str(branch_number))

    start_urls=list(set(start_urls))


    def parse(self, response):
        
        working_page = response.xpath('//*[@class="searchHeader-title"]/span/text()').extract()
        if working_page[0] != "0":

            for sel in response.xpath('//*[@class="l-propertySearch-main"]'):
                name = sel.xpath('.//div[@id="searchSidebar-agentInformation"]/div/div[@class="searchSidebar-agentInformation-address"]/strong/text()').extract()            
                address = sel.xpath('.//div[@id="searchSidebar-agentInformation"]/div/div[@class="searchSidebar-agentInformation-address"]/p/text()').extract()
                telephone = sel.xpath('.//div[@id="searchSidebar-agentInformation"]/div/div[@class="searchSidebar-agentInformation-telephoneNumber"]/span/text()').extract_first()
                results = sel.xpath('.//div[@class="searchHeader-title"]/span/text()').extract()
                branch_url = str(response.url)
                try:
                    branch_id = str(response.url).split("BRANCH%5E")[-1].split("&includeSSTC")[0]
                except ExplicitException:
                    try:
                        branch_id = str(response.url).split("BRANCH%5E")[-1].split("&propertyStatus")[0]
                    except ExplicitException:
                        pass
                item = Rightmove1Item()
                item['name'] = name
                item['address'] = address
                item['telephone'] = telephone
                item['results'] = results
                item['branch_id'] = branch_id
                item['branch_url'] = branch_url
                yield item
                
