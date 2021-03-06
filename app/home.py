import random

from protocols import BaseHandler
import requests
from app.banner import Banner
import const


class Home(object):
    def __init__(self):
        self.tag = 'home'
        self.url = 'http://www.bilibili.com/index/ding.json'

    def get_data(self):
        res = requests.get(url=self.url)
        if 304 >= res.status_code >= 200:
            results = self.__filter(res.json())
            banner_list = Banner().get_banner()
            results['banner'] = banner_list
            return BaseHandler().write_object(const.SUCCESS_CODE, const.SUCCESS_MESSAGE, results)
        return BaseHandler().write_list(const.FAIL_CODE, const.FAIL_MESSAGE)

    def __filter(self, json_data):
        category_list = {}
        inner_list = []
        for category in json_data:
            if category in ['list', 'results', 'pages', 'code']:
                continue
            for item in json_data[category]:
                inner_list.append(json_data[category][item])
        # todo 做成分页推荐
        if len(inner_list) > 20:
            category_list['video_list'] = random.sample(inner_list, 20)
        else:
            category_list['video_list'] = inner_list
        return category_list
