from flask import jsonify
import logging


class BaseHandler(object):
    '''公共基类'''

    def __write_json(self, response=None):
        return jsonify(response)

    # 只有code 和 message的情况
    def write_normal(self, code=200, message='获取成功'):
        return self.__write_json({'code': code, 'message': message})

    # 对象
    def write_object(self, code=200, message='获取成功', result=None):
        if result is None:
            result = {}
        return self.__write_json({
            'code': code,
            'message': message,
            'result': result,
        })

    # 列表
    def write_list(self, code=200, message='获取成功', count=0, page=1, data=None):
        if data is None:
            data = []
        return self.__write_json({
            'code': code,
            'message': message,
            'result': {
                'count': count,
                'data': data,
                'page': page,
            }
        })

    # 错误
    def write_error(self, code=502, message='获取失败'):
        return self.__write_json({
            'code': code,
            'message': message
        })
