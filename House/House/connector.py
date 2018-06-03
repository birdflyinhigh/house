# -*- coding: utf-8 -*-
import pymysql

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

    sql = 'insert into agent_info (name,company,mobile,service_area,city,area,plate,community,url) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s");' % (name,company,mobile,service_area,city,area,plate,community,url)

    cur.execute(sql)

    conn.commit()
conn = pymysql.connect(host='localhost', port=3306, user='root', password='mysql', db='house', charset='utf8')
cur = conn.cursor()


def check_sum():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='mysql', db='house', charset='utf8')
    cur = conn.cursor()
    sql = """select count(*) as "{}" from agent_info where area="{}";"""
    sh_list = ['不限', '黄浦', '卢湾', '静安', '徐汇', '浦东', '长宁', '虹口', '杨浦', '普陀', '闸北', '闵行', '宝山', '嘉定', '青浦', '奉贤', '崇明', '金山', '松江', '上海周边']
    bj_list = ['朝阳', '海淀', '丰台', '东城', '西城', '石景山', '昌平', '通州', '大兴', '顺义', '亦庄开发区', '房山', '门头沟', '怀柔', '北京周边', '密云', '平谷', '延庆', '不限']
    gz_list = ['不限', '天河', '番禺', '海珠', '白云', '越秀', '花都', '增城', '荔湾', '黄埔', '南沙', '从化', '周边']
    print_total(bj_list, '北京')
    print_total(sh_list, '上海')
    print_total(gz_list, '广州')


def print_total(bj_list, city):
    sql = """select count(*) as "{}" from agent_info where area="{}";"""
    sql_total = """select count(*) from agent_info where city="{}";"""
    for bj in bj_list:
        new_sql = sql.format(bj, bj)
        # print(new_sql)
        cur.execute(new_sql)
        data = cur.fetchone()
        print(city, bj, data[0])
    cur.execute(sql_total.format(city))
    data = cur.fetchone()
    print(city,'总记录数:', data[0])


check_sum()