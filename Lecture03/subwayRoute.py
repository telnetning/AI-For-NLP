#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import chardet
import re
from bs4 import BeautifulSoup
from collections import Counter

INFO_URL = "http://www.bjsubway.com/station/zjgls/#"
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

alias_names = ["one", "two", "four", "five", "six", "seven", "eight", "nine",
               "ten", "thirteen", "thirteen", "fifteen", "bt", "cp", "yz",
               "dx", "fs", "jc"]

lines = []

def init_lines():
    '''
    爬取网页信息，初始化 lines
    :return:
    '''
    res = requests.get(INFO_URL, headers = HEADERS)
    encoding_type = chardet.detect(res.content)
    res.encoding = encoding_type["encoding"]
    soup = BeautifulSoup(res.text, 'lxml')
    for name in alias_names:
        # if-else to solve pages table-attr-class's problem
        if name == "seven":
            line_table = soup.find_all('table', class_ = 'six')[1]
        elif name == "dx":
            line_table = soup.find_all('table', class_ = 'four')[1]
        else:
            line_table = soup.find_all('table', class_ = name)[0]

        # get line name
        pattern = r"^.*线"
        line_name = re.search(pattern, line_table.tr.td.text).group(0)
        # print(line_name)
        # print("======{}======".format(line_table.tr.td.text))

        # get stations and distances
        stations = []
        distances = []
        all_trs = line_table.find_all('tr')
        for tr in all_trs[2:]:
            partition_name = tr.th.text.split('――')[0]
            pattern_distance = tr.td.text
            stations.append(Station(partition_name))
            distances.append(pattern_distance)
        stations.append(Station(all_trs[len(all_trs) - 1]
                        .th.text.split('――')[1]))

        # 判断是否为环线
        is_cycle = False
        if stations[0].name == stations[-1].name:
            is_cycle = True

        lines.append(SubwayLine(line_name, stations, distances, is_cycle))

def init_transferred():
    '''
    找到所有的可换乘站，标记
    因为可换乘点远远少于不可换乘点，因此找到所有的可换乘点，
    再进行遍历效率比直接遍历效率高
    :return:
    '''
    all_stations_repeated = []
    for line in lines:
        for station in line.stations:
            all_stations_repeated.append(station.name)

    is_transferred = [k for k, v in Counter(all_stations_repeated).items()
                      if v > 1]
    # print(is_transferred)
    # 标记
    # for station in is_transferred:
    #    for line in lines:


def navigate(start, target):
    '''
    导航
    :param start: 起点
    :param target: 终点
    :return:
    '''
    pathes = [[start]]

    while pathes:
        path = pathes[0]
        current_station = path[-1] # 上一次找到这里了


class SubwayLine():
    name = None #
    alias_name = None # 网页元素中的 table 的 class 名字
    stations = [] # 所有的站点
    distances = [] # 站与站之间的距离
    is_cycle = False # 是否为环线

    def __init__(self, alias_name, stations, distances, is_cycle):
        self.alias_name = alias_name
        self.stations = stations
        self.distances = distances
        self.is_cycle = is_cycle

class Station():
    name = None
    is_transferred = False # 该站是否可换乘
    lines = None # 该站在哪些线路上

    def __init__(self, name):
        self.name = name

if __name__ == "__main__":
    init_lines()
    init_transferred()
