# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FdaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    drug_name = scrapy.Field()
    active_ingredients = scrapy.Field()
    year = scrapy.Field()
    use = scrapy.Field()
    company = scrapy.Field()
    strength = scrapy.Field()
    dosageform_route = scrapy.Field()
    marketing_status = scrapy.Field()
    TE_code = scrapy.Field()
    RLD = scrapy.Field()
    RS = scrapy.Field()
    drug_class = scrapy.Field()
    review_priority = scrapy.Field()

