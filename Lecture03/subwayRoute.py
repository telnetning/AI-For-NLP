#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://baike.baidu.com/"
ALL_LINE_URL = BASE_URL + "item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485?fr=aladdin"


def get_lines_url():
    html_doc = requests.get(ALL_LINE_URL)
    soup = BeautifulSoup(html_doc)
    print(soup.prettify())

if __name__ == "__main__":
    get_lines_url()
