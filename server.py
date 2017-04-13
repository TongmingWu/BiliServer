import logging

from app.bangumi import Bangumi
from app.bangumi_info import Info
from app.banner import Banner
from flask import Flask, request
from flask_script import Manager
from app.home import Home
from app.video_page import Page
from app.category import Category

from app.live import Live
from app.search import Search
from protocols import BaseHandler

app = Flask(__name__)
app.debug = True
manager = Manager(app)


# 首页接口
@app.route('/api/v1/home/', methods=['GET'])
def get_home():
    return Home().get_data()


# banner接口
@app.route('/api/v1/banner/', methods=['GET'])
def get_banner():
    return Banner().get_banner()


# 首页live接口
@app.route('/api/v1/live/recom/', methods=['GET'])
def get_live_recom():
    return Live().get_live()


# 视频信息接口
@app.route('/api/v1/video/av<aid>/', methods=['GET'])
def get_video_info(aid):
    return Page(aid).get_data()


# 番剧时间表
@app.route('/api/v1/bangumi/', methods=['GET'])
def get_bangumi():
    return Bangumi().get_data()


# 番剧具体信息
@app.route('/api/v1/bangumi/<sid>/', methods=['GET'])
def get_bangumi_info(sid):
    return Info(sid=sid).get_data()


# 视频分类
# param ftid 外层分类 如动画
# param stid 内层分类 如动画中的MAD
@app.route('/api/v1/category/<first_tid>/<second_tid>/', methods=['GET'])
def get_category_video(first_tid, second_tid):
    return


# 获取分类表
@app.route('/api/v1/category/', methods=['GET'])
def get_category():
    return Category().get_category()


# 视频搜索
@app.route('/api/v1/search/', methods=['GET'])
def search():
    word = request.args.get('word')
    if not word:
        return BaseHandler().write_error(404, '关键字不能为空')
    try:
        int(request.args.get('page'))
        page = int(request.args.get('page'))
        order = request.args.get('order')
        return Search(word=word, page=page, order=order).search()
    except ValueError:
        return BaseHandler().write_error(400, '协议错误')


# 初始化logging
def init_log():
    logging.basicConfig(filename='logger.log', level=logging.INFO)


if __name__ == '__main__':
    # init_log()
    manager.run()
