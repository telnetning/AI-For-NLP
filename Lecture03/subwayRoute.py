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

'''
lines 存放所有的线路
结构：键值对，{'5号线': SubwayLineObject}

stations 存放所有的站点
结构：键值对，{'回龙观': StationObject}
'''
LINES = {}
STATIONS = {}

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
            stations.append(partition_name)
            distances.append(pattern_distance)
        stations.append(all_trs[len(all_trs) - 1]
                        .th.text.split('――')[1])

        # 判断是否为环线
        is_cycle = False
        if stations[0] == stations[-1]:
            is_cycle = True

        LINES[line_name] = SubwayLine(line_name, name, stations, distances,
                                        is_cycle)

def init_transferred():
    for line_name, line_info in LINES.items():
        for station in line_info.stations:
            if not station in STATIONS.keys():
                STATIONS[station] = Station(station)
                STATIONS[station].lines = [line_name]
            else:
                if line_name != '2号线' or station != '西直门': # 环线特殊情况
                    STATIONS[station].lines.append(line_name)
                    STATIONS[station].is_transferred = True



def navigate(start, target):
    '''
    导航
    :param start: 起点
    :param target: 终点
    :return:
    '''
    pathes = [[start]]

    seen_line = []

    while len(pathes) != 0:
        path = pathes.pop(0)
        current_station = path[-1]  # 上一次找到这里了

        current_lines = STATIONS[current_station].lines

        # 查看当前 line 是否直达
        for cl in current_lines:
            if cl in seen_line: continue
            if target in LINES[cl].stations:
                path.append(target)
                return path
            else:
                # 加入该 line 上的所有的换乘点
                for station in LINES[cl].stations:
                    if station != current_station and STATIONS[station].is_transferred:
                        pathes.append(path + [station])
            seen_line.append(cl)



class SubwayLine():
    name = None  #
    alias_name = None  # 网页元素中的 table 的 class 名字
    stations = []  # 所有的站点
    distances = []  # 站与站之间的距离
    is_cycle = False  # 是否为环线

    def __init__(self, name, alias_name, stations, distances, is_cycle):
        self.name = name
        self.alias_name = alias_name
        self.stations = stations
        self.distances = distances
        self.is_cycle = is_cycle


class Station():
    name = None
    is_transferred = False  # 该站是否可换乘
    lines = []  # 该站在哪些线路上, 字符串列表

    def __init__(self, name):
        self.name = name


if __name__ == "__main__":
    init_lines()
    init_transferred()
    print("\n最小换乘：")
    print('回龙观\tTO\t西红门:\t' + str('\t->\t'.join(navigate('回龙观', '西红门'))))
    print('苏州街\tTO\t顺义:\t' + str('\t->\t'.join(navigate('苏州街', '顺义'))))
    print('安河桥北\tTO\t东单:\t' + str('\t->\t'.join(navigate('安河桥北', '东单'))))
