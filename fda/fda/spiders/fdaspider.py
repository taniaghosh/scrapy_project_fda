from scrapy import Spider, Request
from fda.items import FdaItem
import re


class FdaSpider(Spider):
    name = "FDA_spider"
    allowed_urls = ['https://www.fda.gov/']
    start_urls = ['https://www.fda.gov/drugs/development-approval-process-drugs/new-drugs-fda-cders-new-molecular-entities-and-new-therapeutic-biological-products']

    def parse(self,response):
        drug_years = response.xpath('//*[@id="main-content"]/div/ul[2]/li/a/@href').extract() 

        for year in drug_years:
            year_url = 'https://www.fda.gov/drugs/new-drugs-fda-cders-new-molecular-entities-and-new-therapeutic-biological-products/novel-drug-approvals' + year.split('novel-drug-approvals')[1]
            yield Request(url = year_url, callback = self.parse_year_page)

    def parse_year_page(self,response):
        
        rows = response.xpath('//tbody/tr')
        # print("="* 50)
        # print(len(rows))
        # print("="* 50)

        for row in rows:
            
            drug_name = row.xpath('./td[2]//a/text()').extract_first()
            if not drug_name:
                drug_name = row.xpath('./td[3]//a/text()').extract_first()
            
            active_ingredients = row.xpath('./td[3]/text()').extract_first()
            
            year = row.xpath('./td[4]/text()').extract_first()
            use = row.xpath('./td[5]/text()').extract_first()

         #     print("="* 50)
        #     print(len(drug_name))
        #     print("="* 50)
        #     # print(active_ingredients)
        #     # print("=" * 50)
        #     print(year)
        #     print("=" * 50)
        #     # print(use)
        #     # print("=" * 50)
            
            meta = {'drug_name' : drug_name,
            'active_ingredients' : active_ingredients,
            'year' : year,
            'use': use}

            # print("=" * 55)
            # print(meta)
            # print("=" * 55)



            drug_urls = row.xpath('./td[2]//a/@href').extract()
            if not drug_urls:
                drug_urls = row.xpath('./td[3]//a/@href').extract()
            
            for url in drug_urls:
                yield Request(url = url, callback = self.parse_drug_page, meta = meta)

    def parse_drug_page(self,response):
        company = response.xpath('//span[@class="appl-details-top"]/text()').extract()[1].strip()


        
        rows =  response.xpath('//*[@id="exampleProd"]/tbody/tr') 

        for row in rows:
            strength = row.xpath('.//td[3]/text()').extract_first()
            dosageform_route = row.xpath('.//td[4]/text()').extract_first()
            marketing_status = row.xpath('.//td[5]/text()').extract_first()
            TE_code = row.xpath('.//td[6]/text()').extract_first().strip()
            RLD = row.xpath('.//td[7]/text()').extract_first()
            RS = row.xpath('.//td[8]/text()').extract_first()

            drug_class = response.xpath('//*[@id="exampleApplOrig"]/tbody/tr//td[4]/text()').extract_first().strip()
            review_priority = response.xpath('//*[@id="exampleApplOrig"]/tbody/tr//td[5]/text()').extract_first().strip()

            item = FdaItem()
            item['drug_name'] = response.meta['drug_name']
            item['active_ingredients'] = response.meta['active_ingredients']
            item['year'] = response.meta['year']
            item['use'] = response.meta['use']
            item['company'] = company
            item['strength'] = strength
            item['dosageform_route'] = dosageform_route
            item['marketing_status'] = marketing_status
            item['TE_code'] = TE_code
            item['RLD'] = RLD
            item['RS'] = RS
            item['drug_class'] = drug_class
            item['review_priority'] = review_priority

            yield item



        
