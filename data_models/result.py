# coding: utf-8
import json


class JsonResult(object):

    def __init__(self):
        self.state = -1
        self.message = ''
        self.data = ''

    @staticmethod
    def success(data=''):
        re = JsonResult()
        re.state = 1
        re.message = 'Success'
        re.data = data
        return re

    @staticmethod
    def error(message, data=''):
        re = JsonResult()
        re.state = 0
        re.message = message
        re.data = data
        return re

    def to_json(self):
        try:
            re_json = json.dumps(
                {
                    'state': self.state,
                    'message': self.message,
                    'data': self.data
                }
                # , encoding='gbk'
            )
        except BaseException, e:
            print e.args
            re_json = JsonResult.error(u'结果json序列化失败').to_json()
            # re_json = self.to_json2()
        return re_json

    def to_json2(self):
        try:
            re_json = json.dumps(
                {
                    'state': self.state,
                    'message': self.message,
                    'data': str([self.data])
                }
                # , encoding='gbk'
            )
        except BaseException, e:
            print e.args
            re_json = JsonResult.error(u'结果json序列化失败').to_json()
        return re_json
