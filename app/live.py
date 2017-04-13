import requests
from protocols import BaseHandler
import json


# 首页直播数据
class Live(object):
    def __init__(self):
        self.tag = 'live'
        self.url = 'http://live.bilibili.com/bili/recom'
        self.params = {
            'callback': 'callback',
        }

    def get_live(self):
        res = requests.get(url=self.url, params=self.params)
        if 304 >= res.status_code >= 200:
            return self.__filter(res.text)
        return BaseHandler().write_error()

    # 过滤成简单数据
    def __filter(self, json_data):
        json_data = str(json_data).replace('callback(', '').replace('});', '}')
        json_data = json.loads(json_data)['data']['recommend']
        return BaseHandler().write_list(200, '获取成功', len(json_data), json_data)
