import requests
from bs4 import BeautifulSoup
from protocols import BaseHandler
import re
import json
from app.banner import Banner


class Category(object):
    def __init__(self, first_tid=None, second_tid=None):
        self.tag = 'category'
        self.first_tid = first_tid
        self.second_tid = second_tid

    # 根据分类获取相关视频
    def get_category_video(self):
        # 先拿当前的分类表 --> 再去匹配链接
        video_list = []
        category_table = json.loads(self.get_category())
        if self.first_tid is None:
            return video_list
        for first_item in category_table:
            if self.first_tid == first_item:
                if self.second_tid is None:
                    url = category_table[first_item]['normal']
                    return self.__get_first_data(url=url)
                for second_item in first_item:
                    if self.second_tid == second_item:
                        url = category_table[first_item][second_item]
                        return self.__get_second_data(url=url)
        # 匹配不到第二层分类的情况,有可能为空或没有这个分类
        return BaseHandler().write_error()

    # 获取一级分类的数据
    def __get_first_data(self, url):
        # 有banner | recommend 4 | 各个二级分类 12
        '''
        一级分类中的各个二级分类接口:http://api.bilibili.com/typedynamic/region
        参数: rid --> 二级分类id | pn --> page num | ps --> 当月第几天
        建两张表
        '''
        result = {}
        res = requests.get(url)
        if 304 >= res.status_code >= 200:
            try:
                soup = BeautifulSoup(res.text, 'lxml')
                top_list = self.__get_top_list(self.first_tid)
                result['banner'] = top_list
                return BaseHandler().write_object(result=result)

            except IndexError and KeyError:
                return BaseHandler().write_error()
        return BaseHandler().write_error()

    # 根据url获取二级分类的数据
    def __get_second_data(self, url):
        res = requests.get(url)
        if 304 >= res.status_code >= 200:
            try:
                soup = BeautifulSoup(res.text, 'lxml')

            except IndexError and KeyError:
                return BaseHandler().write_error()
        return BaseHandler().write_error()

    # 获取顶部banner,只有一级分类单独存在的情况才有
    def __get_top_list(self, tid):
        top_list = []
        if self.first_tid is None:
            return top_list
        nid = 0
        if tid == '番剧':
            nid = 34
        elif tid == '国创':
            nid = 102
        elif tid == '影视':
            nid = 7
        else:
            table = {
                '动画': 52,
                '音乐': 58,
                '舞蹈': 64,
                '科技': 76,
                '游戏': 70,
                '生活': 88,
                '鬼畜': 100,
                '时尚': 94,
                '广告': 1466,
                '娱乐': 82
            }
            pv_id = table[tid]
            top_list = Banner(bid=pv_id).get_banner()
        if nid is not 0:
            top_list = self.__get_new_banner(nid=nid)
        return top_list

    # 新的banner格式获取
    def __get_new_banner(self, nid):
        banner_list = []
        url = 'http://bangumi.bilibili.com/jsonp/slideshow/{nid}.ver'.format(nid=nid)
        res = requests.get(url=url)
        if 304 >= res.status_code >= 200:
            json_data = res.json()
            for item in json_data['result']:
                banner_id = item['id']
                name = item['title']
                pic = item['img']
                url = item['link']
                area = 0
                style = 0
                L = dict([('id', banner_id), ('name', name), ('pic', pic), ('url', url), ('area', area),
                          ('style', style)])
                banner_list.append(L)
        return banner_list

    # 获取分类表
    def get_category(self):
        category = {}
        url = 'http://www.bilibili.com'
        res = requests.get(url)
        if 304 >= res.status_code >= 200:
            soup = BeautifulSoup(res.text, 'lxml')
            for item in soup.select('.nav-menu > li'):
                first_type = {}
                for i_item in item.select('.i_num > li'):
                    title = i_item.select('a > b')[0].get_text()
                    url = i_item.select('a')[0]['href']
                    first_type[title] = 'http:' + url if url.startswith('//') else url
                first_url = item.select('a')[0]['href']
                first_type['normal'] = 'http:' + first_url if first_url.startswith('//') else first_url
                category[item.select('em')[0].get_text()] = first_type
            return json.dumps(category)
        return BaseHandler().write_error()
