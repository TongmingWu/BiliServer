import requests
from bs4 import BeautifulSoup
from protocols import BaseHandler
import re


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

    def __get_top_list(self, tid):
        top_list = []
        # TODO 建立分类表
        return top_list
