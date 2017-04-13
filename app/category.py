import requests
from bs4 import BeautifulSoup
from protocols import BaseHandler
import re
import json


class Category(object):
    def __init__(self):
        self.tag = 'category'

    def get_data(self):
        # 有banner
        # 二级分类数据
        url = 'www.bilibili.com/video/douga.html'
        res = requests.get(url)
        if 304 >= res.status_code >= 200:
            try:
                soup = BeautifulSoup(res.text, 'lxml')
                top_list = self.__get_top_list(soup.select('.top-list'))

            except IndexError and KeyError:
                return BaseHandler().write_error()
        return BaseHandler().write_error()

    # 获取分类表
    def get_category(self):
        category = {}
        url = 'http://www.bilibili.com'
        res = requests.get(url)
        if 304 >= res.status_code >= 200:
            soup = BeautifulSoup(res.text, 'lxml')
            for item in soup.select('.nav-menu > li'):
                first_type = {}
                for i_item in item.select('.i_num > li'):
                    title = i_item.select('a > b')[0].get_text()
                    url = i_item.select('a')[0]['href']
                    first_type[title] = 'http:' + url if url.startswith('//') else url
                first_url = item.select('a')[0]['href']
                first_type['normal'] = 'http:' + first_url if first_url.startswith('//') else first_url
                category[item.select('em')[0].get_text()] = first_type
            return json.dumps(category)
        return BaseHandler().write_error()

    def __get_top_list(self, tid):
        top_list = []
        # TODO 建立分类表
        return top_list
