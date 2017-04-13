import requests
from protocols import BaseHandler
import json


class Info(object):
    def __init__(self, sid=0):
        self.sid = sid

    def get_data(self):
        url = 'http://bangumi.bilibili.com/jsonp/seasoninfo/{sid}.ver'.format(sid=self.sid)
        params = {
            'callback': 'seasonListCallback'
        }
        res = requests.get(url, params=params)
        if 304 >= res.status_code >= 200:
            try:
                result = json.loads(res.text.replace('seasonListCallback(', '').replace('});', '}'))['result']
                recommend_bangumi = self.__get_recommend_bangumi()
                result['recommend_bangumi'] = recommend_bangumi
                return BaseHandler().write_object(code=200, message='获取成功', result=result)
            except KeyError:
                return BaseHandler().write_error(400, '协议错误')
        return BaseHandler().write_error()

    def __get_recommend_bangumi(self):
        url = 'http://bangumi.bilibili.com/web_api/season/recommend/{sid}.json'.format(sid=self.sid)
        res = requests.get(url)
        if 304 >= res.status_code >= 200:
            loads = json.loads(res.text)
            return loads['result']['list']
        return BaseHandler().write_error()
