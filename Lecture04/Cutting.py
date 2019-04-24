#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from functools import lru_cache
"""
动态规划问题之一维切割问题
一根钢筋各个长度的价格：[1,5,8,9,10,17,17,20,24,30]
任意给一根钢筋，怎样切割价钱最高
"""

origin_prices = [1,5,8,9,10,17,17,20,24,30]

prices = defaultdict(int)

for i, p in enumerate(origin_prices):
    prices[i+1] = p


@lru_cache(maxsize=2**10) # 装饰器缓存，不缓存n足够大时会递归过深报错
def r(n):
    """
    r(n) = max(p(n), r(n-1) + r(1), ....,r(1)+r(n-1))
    :return:
    """
    return max([ prices[n-1] ] + [r(n-i) + r(i) for i in range(1, n)])

print(r(100))

"""
动态规划可以分解成三个部分：
1. 子问题重复
2. 缓存子问题的解
3. 实现socution
"""
