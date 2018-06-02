# -*- coding: utf-8 -*-
import pymysql


# def insert_item(item):
#
#
#
# # sql = """
#     create table agent_info(
#         id int unsigned primary key auto_increment not null,
#         name varchar(10) ,
#         company varchar(100) ,
#         mobile varchar(100) ,
#         service_area varchar(100) ,
#         city varchar(100),
#         area varchar(500),
#         plate varchar(500) ,
#         community varchar(500) ,
#         url varchar(500)
#     );"""


def insert_into_mysql(item):
    item = dict(item)
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='mysql', db='house', charset='utf8')
    cur = conn.cursor()

    name = item['name']
    company = item['company']
    mobile = item['mobile']
    service_area = item['service_area']
    city = item['city']
    area = item['area']
    plate = item['plate']
    community = item['community']
    url = item['url']


    # name = name.__str__().decode('unicode-escape')
    # company = company.__str__().decode('unicode-escape')
    # mobile = mobile.__str__().decode('unicode-escape')
    # service_area = service_area.__str__().decode('unicode-escape')
    # city = city.__str__().decode('unicode-escape')
    # area = area.__str__().decode('unicode-escape')
    # plate = plate.__str__().decode('unicode-escape')
    # community = community.__str__().decode('unicode-escape')
    # url = url.__str__().decode('unicode-escape')

    # sql = 'insert into agent_info (name, company, mobile, service_area, city, area, plate, community, url) values (%s, %s, %s, %s, %s, %s，%s, %s, %s);'% (name, company, mobile, service_area, city, area, plate, community, url)





    #
    # name = item['name']
    # address = item['address']
    # url = item['url']
    # contact = item['contact']
    # description = item['desc']
    # big_category = item['big_category']
    # small_category = item['small_category']
    # child_category = item['child_category']
    #
    sql = 'insert into agent_info (name,company,mobile,service_area,city,area,plate,community,url) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s");' % (name,company,mobile,service_area,city,area,plate,community,url)
    # print(words)
    cur.execute(sql)

    conn.commit()