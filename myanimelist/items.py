# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyanimelistItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AnimeItem(scrapy.Item):
    animeId = scrapy.Field()
    pic = scrapy.Field()
    enName = scrapy.Field()
    jpName = scrapy.Field()
    type = scrapy.Field()
    episodes = scrapy.Field()
    premiered = scrapy.Field()
    producers = scrapy.Field()
    studios = scrapy.Field()
    source = scrapy.Field()
    characters = scrapy.Field()
    staffs = scrapy.Field()
    themeSongs = scrapy.Field()
