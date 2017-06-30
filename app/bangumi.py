import requests
from protocols import BaseHandler
import json


# 获取番剧时间表
class Bangumi(object):

    def __init__(self):
        self.url = 'http://bangumi.bilibili.com/api/timeline_v2_global'

    def get_data(self):
        res = requests.get(url=self.url)
        if 304 >= res.status_code >= 200:
            data = json.loads(res.text)['result']
            count = len(data)
            return BaseHandler().write_list(code=200, message='获取成功', count=count, data=data)
        return BaseHandler().write_error()

    # 获取今日更新
    def get_today(self):
        today_list = []
        res = requests.get(url=self.url)
        if 304 >= res.status_code >= 200:
            data = json.loads(res.text)['result']
        return today_list
