# coding:utf-8
import urllib
import uuid
import datetime
import json


class DataModelBase(object):

    def to_string(self, except_none=False):
        for key in self.__dict__:
            data_type = type(self.__dict__[key])
            if data_type == uuid.UUID:
                self.__dict__[key] = str(self.__dict__[key])
            elif data_type == datetime.datetime:
                self.__dict__[key] = self.__dict__[key].strftime('%Y-%m-%dT%H:%M:%S')
            if except_none:
                self.__dict__[key] = '' if self.__dict__[key] is None else self.__dict__[key]
        return self

    def to_url(self):
        for key in self.__dict__:
            if type(self.__dict__[key]) == unicode:
                self.__dict__[key] = urllib.quote(self.__dict__[key].encode('utf8'))
        return self

    @staticmethod
    def check_value(request_data, value):
        re = request_data.get(value)
        if re is None:
            raise "参数缺失， 没有参数 %s" % value
        if type(re) == unicode:
            re = json.loads(re)
        return re

    @staticmethod
    def get_request_values(request_data):
        request_data = json.loads(request_data)
        return DataModelBase.check_value(request_data, u'values')

    @staticmethod
    def load_json(request_data):
        try:
            re = json.loads(request_data)
        except BaseException, e:
            print e.args
            re = "request_data json 转化失败"
        return re


if __name__ == '__main__':
    a = DataModelBase()
    a.__dict__.update({'a': u'测试', 'b': 'test'})
    a.to_url()
    print a.__dict__
