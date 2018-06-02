# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 姓名
    name = scrapy.Field()
    # 公司
    company = scrapy.Field()
    # 电话
    mobile = scrapy.Field()
    # 服务区域
    service_area = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 区域
    area = scrapy.Field()
    # 板块
    plate = scrapy.Field()
    # 小区
    community = scrapy.Field()
    # 个人主页url
    url = scrapy.Field()

