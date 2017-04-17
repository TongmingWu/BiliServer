import requests
from protocols import BaseHandler
import json


# 获取番剧时间表
class Guochuang(object):
    def get_data(self):
        url = 'http://bangumi.bilibili.com/jsonp/timeline_v2_cn.ver'
        params = {
            'callback': 'gc_timeline'
        }
        res = requests.get(url=url, params=params)
        if 304 >= res.status_code >= 200:
            loads = json.loads(res.text.replace('gc_timeline(', '').replace('});', '}'))
            data = loads['result']
            count = len(data)
            return BaseHandler().write_list(code=200, message='获取成功', count=count, data=data)
        return BaseHandler().write_error()
