import scrapy
import re

from urllib.parse import urljoin
from autotrader1.items import Autotrader1Item


class Autotrader1Spider(scrapy.Spider):
    name = "autotrader1"
    allowed_domains = ["autotrader.co.uk"]

    start_urls = ["http://www.autotrader.co.uk/car-dealers/search?channel=cars&postcode=M4+3AQ&radius=1501&forSale=on&toOrder=on&page=1"]

    def parse(self,response):
        for href in response.xpath('//*[@class="dealerList__itemName"]/a[@class="dealerList__itemUrl tracking-standard-link"]/@href'):
            dealer_id = href.re('([^-]*)$')[0]
            new_url = ('/json/dealers/stock?advertising-location=at_cars&advertising-location=at_profile_cars&dealer=') + str(dealer_id) + str('&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&page=1&sort=price-asc')
            url_dealer = urljoin('https://www.autotrader.co.uk/',new_url)
            yield scrapy.Request(url_dealer, callback=self.parse_second)          

        next_page = response.xpath('.//a[@class="pagination--right__active"]/@href').extract()
        if next_page:
            next_href = next_page[0]
            next_page_url = next_href
            request = scrapy.Request(url=next_page_url)
            yield request
            
    def parse_second(self,response):
        text_to_search=[]
        for sel in response.xpath('/html/body'):
            for i in range(0,10):
                try:
                    text_to_search.append(sel.xpath('.//text()').re(r'(?="advertType":")(.*?)(?<="isNationalStockAdvert":)')[i])
                    item = Autotrader1Item()
                    item['name'] = re.findall('(?<="name":")(.*?)(?=")',text_to_search[i])
                    item['dealer_url'] = re.findall('(?<="url":")(.*?)(?=")',text_to_search[i])
                    item['cars'] = sel.xpath('.//text()').re(r'(?<="totalResults":)(.*?)(?=,)')
                    item['dealerReviewValue'] = re.findall('(?<="dealerReviewValue":)(.*?)(?=,)',text_to_search[i])
                    item['numberOfDealerReview'] = re.findall('(?<="numberOfDealerReviews":)(.*?)(?=,)',text_to_search[i])
                    item['veh_id'] = re.findall('(?<="id":")(.*?)(?=")',text_to_search[i])
                    item['description'] = re.findall('(?<="title":")(.*?)(?=")',text_to_search[i])
                    item['price'] = re.findall('(?<="price":")(.*?)(?=")',text_to_search[i])
                    item['registration'] = re.findall('(?<="yearText":")(.*?)(?=")',text_to_search[i])
                    item['miles'] = re.findall('(?<="mileage":")(.*?)(?= miles")',text_to_search[i])
                    item['engine'] = re.findall('(?<=miles \| )(.*?)(?= \| )',text_to_search[i])
                    item['transmission'] = re.findall('(?<=L \| )(.*?)(?= \| )',text_to_search[i])
                    item['fuel'] = re.findall('(?<= \| )(\w+)(?= \| )',str(re.findall('(?<=L \| )(.*?)(?=")',text_to_search[i])))                  
                    item['advert_type'] = re.findall('(?<="advertType":")(.*?)(?=")',text_to_search[i])
                    item['page_type'] = re.findall('(?<="sellerType":")(.*?)(?=")',text_to_search[i])
                    item['condition'] = re.findall('(?<="condition":")(.*?)(?=")',text_to_search[i])
                    item['writeOffCategory'] = re.findall('(?<="writeOffCategory":")(.*?)(?=")',text_to_search[i])
                    item['manufacturerApproved'] = re.findall('(?<="manufacturerApproved":)(.*?)(?=,)',text_to_search[i])
                    item['franchiseApproved'] = re.findall('(?<="franchiseApproved":)(.*?)(?=,)',text_to_search[i])
                    item['totalImages'] = re.findall('(?<="totalImages":)(.*?)(?=,)',text_to_search[i])
                    item['hasVideo'] = re.findall('(?<="hasVideo":)(.*?)(?=,)',text_to_search[i])   
                    item['monthlyPayment'] = re.findall('(?<="monthlyPayment":")(.*?)(?=")',text_to_search[i])
                    item['quoteType'] = re.findall('(?<="quoteType":")(.*?)(?=")',text_to_search[i])
                    item['duration'] = re.findall('(?<="duration":)(.*?)(?=,)',text_to_search[i])
                    item['customerDeposit'] = re.findall('(?<="customerDeposit":")(.*?)(?=")',text_to_search[i])
                    item['totalCredit'] = re.findall('(?<="totalCredit":")(.*?)(?=")',text_to_search[i])
                    item['totalAmountPayable'] = re.findall('(?<="totalAmountPayable":")(.*?)(?=")',text_to_search[i])
                    item['representativeApr'] = re.findall('(?<="representativeApr":")(.*?)(?=")',text_to_search[i])
                    item['totalInterestPayable'] = re.findall('(?<="totalInterestPayable":")(.*?)(?=")',text_to_search[i])
                    item['fixedRateInterest'] = re.findall('(?<="fixedRateInterest":")(.*?)(?=")',text_to_search[i])                    
                    item['finalPayment'] = re.findall('(?<="finalPayment":")(.*?)(?=")',text_to_search[i])                    
                    item['optionToPurchaseFee'] = re.findall('(?<="optionToPurchaseFee":")(.*?)(?=")',text_to_search[i])                    
                    yield item

                except IndexError:
                    pass

        current_page = response.xpath('.//text()').re(r'(?<=,"currentPage":)(.*?)(?=,"totalPages":)')[0]
        total_pages = response.xpath('.//text()').re(r'(?<=,"totalPages":)(.*?)(?=,"hasMoreResults":)')[0]

        if current_page != total_pages:
            next_page_number = int(current_page) + 1
            dealer = response.xpath('.//text()').re(r'(?<="dealer_id":")[^","]+')[0]
            print(dealer)
            next_page = '/json/dealers/stock?advertising-location=at_cars&advertising-location=at_profile_cars&dealer=' + dealer + '&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&page=' + str(next_page_number) + '&sort=price-asc'
            next_page_url = urljoin('https://www.autotrader.co.uk/',next_page)
            request = scrapy.Request(url=next_page_url, callback=self.parse_second)
            yield request
