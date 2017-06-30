from protocols import BaseHandler
import requests
import json

'''获取番剧推荐数据'''


class BangumiRecommend(object):
    def __init__(self):
        pass

    def get_data(self):
        return

    # 获取预告片
    def __get_feature(self):
        url = 'http://bangumi.bilibili.com/jsonp/static/35.ver'
        feature_list = []
        res = requests.get(url=url)
        if 304 >= res.status_code >= 200:
            data = json.loads(res.text)
            for item in data['result']:
                feature_list.append(item)
        return feature_list

    # 获取今日更新
    def __get_today(self):

        return
