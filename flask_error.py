import json
import logging

'''Flask整体错误处理'''


class FlaskError(Exception):
    def __init__(self, status_code=500, message='服务器出错'):
        self.status_code = status_code
        self.message = message

    def to_json(self):
        error = dict([('code', self.status_code), ('message', self.message)])
        logging.error(msg=Exception.args)
        return json.dumps(error, ensure_ascii=False)
