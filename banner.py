import requests
from protocols import BaseHandler


class Banner(object):
    def __init__(self):
        self.tag = 'banner'
        self.url = 'http://api.bilibili.com/x/web-show/res/loc'
        self.params = {
            'pf': 0,
            'id': 23
        }

    def get_banner(self):
        res = requests.get(url=self.url, params=self.params)
        if 304 >= res.status_code >= 200:
            return self.__filter(res.json())
        return BaseHandler().write_list(502, '获取失败')

    # 过滤成简单数据
    def __filter(self, json_data):
        banner_list = []
        for item in json_data['data']:
            banner_id = item['id']
            name = item['name']
            pic = item['pic']
            url = item['url']
            area = item['area']
            style = item['style']
            L = dict([('id', banner_id), ('name', name), ('pic', pic), ('url', url), ('area', area),
                      ('style', style)])
            banner_list.append(L)
        return BaseHandler().write_list(200, '获取成功', len(banner_list), banner_list)
