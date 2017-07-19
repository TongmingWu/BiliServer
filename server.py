import logging
import time
import const

from flask_error import FlaskError
from app.bangumi import Bangumi
from app.bangumi_info import Info
from flask import Flask, request, Response
from flask_script import Manager
from app.home import Home
from app.video_page import Page
from app.category import Category
from app.guochuang import Guochuang
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


# 首页live接口
@app.route('/api/v1/live/recom/', methods=['GET'])
def get_live_recom():
    return Live().get_live()


# 视频信息接口
@app.route('/api/v1/video/av<aid>/', methods=['GET'])
def get_video_info(aid):
    return Page(aid).get_data()


# 获取番剧推荐
@app.route('/api/v1/bangumi/recom/', methods=['GET'])
def get_bangumi_rec():
    return


# 番剧时间表
@app.route('/api/v1/bangumi/', methods=['GET'])
def get_bangumi():
    return Bangumi().get_data()


# 获取国创时间表
@app.route('/api/v1/guochuang/', methods=['GET'])
def get_guochuang():
    return Guochuang().get_data()


# 番剧具体信息
@app.route('/api/v1/bangumi/<sid>/', methods=['GET'])
def get_bangumi_info(sid):
    return Info(sid=sid).get_data()


# 视频分类
# param ftid 外层分类 如动画
@app.route('/api/v1/category/<first_tid>/', methods=['GET'])
def get_first_category_video(first_tid):
    return Category(first_tid=first_tid).get_category_video()


# 视频分类
# param ftid 外层分类 如动画
# param stid 内层分类 如动画中的MAD
@app.route('/api/v1/category/<first_tid>/<second_tid>/', methods=['GET'])
def get_second_category_video(first_tid, second_tid):
    return Category(first_tid=first_tid, second_tid=second_tid).get_category_video()


# 获取分类表
@app.route('/api/v1/category/', methods=['GET'])
def get_category():
    return Category().get_category()


# 视频搜索
@app.route('/api/v1/search/', methods=['GET'])
def search():
    word = request.args.get('word')
    if not word:
        return BaseHandler().write_error(const.FAIL_CODE, const.KEYWORD_NONE_MESSAGE)
    try:
        page = request.args.get('page')
        return Search(word=word, page=page).search()
    except Exception:
        return BaseHandler().write_error(const.FAIL_CODE, const.FAIL_CODE)


# cookies测试
@app.route('/api/v1/cookies')
def get_cookies():
    res = Response('add cookies')
    res.set_cookie(key='name', value='tongming', expires=time.time() + 6 * 60)
    return res


@app.errorhandler(FlaskError)
def handle_error(error_json):
    return error_json


# 初始化logging
def init_log():
    logging.basicConfig(filename='logger.log', level=logging.INFO)


if __name__ == '__main__':
    # init_log()
    manager.run()
