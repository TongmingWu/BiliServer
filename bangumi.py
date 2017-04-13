import requests
from protocols import BaseHandler
import json


# 获取番剧时间表
class Bangumi(object):
    def get_data(self):
        url = 'http://bangumi.bilibili.com/jsonp/season_rank_list/global/3.ver'
        params = {
            'callback': 'bangumiRankCallback'
        }
        res = requests.get(url=url, params=params)
        if 304 >= res.status_code >= 200:
            loads = json.loads(res.text.replace('bangumiRankCallback(', '').replace('});', '}'))
            data = loads['result']['list']
            count = len(data)
            return BaseHandler().write_list(code=200, message='获取成功', count=count, data=data)
        return BaseHandler().write_error()
