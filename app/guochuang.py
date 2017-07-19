import requests
from protocols import BaseHandler
import json
import const


# 获取国产动画时间表
class Guochuang(object):
    def get_data(self):
        url = 'http://bangumi.bilibili.com/api/timeline_v2_cn'
        res = requests.get(url=url)
        if 304 >= res.status_code >= 200:
            # loads = json.loads(res.text.replace('gc_timeline(', '').replace('});', '}'))
            data = json.loads(res.text)['result']
            count = len(data)
            return BaseHandler().write_list(code=const.SUCCESS_CODE, message='获取成功', count=count, data=data)
        return BaseHandler().write_error()
