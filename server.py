from flask_script import Manager
from flask import Flask, redirect, request, render_template, abort, Response
from banner import Banner
from live import Live
from home import Home

app = Flask(__name__)
app.debug = True
manager = Manager(app)


# 首页接口
@app.route('/api/v1/home', methods=['GET'])
def get_home():
    return Home().get_data()


# banner接口
@app.route('/api/v1/banner', methods=['GET'])
def get_banner():
    return Banner().get_banner()


# 首页live接口
@app.route('/api/v1/live/recom')
def get_live_recom():
    return Live().get_live()


if __name__ == '__main__':
    manager.run()
