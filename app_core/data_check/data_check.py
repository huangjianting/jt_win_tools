# coding: utf-8
from uuid import UUID


class DataCheck(object):

    @staticmethod
    def is_uuid(data_string):
        try:
            UUID(data_string)
            return True
        except:
            return False

    @staticmethod
    def is_not_none(data_string):
        if data_string is None:
            return False
        else:
            return True

    @staticmethod
    def len_not_zero(data_string):
        try:
            if len(data_string) > 0:
                return True
        except:
            pass
        return False

    @staticmethod
    def is_int(data_string):
        try:
            int(data_string)
            return True
        except:
            return False

    @staticmethod
    def is_not_empty(data_string):
        if data_string == '' or data_string == u'' or data_string == [] or data_string == {}:
            return False
        else:
            return True
