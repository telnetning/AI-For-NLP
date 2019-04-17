#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://baike.baidu.com"
ALL_LINE_URL = BASE_URL + "/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485" \
                          "?fr=aladdin"
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4'}


def get_lines_url():

    '''
    获取所有的路线及其百度百科链接页
    :return:
    '''

    res = requests.get(ALL_LINE_URL, headers = HEADERS)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')

    # 默认找的节点是其第一个子节点，过滤之后只剩下需要的那个表格
    table_tag = filter(lambda tag : tag.tr.th and tag.tr.th.text == u"线路",
                        soup.find_all('table'))

    assert len(table_tag) == 1
    all_trs = table_tag[0].find_all('tr')
    all_trs = filter(lambda tr : tr.a,
                     all_trs)

    all_trs.pop(len(all_trs) - 1) # 去掉最后一个非数据

    all_lines = {}
    for tr in all_trs:
        all_lines[tr.a.text] = tr.a['href']

    assert len(all_lines) == 19
    return all_lines

def get_line_stations_info(name, link):
    '''
    ### http://www.bjsubway.com/station/zjgls/# 百度百科数据不完整的可以从这里取数据
    获取各站区间及站间距
    :param name: 地铁线路名
    :param link: 百度百科链接页面
    :return:
    '''
    print(u"Get {} info Begin".format(name))
    page_url = BASE_URL + link
    res = requests.get(page_url, headers = HEADERS)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    table_tag = filter(lambda tag : tag.tr.th and tag.tr.th.text == u'起始/终到车站',
                       soup.find_all('table'))
    try:
        assert len(table_tag) == 1
    except AssertionError as e:
        print(e)
        return
    all_trs = table_tag[0].find_all('tr')
    all_trs.pop(0) # 去掉导航栏
    for tr in all_trs:
        path_name = tr.th.text
        path_distance = tr.td.text
        print(u"path_name:{} path_distance:{}".format(path_name, path_distance))

if __name__ == "__main__":
    all_lines = get_lines_url()
    # 获取所有线路链接
    for name, href in all_lines.items():
        print(u"name:{} link:{}".format(name, href))

        get_line_stations_info(name, href)
