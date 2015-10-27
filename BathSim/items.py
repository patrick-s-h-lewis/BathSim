# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BathHarvestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    doi = scrapy.Field()
    authors = scrapy.Field()
    free_text = scrapy.Field()
    year = scrapy.Field()
    publication = scrapy.Field()
    abstract = scrapy.Field()
    
