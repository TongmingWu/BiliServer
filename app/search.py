import requests
from bs4 import BeautifulSoup
from protocols import BaseHandler
import re


# 搜索推荐字 http://www.bilibili.com/widget/getSearchDefaultWords

class Search(object):
    def __init__(self, word=None, page=1, order='totalrank'):
        if page is None:
            page = 1
        if word is None:
            word = ''
        self.word = word
        self.page = page
        self.order = order      # 排列方式

    def search(self):
        url = 'http://search.bilibili.com/all'
        params = {
            'keyword': self.word,
            'page': self.page,
            'order': self.order
        }
        res = requests.get(url=url, params=params)
        if 304 >= res.status_code >= 200:
            try:
                data = self.__filter(res.text)
                return BaseHandler().write_list(count=len(data), page=self.page, data=data)
            except KeyError or IndexError:
                return BaseHandler().write_error()
        return BaseHandler().write_error()

    def __filter(self, data=None):
        result_list = []
        if data is None:
            return
        soup = BeautifulSoup(data, 'lxml')
        for item in soup.select('.ajax-render > li'):
            aid = int(re.findall(r'av(\d+)', item.select('.title')[0]['href'])[0])
            title = item.select('.title')[0]['title']
            description = item.select('.des')[0].get_text()
            pic = str(soup.select('.img > img')[0]['data-src'])
            if pic.startswith('//'):
                pic = 'http:' + pic
            tags = item.select('.tags > span')
            play = tags[0].get_text()
            if str(play).find('万'):
                play = float(re.search(r'(\d+)(\.\d+)?', play).group(0)) * 10000
            video_review = int(tags[1].get_text())
            create = tags[2].get_text()
            author = tags[3].get_text()
            mid = int(re.findall(r'com/(\d+)', tags[3].select('a')[0]['href'])[0])
            duration = item.select('.so-imgTag_rb')[0].get_text()
            category = item.select('.type')[0].string
            # TODO 根据category去数据库匹配对应的typeid
            coins = 0
            pubdate = ''
            subtitle = ''
            favorites = 0
            typeid = 0
            review = 0
            L = dict([('aid', aid), ('title', title), ('description', description), ('play', play),
                      ('author', author), ('video_review', video_review), ('create', create),
                      ('pic', pic), ('mid', mid), ('duration', duration), ('coins', coins),
                      ('pubdate', pubdate), ('subtitle', subtitle), ('favorites', favorites),
                      ('typeid', typeid), ('review', review)])
            result_list.append(L)
        return result_list
