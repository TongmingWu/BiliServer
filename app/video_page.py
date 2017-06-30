import hashlib

import requests
from bs4 import BeautifulSoup
from protocols import BaseHandler
import json
import re
from app.category import Category

appkey = 'f3bb208b3d081dc8'
SECRETKEY_MINILOADER = '1c15888dc316e05a15fdd0a02ed6584f'


# 视频信息
class Page(object):
    def __init__(self, aid=0):
        self.aid = aid

    # 获取视频信息
    def get_data(self):
        url = 'http://www.bilibili.com/video/av%s/' % self.aid
        res = requests.get(url, allow_redirects=True)
        history = res.history
        if len(history) == 0:
            return self.__filter_normal_video(res.text)
        elif len(history) > 0:  # 出现重定向
            return self.__filter_bangumi_video(res.text)
        return BaseHandler().write_error()

    # 清洗普通视频数据
    def __filter_normal_video(self, data):
        result = {}
        soup = BeautifulSoup(data, 'lxml')
        try:
            mid = soup.select('.u-face > a')[0]['mid']  # mid可以根据http://space.bilibili.com/<mid>进入作者空间
            author_info = self.__get_author_info(mid)
            play_info = self.__get_play_info()

            title = soup.select('.info > .v-title')[0].get_text()
            tag_list = []
            for tag in soup.select('.tag-list > li'):
                tag_list.append(tag.select('a')[0].get_text())
            desc = soup.select('#v_desc')[0].get_text()
            cid = 0
            re_findall = re.findall(r'cid=(\d+)', soup.select('.scontent > script')[0].string)
            if re_findall:
                cid = re_findall[0]  # 获取视频真正链接 - 弹幕 的重要参数
            video_url_info = self.__get_video_url(cid)
            create_time = str(soup.select('time')[0]['datetime']).replace('T', ' ')
            category = None
            category_url = None
            for item in soup.select('.tminfo > span'):
                category = item.select('a')[0].string
                category_url = 'http://www.bilibili.com%s' % item.select('a')[0]['href']

            # 相关视频
            relative_list = self.__get_relative_video()
            result['author_info'] = author_info
            result['play_info'] = play_info
            result['title'] = title
            result['tag_list'] = tag_list
            result['desc'] = desc
            result['cid'] = int(cid)
            result['create_time'] = create_time
            result['video_info'] = video_url_info
            result['category'] = category
            result['category_url'] = category_url
            result['relative_list'] = relative_list
        except IndexError or KeyError:  # 网页改版的情况
            return BaseHandler().write_error()
        return BaseHandler().write_object(code=200, message='获取成功', result=result)

    # 清洗番剧视频数据
    def __filter_bangumi_video(self, data):
        # todo 获取番剧视频详情信息
        result = {}
        return BaseHandler().write_object(code=200, message='获取成功', result=result)

    # 获取作者信息
    def __get_author_info(self, mid=0):
        author_info = {}  # 作者信息
        url = 'http://api.bilibili.com/cardrich'
        params = {
            'callback': 'callback',
            'mid': mid,
        }
        res = requests.get(url=url, params=params)
        if 304 >= res.status_code >= 200:
            author_info = str(res.text).replace('callback(', '').replace('});', '}')
        return json.loads(author_info)['data']

    # 获取播放信息
    def __get_play_info(self):
        play_info = {}
        url = 'http://api.bilibili.com/archive_stat/stat'
        params = {
            'callback': 'callback',
            'aid': self.aid,
        }
        res = requests.get(url, params)
        if 304 >= res.status_code >= 200:
            play_info = str(res.text).replace('callback(', '').replace('});', '}')
        return json.loads(play_info)['data']

    # 获取视频真正的连接
    def __get_video_url(self, cid=0):
        video_download_info = {}
        sign_this = hashlib.md5(bytes('cid={cid}&from=miniplay&player=1{SECRETKEY_MINILOADER}'
                                      .format(cid=cid, SECRETKEY_MINILOADER=SECRETKEY_MINILOADER),
                                      'utf-8')).hexdigest()
        url = 'http://interface.bilibili.com/playurl?&cid=' + str(
            cid) + '&from=miniplay&player=1' + '&sign=' + sign_this
        res = requests.get(url)
        if 304 >= res.status_code >= 200:
            soup = BeautifulSoup(res.text, 'lxml')
            size = soup.select('size')[0].string
            length = soup.select('length')[0].string
            url_list = []
            findall = re.findall(r'CDATA\[(http:.*)]', res.text)
            for item in findall:
                url_list.append(item.replace(']', ''))
            video_download_info['size'] = size
            video_download_info['length'] = length
            video_download_info['url_list'] = url_list
        return video_download_info

    # 获取相关视频
    def __get_relative_video(self):
        result_list = []
        url = 'http://comment.bilibili.com/recommendnew,{aid}'.format(aid=self.aid)
        res = requests.get(url)
        if 304 >= res.status_code >= 200:
            result_list = res.json()['data']
        return result_list
