#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import chardet
import re
from bs4 import BeautifulSoup

INFO_URL = "http://www.bjsubway.com/station/zjgls/#"
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

alias_names = ["one", "two", "four", "five", "six", "seven", "eight", "nine",
               "ten", "thirteen", "fourteen", "fifteen", "bt", "cp", "yz",
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

        # 获取线路名字
        pattern = r"^.*线"
        line_name = re.search(pattern, line_table.tr.td.text).group(0)

        # 获取站和站间距
        stations = []
        distances = []
        all_trs = line_table.find_all('tr')
        for tr in all_trs[2:]:
            partition_name = tr.th.text.split('――')[0]
            pattern_distance = tr.td.text
            stations.append(partition_name)
            distances.append(int(pattern_distance))
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



def navigate(start, target, strategy = None):
    '''
    导航
    :param start: 起点
    :param target: 终点
    :return:
    '''
    pathes = [[Path(end=start)]]

    seen_line = []

    while len(pathes) != 0:
        path = pathes.pop(0)
        current_station = path[-1].end  # 上一次找到这里了

        current_lines = STATIONS[current_station].lines

        # 查看当前 line 是否直达
        for cl in current_lines:
            if cl in seen_line: continue
            if target in LINES[cl].stations:
                path.append(Path(start=current_station, end=target, line=cl))
                return path
            else:
                # 加入该 line 上的所有的换乘点
                for station in LINES[cl].stations:
                    if station != current_station and STATIONS[station].is_transferred:
                        pathes.append(path + [Path(start=current_station, end=station, line=cl)])
            seen_line.append(cl)
        if strategy:
            pathes = sorted(pathes, key=strategy)


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


class Path():
    start = None
    end = None
    line = None
    distance = None

    def __init__(self, start='', end='', line=''):
        self.start = start
        self.end = end
        self.line = line
        if start and end and line:
            self.cal_distance()

    def cal_distance(self):
        line_object = LINES[self.line]
        start_index = line_object.stations.index(self.start)
        end_index = line_object.stations.index(self.end)
        if line_object.is_cycle:
            # 环路存在两条路径，取最小
            self.distance = min(
                                sum(line_object.distances[start_index:end_index]),
                                sum(line_object.distances[end_index:start_index])
                               )
        else:
            if end_index > start_index:
                self.distance = sum(line_object.distances[start_index:end_index])
            else:
                self.distance = sum(line_object.distances[end_index:start_index])

def printRoute(route):
    '''
    传入的是 Path 对象列表
    :return:
    '''
    # for path in route:
    #    print("\t\t{}: {} -> {}".format(path.line, path.start, path.end))

    return '\t\t'.join([str("\t\t{}: {} -> {}".format(path.line, path.start,
                                                      path.end)) for path in route[1:]])

def calAllDistances(pathes):
    '''
    传入某条换乘方案，计算其总路程
    :return:
    '''
    return sum([path.distance for path in pathes[1:]])

def comprehensiveDisAndStaNums (pathes):
    '''
    根据总路程和换乘站比较
    总路程大约区间：1000-10000 权值设置成 1/1000
    换乘站差值大约区间：1-2 权值设置成 5
    :return:
    '''
    all_distance = sum([path.distance for path in pathes[1:]])
    all_station = len(pathes)
    return all_distance * 1/10000 + all_station * 5

if __name__ == "__main__":
    init_lines()
    init_transferred()
    print('\n回龙观 TO 西红门:')
    print("默认路径：")
    print(printRoute(navigate('回龙观', '西红门')))
    print("最少换乘：")
    print(printRoute(navigate('回龙观', '西红门', strategy=lambda x : len(x))))
    print("最短距离：")
    print(printRoute(navigate('回龙观', '西红门', strategy=lambda x : calAllDistances(x))))
    print("综合考虑：")
    print(printRoute(navigate('回龙观', '西红门', strategy=lambda x : comprehensiveDisAndStaNums(x))))

    print('\n苏州街 TO 顺义:')
    print("默认路径：")
    print(printRoute(navigate('苏州街', '顺义')))
    print("最少换乘：")
    print(printRoute(navigate('苏州街', '顺义', strategy=lambda x : len(x))))
    print("最短距离：")
    print(printRoute(navigate('苏州街', '顺义', strategy=lambda x :
    calAllDistances(x))))
    print("综合考虑：")
    print(printRoute(navigate('苏州街', '顺义', strategy=lambda x :
    comprehensiveDisAndStaNums(x))))

    print('\n七里庄 TO 丰台站:')
    print("默认路径：")
    print(printRoute(navigate('七里庄', '丰台站')))
    print("最少换乘：")
    print(printRoute(navigate('七里庄', '丰台站', strategy=lambda x : len(x))))
    print("最短距离：")
    print(printRoute(navigate('七里庄', '丰台站', strategy=lambda x : len(x))))
    print("综合考虑：")
    print(printRoute(navigate('七里庄', '丰台站', strategy=lambda x :
    comprehensiveDisAndStaNums(x))))

'''
OUTPUT:
回龙观 TO 西红门:
默认路径：
		13号线: 回龙观 -> 西直门				4号线: 西直门 -> 公益西桥				大兴线: 公益西桥 -> 西红门
最少换乘：
		13号线: 回龙观 -> 西直门				4号线: 西直门 -> 公益西桥				大兴线: 公益西桥 -> 西红门
最短距离：
		13号线: 回龙观 -> 知春路				10号线: 知春路 -> 海淀黄庄				4号线: 海淀黄庄 -> 公益西桥				大兴线: 公益西桥 -> 西红门
综合考虑：
		13号线: 回龙观 -> 西直门				4号线: 西直门 -> 公益西桥				大兴线: 公益西桥 -> 西红门

苏州街 TO 顺义:
默认路径：
		10号线: 苏州街 -> 知春路				13号线: 知春路 -> 望京西				15号线: 望京西 -> 顺义
最少换乘：
		10号线: 苏州街 -> 知春路				13号线: 知春路 -> 望京西				15号线: 望京西 -> 顺义
最短距离：
		10号线: 苏州街 -> 北土城				8号线: 北土城 -> 奥林匹克公园				15号线: 奥林匹克公园 -> 顺义
综合考虑：
		10号线: 苏州街 -> 北土城				8号线: 北土城 -> 奥林匹克公园				15号线: 奥林匹克公园 -> 顺义

七里庄 TO 丰台站:
默认路径：
		9号线: 七里庄 -> 六里桥				10号线: 六里桥 -> 丰台站
最少换乘：
		9号线: 七里庄 -> 六里桥				10号线: 六里桥 -> 丰台站
最短距离：
		9号线: 七里庄 -> 六里桥				10号线: 六里桥 -> 丰台站
综合考虑：
		14号线: 七里庄 -> 西局				10号线: 西局 -> 丰台站
'''

'''
分析：
默认路径通过 BFS 计算，其结果和最少换乘的结果始终一致。
详细结果分析：
1) 回龙观 -> 西红门
    百度地图推荐最优方案：和 默认路径、最小换乘、综合考虑的方案相同，和最短路径的方案不同
    不同的原因是 最短距离 只是在中间状态时进行 path 的比较，不代表最终状态，可能导致得到的最短距离路径实际不是。

2) 苏州街 -> 顺义
    百度地图推荐最优方案：和 最短距离、综合考虑的方案相同，和默认路径、最小换乘路径不同
    原因在于 最小换乘不考虑路程，优先搜索到了一个非最优解。

3）七里庄 -> 丰台站
    百度推荐最优方案：和 综合考虑 的方案相同，和最小换乘、最短距离方案不同
    原因还是淡村值考虑最小换乘或者距离都容易导致优先搜索到非最优解。
'''