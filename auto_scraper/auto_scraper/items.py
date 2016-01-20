# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutoScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AutoItem(scrapy.Item):
    gp_id = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    kms = scrapy.Field()
    ccs = scrapy.Field()
    color = scrapy.Field()
    year = scrapy.Field()
