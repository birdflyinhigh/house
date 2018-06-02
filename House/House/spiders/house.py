# -*- coding: utf-8 -*-
import scrapy
import re
import time
from House.items import HouseItem
from House.connector import insert_into_mysql

class HouseSpider(scrapy.Spider):
    name = 'house'
    allowed_domains = ['163.com']
    start_urls = ['http://esf.house.163.com/gz/search/0-0-0-0-1.html', 'http://esf.house.163.com/bj/search/0-0-0-0-1.html', 'http://esf.house.163.com/sh/search/0-0-0-0-1.html']
    prefix = 'http://esf.house.163.com'

    def parse(self, response):
        """
        :param response: 获取start urls的response
        :return: 转交request,使用callback函数,解析每个区域的经纪人列表url
        """

        city = response.xpath('//*[@class="hed_city_name"]/text()').extract_first()
        area_ids = response.xpath('//*[@class="al_dis_list"]/em/@_value').extract()
        area_names = response.xpath('//*[@class="al_dis_list"]/em/text()').extract()
        for i in range(len(area_ids)):
            if i == 2:
                break
            area_name = area_names[i]
            area_id = area_ids[i]
            if area_name == u'不限':
                continue
            # 匹配替换，构造各个区域的列表页面url
            regex = r'search\/[0-9]+-'
            repl = r'search/{}-'.format(area_id)
            url = re.sub(regex, repl, response.url)
            # 配置area_info meta data
            area_info = {
                'area_name': area_name,
                'city': city,
                'url': url
            }
            time.sleep(1)
            yield scrapy.Request(
                url=url,
                callback=self.parse_page_data,
                meta={'area_info': area_info}
            )

    def parse_page_data(self, response):
        """进入<区域>经纪人第一页，获取该区域里面的所有页面的url,提交下一个解析"""

        area_info = response.meta['area_info']
        postfixs = response.xpath('//*[@class="pager_box"]/a/@href').extract()
        for postfix in postfixs:
            url = self.prefix + postfix
            time.sleep(0.4)
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
            time.sleep(0.6)
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
        # print '*'*100
        insert_into_mysql(item=item)

        # yield item

    def list_to_string(self, items):
        info = ''
        for item in items:
            info += item + ','
        return info[:-1]



