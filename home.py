from protocols import BaseHandler
import requests


class Home(object):
    def __init__(self):
        self.tag = 'home'
        self.url = 'http://www.bilibili.com/index/ding.json'

    def get_data(self):
        res = requests.get(url=self.url)
        if 304 >= res.status_code >= 200:
            return self.__filter(res.json())
        return BaseHandler().write_list(502, '获取失败')

    def __filter(self, json_data):
        category_list = {}
        for category in json_data:
            if category == 'list' or category == 'results' or category == 'pages':
                continue
            inner_list = []
            for item in json_data[category]:
                inner_list.append(json_data[category][item])
            category_list[category] = inner_list
        return BaseHandler().write_object(200, '获取成功', category_list)