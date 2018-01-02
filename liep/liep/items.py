# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepItem(scrapy.Item):

    name = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    address = scrapy.Field()
    # 投递时间反馈
    experience = scrapy.Field()
