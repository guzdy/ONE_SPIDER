# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OneItemImage(scrapy.Item):
    img_url = scrapy.Field()
    img_num = scrapy.Field()
    img_info = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()


class OneItemArticle(scrapy.Item):
    description = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    article = scrapy.Field()
    url = scrapy.Field()


class OneItemQuestion(scrapy.Item):
    quest = scrapy.Field()
    quest_detail = scrapy.Field()
    answer = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
