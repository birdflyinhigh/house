# -*- coding: utf-8 -*-
import scrapy
import re
import time
from House.items import HouseItem
from House.connector import insert_into_mysql

class HouseSpider(scrapy.Spider):
    name = 'house'
    allowed_domains = ['163.com']
    start_urls = []
    # 北京地区的
    base_url_bj = 'http://esf.house.163.com/bj/search/{}-0-0-0-1.html'
    base_url_gz = 'http://esf.house.163.com/gz/search/{}-0-0-0-1.html'
    base_url_sh = 'http://esf.house.163.com/sh/search/{}-0-0-0-1.html'
    for i in range(0, 19):
        bj_url = base_url_bj.format(i)
        print(bj_url)
        start_urls.append(bj_url)
    # 广州地区
    for i in range(0, 14):
        gz_url = base_url_gz.format(i)
        print(gz_url)
        start_urls.append(gz_url)
    # 上海地区
    for i in range(0, 20):
        sh_url = base_url_sh.format(i)
        print(sh_url)
        start_urls.append(sh_url)
    prefix = 'http://esf.house.163.com'

    def parse(self, response):
        """url 是区信息，功能是找该区的所有列表页面url
        """
        city = response.xpath('//*[@class="hed_city_name"]/text()').extract_first()
        print(city)
        area_name = response.xpath('//*[@class="al_item al_item_cr"]/text()').extract_first()
        base_url = response.url
        print(area_name)
        area_info = {
            'area_name': area_name,
            'city': city,
        }
        try:
            pages = response.xpath('//*[@class="pager_box"]/a/text()').extract()[-2]
        except:
            pages = 1
        pages = int(pages)
        print(pages, type(pages))
        for i in range(pages):
            end_fix = '-{}.html'.format(str(i+1))
            url = base_url.replace('-1.html', end_fix)
            yield scrapy.Request(
                url=url,
                callback=self.parse_agent_list,
                meta={'area_info': area_info}
            )

    def parse_agent_list(self,response):
        """针对每个列表页面的数据，获取对应的详情页url"""
        area_info = response.meta['area_info']
        agents = response.xpath('//*[@class="al_agent_cell clearfix"]')
        for agent in agents:
            postfix = agent.xpath('div[1]/a/@href').extract_first()
            url = self.prefix + postfix
            area_info['company'] = agent.xpath('//*[@class="al_agent_company"]/text()').extract_first()
            # time.sleep(0.02)
            yield scrapy.Request(
                url=url,
                callback=self.parse_agent_detail,
                meta={'area_info': area_info}
            )

    def parse_agent_detail(self,response):
        """解析详情页面的数据，获取具体的详情页面，yield items"""
        area_info = response.meta['area_info']
        item = dict()
        item['city'] = area_info['city']
        item['area'] = area_info['area_name']
        company = response.xpath('//*[@class="va_agent_company"]/text()').extract_first()
        if company:
            item['company'] = company
        else:
            item['company'] = area_info['company']
        item['name'] = response.xpath('//*[@class="va_agent_name"]/text()').extract_first()
        item['mobile'] = response.xpath('//*[@class="number-hidden"]/@cel').extract_first()
        item['service_area'] = response.xpath('//*[@class="va_agent_dis"]/em[2]/text()').extract_first()
        plates = response.xpath('//*[@class="va_plate_list"]/em/text()').extract()[1:]
        item['plate'] = self.list_to_string(plates)
        communities = response.xpath('//*[@class="va_community_list"]/em/text()').extract()[1:]
        item['community'] = self.list_to_string(communities)
        item['url'] = response.url
        print('*'*100)
        print(item)
        print('*'*100)
        insert_into_mysql(item=item)


    def list_to_string(self, items):
        info = ''
        for item in items:
            info += item + ','
        return info[:-1]



