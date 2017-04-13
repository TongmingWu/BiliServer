import logging
from flask_script import Manager
from flask import Flask, redirect, request, render_template, abort, Response
from banner import Banner
from live import Live
from home import Home
from video_page import Page
from bangumi import Bangumi
from bangumi_info import Info
from category import Category
from search import Search
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
@app.route('/api/v1/live/recom/')
def get_live_recom():
    return Live().get_live()


# 视频信息接口
@app.route('/api/v1/video/av<aid>/')
def get_video_info(aid):
    return Page(aid).get_data()


# 番剧时间表
@app.route('/api/v1/bangumi/')
def get_bangumi():
    return Bangumi().get_data()


# 番剧具体信息
@app.route('/api/v1/bangumi/<sid>/')
def get_bangumi_info(sid):
    return Info(sid=sid).get_data()


# 视频分类
@app.route('/api/v1/category/')
def get_category():
    return


# 视频搜索
@app.route('/api/v1/search/')
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
