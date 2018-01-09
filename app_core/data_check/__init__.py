# coding: utf-8
from data_check import DataCheck


method_dict = dict(
    UUID=DataCheck.is_uuid,
    NotNone=DataCheck.is_not_none,
    LenNotZero=DataCheck.len_not_zero,
    IsInt=DataCheck.is_int,
    IsNotEmpty=DataCheck.is_not_empty,
)


def check_string(data_string, check_list, default_value=None, error_message=None):
    if type(check_list) != list:
        check_list = [check_list]
    for line in check_list:
        if line not in method_dict.keys():
            raise BaseException('check method is not found')
        if not method_dict.get(line)(data_string):
            if default_value is not None:
                return default_value
            else:
                if error_message is None:
                    raise BaseException('data error')
                else:
                    raise BaseException(error_message)
    return data_string
